#!/bin/sh

python scrape.py
git add -A
git commit -m "Update"
git push
