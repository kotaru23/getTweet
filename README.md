# Tweet収集用のプログラム

## 環境
Python 3.6.3  
OS: CentOS7, macOS Sierra  
で確認済み  

## Proxy
プロキシの設定が必要な場合は下記のように設定をする。
下記をterminalで入力する  

```
$ export https_proxy=your.proxy.jp:8080
```

## 依存ライブラリのインストール
pip install -r requirements.txt

## Twitter API Keyの用意
twitter-api-keysディレクトリを作成し、その直下に適当な名前のファイルを作成し、
下記を記述する。
- Consumer Key
- Consumer Secret
- Access Token
- Access Token Secret

```
$ cat ./twitter-api-keys/sample-api-keys.txt
abcdefggggggggggggggggggg
Ssssssssssssssssssssssssssssssssssssssssssssssssss
777777777777777777-fffffffffffffffffffffffffffffff
Ggggggggggggggggggggggggggggggggggggggggggggg
```

## 使い方

```
echo "screen_name" | ./getTweet.py
```

または、./screen_name.txtに取得したいTwitterアカウントのScreen Nameを記述して  

```
python getTweet.py -i ./screen_name.txt
```

出力先のディレクトリはoフラグで指定できます。  

```
./getTweet.py -i ./screen_name.txt -o /path/to/output
```

取得したつぶやきデータはjson形式で保存されます。
