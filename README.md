# getTweet

# Tweetの大量収集
Tweetを取得する際に必要なこと  
つぶやきを収集するために，いくつかやらなければならないことがある．  
  
## 本ドキュメントの作成日時
20170502-20170503  
  
## 動作を検証した環境
macOS Sierra 10.12.4  
Ubuntu 16.04.2 LTS  
CentOS Linux release 7.3.1611 (Core)  
  
いずれのOSにおいても
Python 3.6.1 :: Anaconda custom (64-bit)  
Bash  
  
上記環境以外でもネットワーク環境が適切に設定されていて，Bashが使えてPython 3系で，必要なことが全てなされているのであるなら，つぶやき収集プログラムは動くはず． 
  
  
# 準備
## Python3のインストール，および依存ライブラリのインストール
各OSの手順に従ってPython3をインストールしてください．  
Ubuntu16.04の場合はデフォルトでpython3がインストールされています．  
その後  
pip3 install requests_oauthlib  
pip3 install timeout-decorator  
で必要なライブラリをインストールする．  

## zipコマンドのインストール
zipコマンドをインストールしてください  
Ubuntuなら  
sudo apt-get install zip -y  
でインストールできます．


  
## Twitter API Keyを4種類取得
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

このConsumer Key, Consumer Secret, Access Token, Access Token Secretの四つのキーをtwitter_keys.txtに上からこの順で記述する  

下記のように記述する．(無論,下記をコピペしても動かない)  
$ cat twitter_keys.txt  
aaaaaaaaaaaaaaaaaaaaa  
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb  
xxxxxxxxxxxxxxxxxxxx-ccccccccccccccccccccccccccccc  
yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy  
$  
  
これで準備完了  

# つぶやきの取得

つぶやきを収集するには下記のコマンドを実行すれば良い  
$ cat screen_name.txt | nohup ./getTweet.sh > /dev/null &  
  
このコマンドはgetTweet100000.shあるいはgetTweet3_100000.shに記述されている.  
Python3を使うためのコマンドがpython3であるなら，getTweet3_100000.shを使ってください.  
Python3を使うためのコマンドがpythonであるなら，getTweet100000.shを使ってください.  

  
収集されたつぶやきはjsonディレクトリに格納される．  
jsonディレクトリがない場合は作成してください
  
本プログラムでは下記のようなデータを標準入力としてgetTweets.pyプログラムに与えている．  
$ cat screen_name.txt | head   
yukina39  
bellydog77  
Love_McD  
mochi0world  
asako_desuyo  
yuuno_iruka712  
new_tecchan  
rutou_bot  
Arfia_demegei  
makotonanako  
  

## Pythonのログ

ログは下記のようになっている  
$ cat getTweet.log | tail  
2017-05-02 01:50:28,280-Main-DEBUG-Successfully Saved tweet of 00_kirq to ./json/00_kirq.json  
2017-05-02 01:50:29,235-Main-DEBUG-Getting tweet of 00_kmt7  
2017-05-02 01:50:29,824-Main-DEBUG-Successfully Saved tweet of 00_kmt7 to ./json/00_kmt7.json  
2017-05-02 01:50:30,526-Main-DEBUG-Getting tweet of 00_m0405  
2017-05-02 01:50:38,126-Main-DEBUG-Successfully Saved tweet of 00_m0405 to ./json/00_m0405.json  
2017-05-02 01:50:38,919-Main-DEBUG-Getting tweet of 00_magnolia  
2017-05-02 01:50:55,268-Main-DEBUG-Successfully Saved tweet of 00_magnolia to ./json/00_magnolia.json  
2017-05-02 01:50:56,394-Main-DEBUG-Getting tweet of 00_mangan  
2017-05-02 01:50:57,167-requestTweet-DEBUG-Too Many Requests  
2017-05-02 01:50:57,338-Wait-DEBUG-Wait 170.0 sec  
$   
  

下記の二行があれば正常につぶやきが取得できている  
2017-05-02 01:50:29,235-Main-DEBUG-Getting tweet of 00_kmt7  
2017-05-02 01:50:29,824-Main-DEBUG-Successfully Saved tweet of 00_kmt7 to ./json/00_kmt7.json  
  
  
下記の二行があるとき，アクセスしすぎを防ぐためにアクセスを停止している  
2017-05-02 01:50:57,167-requestTweet-DEBUG-Too Many Requests  
2017-05-02 01:50:57,338-Wait-DEBUG-Wait 170.0 sec  
  
