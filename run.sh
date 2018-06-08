#!/bin/bash

function getFullPath () {
    # パスを絶対パスにする
    if [ ${1:0:1} != "/" ]; then
        # 相対パスが引数に入力されたとき(1文字目が"/"なら)
        echo `pwd`/$1
    else
        # 絶対パスが引数に入力されたとき
        echo $1
    fi
}

docker run --rm -v `getFullPath $1`:/app/key.toml -v `getFullPath $2`:/app/screen_name.txt -v `getFullPath $3`:/app/output/ geotaru/get-tweet
