#!/bin/bash

if [ "$#" -eq 2 ]
then
	python3 20171091_1.py $1 $2 > 20171091_1.txt

elif [ "$#" -eq 1 ]
then
	python3 20171091_2.py $1 > 20171091_2.txt

else
    echo "Input format for 1st case: bash <input file name> <X>"
    echo "Input format for 2nd case: bash <input file name>"
fi
