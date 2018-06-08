#!/bin/bash

showLastLine () {
    cat $1 | egrep -n "^`cat ./ScreenNameLatest.txt `$" | cut -d":" -f1
}

cat $1 | tail -n +`showLastLine $1`
