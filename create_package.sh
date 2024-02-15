#!/usr/bin/env bash


VENDOR=$1
PACKAGE=$2
shift
shift

if [ ! -d "store/$VENDOR" ]
then

mkdir store/$VENDOR
cat <<- EOF > store/$VENDOR/README.md
CREATED BY NEUROGISTRY
EOF

git add store/${VENDOR}/README.md
git commit -m "Neurogister added $VENDOR"

fi

if [ -d "store/$VENDOR/$PACKAGE" ]
then
    echo "package $PACKAGE already exists for vendor $VENDOR"
    exit 1
fi

mkdir -p store/$VENDOR/$PACKAGE
for file in $@
do
    ln -s $file store/$VENDOR/$PACKAGE/$(basename $file)
done

dvc add --no-commit store/$VENDOR/$PACKAGE
#dvc commit -f store/$VENDOR/$PACKAGE
#dvc push store/$VENDOR/$PACKAGE
