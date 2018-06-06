# Tweet収集用のプログラム

## Requirements

- Python 3.6.x  
- OS: LinuxまたはmacOS
- pipenv


## Proxy
プロキシの設定ができていないと大学内からTwitter APIを使うことができない。  
下記をterminalで入力すること  

```
$ export https_proxy=proxy.uec.ac.jp:8080
```

## 依存ライブラリのインストール
pip install -r requirements.txt

## Twitter API Keyの用意
tomlファイルに下記を記述する。
- Consumer Key
- Consumer Secret
- Access Token
- Access Token Secret

```
$ cat twitter-api-keys/api-keys.toml
consumerKey = "yourConsumerKey"
consumerSecret = "yourConsumerSecret"
accessToken ="yourAccessToken"
accessTokenSecret = "yourAccessTokenSecret"
```

## 使い方

```
$ ./getTweet.py --help
Usage: getTweet.py [OPTIONS]

Options:
  -k, --key TEXT               Twitter API Keysを記述したtomlファイルのPath
  -s, --screen_name_list TEXT  Screen Nameが記述されたファイルのパス
  -o, --output TEXT            出力のjsonファイルを置くパス
  --help                       Show this message and exit.
```

## Example

```
./getTweet.py -k "Twitter API Keysを記述したtomlファイルのPath" -s "Screen Nameを記述したファイルのパス" -o "jsonファイルを出力するディレクトリ"
```

```
echo "screen_name" | ./getTweet.py -k "Twitter API Keysを記述したtomlファイルのPath"  -o "jsonファイルを出力するディレクトリ"
```

取得したつぶやきデータはjson形式で保存されます。
