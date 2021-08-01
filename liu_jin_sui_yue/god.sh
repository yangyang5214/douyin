#!/bin/bash

n=$1

python3.9 merge_ljsy.py $n $2

python3.9 main.py -n $n -m split
python3.9 main.py -n $n -m glance
python3.9 main.py -n $n -m merge
