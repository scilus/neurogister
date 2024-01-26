# Setup the DVC local registry
```
dvc init
dvc cache dir ~/.neurogister/dvc-cache
dvc config cache.shared group
dvc config cache.type symlink
```


# Setup the DVC remote registry
```
dvc remote add -d neurogister ssh://<remote url>:<remote port><path to data>
```

## Create keyfile for authentication and setup on remote
```
ssh-keygen -q -f neurogister.keyfile -N "" -C "<user>@<host>"
ssh-copy-id -i neurogister.keyfile.pub <user>@<remote url>
cp neurogister.keyfile ~/.ssh/.
cp neurogister.keyfile.pub ~/.ssh/.
```

## Add local authentication
```
dvc remote modify --local neurogister user <user>
dvc remote modify --local neurogister keyfile <keyfile>
dvc remote modify --local neurogister ask_passphrase false
```

# Construct legacy Scilpy local registry (inside hatch env)
```
neuro_port_legacy_scilpy.py <gdrive listing>
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

# Add new data to dvc
- Add your datasets inside data/
```
dvc add .
dvc commit
dvc push
git add --all
git commit -m "<data message>"
git push
```

# Create a new package from existing data
```
neuro_create_package.py <package name> <files in data>
```