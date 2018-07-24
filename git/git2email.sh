#!/bin/bash

if [ -z $1 ]; then
    echo "Usage: $0 <repo.url>"
    exit 0
fi

if [ -d output ]; then
    echo output path already exists.  Remove it to continue.
    exit 0
fi

git clone -q $1 output
cd output
git log | grep Author | sort | uniq
cd ..
rm -rf output
