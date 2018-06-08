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

# 第1引数にTwitter API Keyのtomlファイルのパスを指定
# 第2引数に取得したいscreen_name.txtを追加
# 第3引数に出力先ディレクトリを指定
# 第4引数に最後に取得したスクリーンネームを保存するためのファイルパスを指定
# 第5引数にログファイルのパスを指定
# それぞれ相対パスでもOK
docker run --rm -v `getFullPath $1`:/app/key.toml -v `getFullPath $2`:/app/screen_name.txt -v `getFullPath $3`:/app/output/ -v `getFullPath $4`:/app/ScreenNameLatest.txt -v `getFullPath $5`:/app/getTweet.log geotaru/get-tweet
