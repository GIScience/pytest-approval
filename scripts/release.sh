#!/bin/sh

set -e

if [ $# -eq 0 ]; then
    echo "Please supply one of the following values as argument:"
    echo "major, minor, patch, stable, alpha, beta, rc, post, dev"
    exit
fi

git switch main

uv version --bump "$1"

$EDITOR CHANGELOG.md

git add -p pyproject.toml CHANGELOG.md
git add uv.lock

git commit -m "$1"
git push
git tag "$1" -m "$1"
git push origin "$1"
