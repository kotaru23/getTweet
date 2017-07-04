## Tweetの大量収集
Tweetを取得する際に必要なこと  
つぶやきを収集するために，いくつかやらなければならないことがある．  
  
### 本ドキュメントの作成日時
20170502-20170503  
### 修正日時
20170704  
  
### 動作を検証した環境
macOS Sierra 10.12.4, 10.12.5  
Ubuntu 16.04.2 LTS  
CentOS Linux release 7.3.1611 (Core)  
  
いずれのOSにおいても
Python 3.6.1 :: Anaconda custom (64-bit)  
Python 3.6.1
Bash  
  
上記環境以外でもネットワーク環境が適切に設定されていて，Bashが使えてPython 3系で，必要なことが全てなされているのであるなら，つぶやき収集プログラムは動くはず． 
  
  
## 準備
### Python3のインストール，および依存ライブラリのインストール
各OSの手順に従ってPython3をインストールしてください．  
Ubuntu16.04の場合はデフォルトでpython3がインストールされています．  
その後  
pip3 install requests_oauthlib  
~~pip3 install timeout-decorator~~  
で必要なライブラリをインストールする．  

~~## zipコマンドのインストール
zipコマンドをインストールしてください  
Ubuntuなら  
sudo apt-get install zip -y  
でインストールできます．~~


  
### Twitter API Keyを4種類取得
Twitter Application Managementへアクセス  
https://apps.twitter.com/  
  
Twitterのアカウントがあればそれを使ってください．なければ作成してください．  
また，アクセスキーの取得には電話番号をアカウントと紐つけることが必要です(20170502時点). 下記の操作を実行した後，電話番号をアカウントから除去しても構いません．  
  
上記のサイトの右上にある，Create New Appをクリック  
そのあと，Create an applicationという画面に遷移するので，そこで，必要事項を記入する  
Name, Description, Website, Callback URLともにデタラメで構わないが，全てに記入してください.
その後，Developer Agreementにチェックを入れ，Create your Twitter applicationをクリックする．  
全て正しく入力するとConsumer KeyとConsumer Keyが生成される．つぎに上にあるタブからKeys and Access Tokensをクリックし，そのページの下部にあるTake ActionsのCreate my access tokenをクリックする  
これで，アクセストークンが作成されたはず．  

#### twitter_keysの準備
このConsumer Key, Consumer Secret, Access Token, Access Token Secretの四つのキーをテキストファイルに上からこの順で記述する  

具体的には下記のように記述する．(無論,下記をコピペしても動かない)  
$ cat twitter_keys.txt  
aaaaaaaaaaaaaaaaaaaaa  
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb  
xxxxxxxxxxxxxxxxxxxx-ccccccccccccccccccccccccccccc  
yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy  
$  
このテキストファイルはtwitter_keysディレクトリの直下に置いてください  
  
#### screen_name.txtの配置
下記のようにscreen_name.txtに取得したいTwitterアカウントのスクリーンネームを記述してください  
これをgetTweets.pyと同じディレクトリの階層に入れてください．  
$ cat screen_name.txt | head   
hodsaf11  
heohdfaj12  
hhfasfa12  
github_daisuki12  
hara_hetta  
  

これで準備完了  

## つぶやきの取得

つぶやきを収集するには下記のコマンドを実行すれば良い  
$ python getTweets.py  

  
収集されたつぶやきはcollected_tweetディレクトリに格納される．  
collected_tweetディレクトリがなければ，自動作成されます．
  

### 本プログラムのログ

ログは下記のようになっている  
下記の二行があれば正常につぶやきが取得できている  
2017-05-02 01:50:29,235-Main-DEBUG-Getting tweet of 00_kmt7  
2017-05-02 01:50:29,824-Main-DEBUG-Successfully Saved tweet of hoge to ./json/hoge.json  
  
  
下記の二行があるとき，アクセスしすぎを防ぐためにアクセスを停止している  
2017-05-02 01:50:57,167-requestTweet-DEBUG-Too Many Requests  
2017-05-02 01:50:57,338-Wait-DEBUG-Wait 170.0 sec  
  
エラーコードが401のときにはアクセスキーが間違っているか，  
あるいは取得対象アカウントが鍵垢になっていると考えられる  
-> ずっと401 error を吐いているようであれば，おそらくアクセスキーが間違ってるので直してください  

  
## つぶやき収集プログラムの強制終了
プログラムを強制終了したいときはCtrl+CかpsコマンドでxargsののPIDを確認し，killコマンドでプロセスを強制終了すると良いでしょう．
$ ps | grep python | awk '{print $1}' | xargs kill  
(上記コマンドは本プログラム以外にpythonプログラムが動いていないということを確認してから実行してください)
