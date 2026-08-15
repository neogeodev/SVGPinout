#!/usr/bin/env sh
#
if ! command -v inkscape >/dev/null 2>&1 ; then
    echo "You need to install the inkscape package!"
    exit 1
fi

if [ ! -d svg ]; then
    echo "svg folder does not exist!"
    exit 2
fi

if [ ! "$(ls -A svg)" ]; then
    echo "'svg' folder is empty, nothing to do!"
    exit 3
fi

if [ ! -d png ]; then
    echo "Creating png folder"
    mkdir png
fi

for f in svg/*.svg
do
    inkscape --export-background-opacity=0 \
        --export-type=PNG \
        --export-filename=png/$(basename $f .svg) "$f"
done
