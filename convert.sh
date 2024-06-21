#!/usr/bin/env bash

if [[ ! -d "myenv" ]]; then
    ./init-env.sh
fi

source myenv/bin/activate
python3 convert.py