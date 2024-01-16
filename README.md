

# Setup the DVC registry
```
dvc init
dvc cache dir ~/.scilpy/dvc-cache
dvc config cache.shared group
dvc config cache.type symlink
```


# Setup the DVC remote registry
```
dvc remote add -d scil-data ssh://<remote url>:<remote port><path to data>
```

## Create keyfile for authentication and setup on remote
```
ssh-keygen -q -f scil-data.keyfile -N "" -C "<user>@<host>"
ssh-copy-id -i scil-data.keyfile.pub <user>@<remote url>
cp scil-data.keyfile ~/.ssh/.
cp scil-data.keyfile.pub ~/.ssh/.
```

## Add local authentication
```
dvc remote modify --local scil-data user <user>
dvc remote modify --local scil-data keyfile <keyfile>
dvc remote modify --local scil-data ask_passphrase false
```

# Construct legacy scil-data local registry
```
python3 construct_dvc_store.py
dvc commit
dvc push
git add *.dvc .dvcignore *.gitignore
git commit -m "Generate legacy registry"
git push
```

# Commit config and setup to git
```
git add --all
git commit -m "Initial registry setup"
git push
```