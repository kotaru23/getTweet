#!/bin/bash

# 第1引数にTwitter API Keyのtomlファイルのパスを指定
# 第2引数に取得したいscreen_name.txtを追加
# 第3引数に出力先ディレクトリを指定
docker run --rm \
    -v $1:/app/key.toml \
    -v $2:/app/screen_name.txt \
    -v $3:/app/output/ \
    get-tweet