エラーコードが401のときにはアクセスキーが間違っているか，  
あるいは取得対象アカウントが鍵垢になっていると考えられる  
-> ずっと401 error を吐いているようであれば，おそらくアクセスキーが間違ってるので直してください  

# つぶやき収集の再開
もし，途中から再開したい場合は，再開する行番号を調べる．getTweet.logの最後尾を見れば，どのアカウントのつぶやきまで収集したかわかるでしょう．  
  
例: Frk_72が何行目にあるか知りたい
$ cat screen_name.txt | tail  
FrixumPullum  
Frk_72  
Frk_ModeRed  
Frkn516  
Frn2b8iEFgXbLvL  
FroZeN246  
FroakieBot  
FrogCall13  
FrogDrop__108  
FrogKabai396  

grepの-n オプションを用いれば簡単に行数を知ることができます．
$ cat screen_name.txt | grep -n Frk_72  
99992:Frk_72  
  
上記の方法以外にVi/VimやEmacs等で検索をして，行数を表示するコマンド(機能)を使っても良いでしょう  
  

例えば，再開する行番号が100であった場合は下記のコマンドで大丈夫でしょう．  
  
cat screen_name.txt | tail -n +100 | nohup ./getTweet.sh &  
  

  
# つぶやき収集プログラムの強制終了
プログラムを強制終了したいときはpsコマンドでxargsののPIDを確認し，killコマンドでプロセスを強制終了すると良いでしょう  
実例  
あやまって二つプロセスを立ち上げてしまった場合  
$ ps  
  PID TTY          TIME CMD  
19818 pts/22   00:00:00 bash  
21161 pts/22   00:00:00 xargs  
21247 pts/22   00:00:00 xargs  
24308 pts/22   00:00:00 sh  
24310 pts/22   00:00:00 python  
24366 pts/22   00:00:00 sh  
24371 pts/22   00:00:00 python  
24443 pts/22   00:00:00 ps  
  
IDを見つけたらkillコマンド  
$ kill 21161  
$ kill 21247  
荒ぶるプロセスを鎮めることに成功したことを確認  
$ ps  
  PID TTY          TIME CMD  
19818 pts/22   00:00:00 bash  
24633 pts/22   00:00:00 ps  
しばらく待った後で，logをみると，pythonのプログラムが正常に終了していることがわかる．  
jsonファイルをjsonディレクトリの下にうまく保存したと記録されている  
$ cat getTweet.log | tail  
2017-05-02 23:26:19,365-Main-DEBUG-Getting tweet of 0000_guoyang  
2017-05-02 23:26:19,457-Main-DEBUG-Getting tweet of 0000_guoyang  
2017-05-02 23:26:25,792-Main-DEBUG-Successfully Saved tweet of 0000_guoyang to ./json/0000_guoyang.json  
2017-05-02 23:26:25,815-Main-DEBUG-Successfully Saved tweet of 0000_guoyang to ./json/0000_guoyang.json  
2017-05-02 23:26:26,202-Main-DEBUG-Getting tweet of 0000_kzkz  
2017-05-02 23:26:26,223-Main-DEBUG-Getting tweet of 0000_kzkz  
2017-05-02 23:26:27,315-Main-DEBUG-Successfully Saved tweet of 0000_kzkz to ./json/0000_kzkz.json  
2017-05-02 23:26:27,462-Main-DEBUG-Successfully Saved tweet of 0000_kzkz to ./json/0000_kzkz.json  
2017-05-02 23:26:27,675-Main-DEBUG-Getting tweet of 0000_murata_Ryo  
2017-05-02 23:26:40,467-Main-DEBUG-Successfully Saved tweet of 0000_murata_Ryo to ./json/0000_murata_Ryo.json  
  
もし，xargsのプロセスをkillしても，プログラムが動いている(ログが更新され続けている)場合は同様の手順でpythonのプロセスもkillするとよいでしょう．  
  
  
また，うまく動いている場合のpsコマンドの出力は下記の通りです．  
$ ps  
  PID TTY          TIME CMD  
19818 pts/22   00:00:00 bash  
24668 pts/22   00:00:00 cat  
24669 pts/22   00:00:00 getTweet.sh  
24670 pts/22   00:00:00 xargs  
24671 pts/22   00:00:00 sh  
24673 pts/22   00:00:00 python  
24704 pts/22   00:00:00 ps  
$   
  
  
もし万が一どうやってもプロセスが消えないのであれば再起動してください．  
その後，最後に取得したつぶやきのアカウント名をlogより調べ，再度プログラムを起動してください．  
再度プログラムを起動する際は，「つぶやき収集の再開」の項を参考にして起動してください．  
