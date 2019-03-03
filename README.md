# Tweet収集用のプログラム

## Requirements

- Python 3.7.x
- OS: LinuxまたはmacOS
- Docker(optional)

## 依存ライブラリのインストール
```
$ pip install -r requirements.txt
```

## Twitter API Keyの用意
tomlファイルに下記を記述する。
これらは https://apps.twitter.com/ から入手できる

- Consumer Key
- Consumer Secret
- Access Token
- Access Token Secret

```
$ cat twitter-api-keys/api-keys.toml
consumerKey = "yourConsumerKey"
consumerSecret = "yourConsumerSecret"
accessToken = "yourAccessToken"
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
$ ./getTweet.py -k "Twitter API Keysを記述したtomlファイルのPath" -s "Screen Nameを記述したファイルのパス" -o "jsonファイルを出力するディレクトリ"
```

```
$ echo "screen_name" | ./getTweet.py -k "Twitter API Keysを記述したtomlファイルのPath"  -o "jsonファイルを出力するディレクトリ"
```

取得したつぶやきデータはgzip形式で保存されます。中身はjsonファイルです。

## Dockerを使う場合

- 第1引数にTwitter API Keyのtomlファイルのパスを指定
- 第2引数に取得したいscreen_name.txtを追加
- 第3引数に出力先ディレクトリを指定
```
$ docker pull geotaru/get-tweet # DockerのイメージをDocker Hubからダウンロード(最初のみ)
$ ./run.sh ./twitter-api-keys/api-keys.toml ./screen_name.txt ./output/ ./ScreenNameLatest.txt ./getTweet.log
$ ./resume.sh ./twitter-api-keys/api-keys.toml ./screen_name.txt ./output/ ./ScreenNameLatest.txt ./getTweet.log # 途中から再開する場合
```
