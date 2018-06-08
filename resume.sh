#!/bin/bash

showLastLine () {
    # 第1引数はスクリーンネームが列挙されたファイル名
    # 第2引数は最後に取得したアカウント名が書かれたファイル名
    cat $1 | \
    egrep -n "^`cat $2`$" | \
    cut -d":" -f1
}


cat $2 | tail -n +`showLastLine $2 $4` > ./screen_name_tmp.txt
./run.sh $1 ./screen_name_tmp.txt $3 $4 $5
