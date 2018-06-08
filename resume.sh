#!/bin/bash

# 第1引数にTwitter API Keyのtomlファイルのパスを指定
# 第2引数に取得したいscreen_name.txtを追加
# 第3引数に出力先ディレクトリを指定
# 第4引数に最後に取得したスクリーンネームを保存するためのファイルパスを指定
# 第5引数にログファイルのパスを指定
# それぞれ相対パスでもOK

showLastLine () {
    # 第1引数はスクリーンネームが列挙されたファイル名
    # 第2引数は最後に取得したアカウント名が書かれたファイル名
    cat $1 | \
    egrep -n "^`cat $2`$" | \
    cut -d":" -f1
}

# 途中から再開するために取得すべきスクリーンネームを更新
cat $2 | tail -n +`showLastLine $2 $4` > ./screen_name_tmp.txt
./run.sh $1 ./screen_name_tmp.txt $3 $4 $5
