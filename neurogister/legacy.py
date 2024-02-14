

import os
import json
import hashlib
import logging
import pathlib
import requests
import shutil
import zipfile


def get_home():
    """ Set a user-writeable file-system location to put files. """
    if 'SCILPY_HOME' in os.environ:
        scilpy_home = os.environ['SCILPY_HOME']
    else:
        scilpy_home = os.path.join(os.path.expanduser('~'), '.scilpy')
    return scilpy_home


class ScilpyFetcher:
    drive_endpoint = "https://drive.usercontent.google.com/download?"
    local_endpoint = get_home()

    def __init__(self, archive_list, local_endpoint=None):
        if local_endpoint is not None:
            self.local_endpoint = local_endpoint
        if archive_list is not None:
            self.archive_list = archive_list

    def download_file_from_google_drive(self, id, destination):
        """
        Download large file from Google Drive.
        Parameters
        ----------
        id: str
            id of file to be downloaded
        destination: str
            path to destination file with its name and extension
        """
        def get_confirm_token(response):
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    return value

            return None

        def save_response_content(response, destination):
            CHUNK_SIZE = 32768

            with open(destination, "wb") as f:
                for chunk in response.iter_content(CHUNK_SIZE):
                    f.write(chunk)

        session = requests.Session()
        params = {'id': id, 'confirm': True}
        response = session.get(self.drive_endpoint, params=params, stream=True)
        token = get_confirm_token(response)

        if token:
            params['confirm'] = token
            response = session.get(self.drive_endpoint, params=params, 
                                   stream=True)

        save_response_content(response, destination)

    def fetch_data(self, files_dict=None, keys=None, test_md5=False, unpack=True):
        """
        Fetch data. Typical use would be with gdown.
        But with too many data accesses, downloaded become denied.
        Using trick from https://github.com/wkentaro/gdown/issues/43.
        """

        if files_dict is None:
            files_dict = self.archive_list

        if not os.path.exists(self.local_endpoint):
            os.makedirs(self.local_endpoint)

        if keys is None:
            keys = files_dict.keys()
        elif isinstance(keys, str):
            keys = [keys]
        for f in keys:
            url_id, md5 = files_dict[f]
            full_path = os.path.join(self.local_endpoint, f)
            full_path_no_ext, ext = os.path.splitext(full_path)

            CURR_URL = self.drive_endpoint + 'export=download&confirm=y&id=' + url_id
            if not os.path.isdir(full_path_no_ext):
                if ext == '.zip' and not os.path.isdir(full_path_no_ext):
                    logging.warning(
                        'Downloading and extracting {} from url {}'
                        ' to {}'.format(f, CURR_URL, self.local_endpoint))

                    # Robust method to Virus/Size check from GDrive
                    self.download_file_from_google_drive(url_id, full_path)

                    with open(full_path, 'rb') as file_to_check:
                        data = file_to_check.read()
                        md5_returned = hashlib.md5(data).hexdigest()

                    if test_md5 and md5_returned != md5:
                        raise ValueError('MD5 mismatch for file {}.'.format(f))

                    if unpack:
                        try:
                            # If there is a root dir, we want to skip one level.
                            z = zipfile.ZipFile(full_path)
                            zipinfos = z.infolist()
                            root_dir = pathlib.Path(
                                zipinfos[0].filename).parts[0] + '/'
                            assert all([s.startswith(root_dir) for s in z.namelist()])
                            nb_root = len(root_dir)
                            for zipinfo in zipinfos:
                                zipinfo.filename = zipinfo.filename[nb_root:]
                                if zipinfo.filename != '':
                                    z.extract(zipinfo, path=full_path_no_ext)
                        except AssertionError:
                            # Not root dir. Extracting directly.
                            z.extractall(full_path)
                        finally:
                            z.close()
                            os.remove(full_path)
                else:
                    raise NotImplementedError(
                        "Data fetcher was expecting to deal with a zip file.")

            else:
                # toDo. Verify that data on disk is the right one.
                logging.warning("Not fetching data; already on disk.")
