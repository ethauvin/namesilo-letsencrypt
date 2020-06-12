#!/bin/bash

RELEASE=release

if [ $# != 1 ];
then
	echo "Usage: $(basename "$0") <version>"
	exit 2
else
    if ! [ -d "$RELEASE" ]
    then
        mkdir "$RELEASE"
    fi
    PROJECT=$(basename "$(pwd)")
    DIR="${PROJECT}-${1}"
    mkdir "$DIR"
    cp ./*.py ./*.md ./*.txt "$DIR"
    dos2unix "$DIR"/*.*
    touch "$DIR" "$DIR"/*.*
    tar -czvf "${RELEASE}/${DIR}.tar.gz" "$DIR"
    zip --to-crlf -r "${RELEASE}/${DIR}.zip" "$DIR"
    touch "$RELEASE"/*.*
    rm -rf "${DIR}"
fi
