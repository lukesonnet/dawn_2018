#!/bin/sh

python scrape.py
git diff dawn_unofficial.csv
git add -A
git commit -m "Update"
git push
