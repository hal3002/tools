#!/bin/bash

# Requires the following in your ~/.gitconfig
# Found here: https://github.com/brauliobo/gitconfig/blob/master/configs/.gitconfig
# [alias]
#    change-commits = "!f() { VAR=$1; OLD=$2; NEW=$3; shift 3; git filter-branch --env-filter \"if [[ \\\"$`echo $VAR`\\\" = '$OLD' ]]; then export $VAR='$NEW'; fi\" $@; }; f "

author=$1
email=$2
repo=$3

if [[ -z $author ]] || [[ -z $email ]] || [[ -z $repo ]]; then
    echo "Usage: $0 <author> <email> <git.url>"
    exit 0
fi


git clone -q $repo output
cd output

for old_author in `git log | grep Author | cut -f 2 -d " " | sort | uniq`; do
    echo "$old_author -> $author"
    git change-commits GIT_AUTHOR_NAME $old_author $author -f
done

for old_email in `git log | grep Author | cut -f 3 -d " " | sort | uniq | cut -f 2 -d '<' | cut -f 1 -d '>'`; do
    echo "$old_email -> $email"
    git change-commits GIT_AUTHOR_EMAIL $old_email $email -f
done

echo "Results:"
echo "============================"
git log | grep Author | sort | uniq
