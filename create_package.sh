#!/usr/bin/env bash


VENDOR=$1
PACKAGE=$2
shift
shift

if [ ! -d "store/$VENDOR" ]
then

mkdir store/$VENDOR
cat <<- EOF > store/$VENDOR/meta.yml
description: CREATED BY NEUROGISTRY
packages:
EOF

git add store/$VENDOR/meta.yml
git commit -m "Added vendor $VENDOR"

fi

if [ -d "store/$VENDOR/$PACKAGE" ]
then
    echo "package $PACKAGE already exists for vendor $VENDOR"
    exit 1
fi

mkdir -p store/$VENDOR/$PACKAGE
for file in $@
do
    ln -s $PWD/$file store/$VENDOR/$PACKAGE/$(basename $file)
done

cat <<- EOF >> store/$VENDOR/meta.yml
  - $PACKAGE
EOF

git add store/$VENDOR/meta.yml

dvc add --no-commit store/$VENDOR/$PACKAGE
dvc commit -f store/$VENDOR/$PACKAGE
dvc push store/$VENDOR/$PACKAGE

git commit -m "Create package $PACKAGE for vendor $VENDOR"
