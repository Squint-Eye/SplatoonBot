#!/bin/bash
root=$(pwd)
export PYTHONIOENCODING=utf8
echo 'Checking Dependencies...'
python3 -m pip install --user --upgrade -r requirements.txt --quiet
echo 'Loading Bot...'
cd "$root/bot"
python3 ./main.py