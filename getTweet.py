#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
このプログラムはアカウント名(screen name)を標準入力に与えるとそのアカウントのつぶやきを過去に遡って採取します．
その中身はdictionaryを要素とするlistです．

指定したアカウントが鍵垢だったり，そもそも存在しない場合，データを取得せず異常終了します．
なおつぶやきデータ中に含まれる時刻(created_at)はUTCです．
'''

import click
import toml
from requests_oauthlib import OAuth1Session
import json
from time import sleep, mktime
import datetime
from logging import getLogger, FileHandler, DEBUG, Formatter
from os import mkdir, listdir
from os.path import exists
import codecs
import sys
import gzip

'''
Twitterのスクリーンネーム(@につづく名前)，取得したTwitterのつぶやきデータを保存するリスト，リクエストを投げる際に必要なパラメータを
引数にとる．
返り値はつぶやきデータの入ったリストである．
ネットワークに繋がっていなかったり異常がある場合は強制終了する
'''


# Logger settings
handler = FileHandler('getTweet.log', mode='a', encoding='utf_8')
handler.setLevel(DEBUG)
formatter = Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
handler.setFormatter(formatter)


def getTweet(screen_name: str, params: dict, twitter_keys: list):
    """
    過去に遡ってツイートを取得する
    """
    # Set Logger
    logger_getTweet = getLogger('getTweet')
    logger_getTweet.setLevel(DEBUG)
    logger_getTweet.addHandler(handler)
    # initialize the list to save tweets
    save_list = []
    # API上限に達するまで取得し続ける．API上限に達すると配列tweetの長さが0に
    # 200 tweets per 1 loop
    for i in range(20):
        res = requestTweet(params, twitter_keys)
        if res is None:
            # つぶやき収集失敗
            return None
        tweet = json.loads(res.text)
        if len(tweet) != 0:
            save_list.extend(tweet)
            # 1回のリクエストで取得できるユーザのつぶやきデータの総数は200
            params = {'screen_name': screen_name, 'count': '200', 'max_id': tweet[-1]['id'] - 1}
        else:
            return save_list
    return None


def requestTweet(params: dict, twitter_keys: list):
    """
    APIへのアクセスを制御する
    """
    # Set Logger
    logger_request = getLogger('requestTweet')
    logger_request.setLevel(DEBUG)
    logger_request.addHandler(handler)
    twitter_consumer_key, twitter_consumer_secret, twitter_access_token_key, twitter_access_token_secret = twitter_keys
    # Start Session
    session = OAuth1Session(twitter_consumer_key,
                            twitter_consumer_secret,
                            twitter_access_token_key,
                            twitter_access_token_secret,
                            '200')
    # このURLで特定のユーザのつぶやきを取得することができる
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    # データを取得
    res = session.get(url, params=params)
    # エラー対策
    status = res.status_code
    if status == 200:
        return res
    if status == 503:
        logger_request.debug('short sleep: wait 60 sec')
        sleep(60)
        logger_request.debug('restart')
        res = requestTweet(params, twitter_keys)
        return res
    if status == 404:
        logger_request.warn('Screen name: ' + str(params['screen_name']) + ' was NOT FOUND')
        return None
    if status == 429:
        logger_request.debug('Too Many Requests')
        wait(session)
        logger_request.debug('Restart')
        res = requestTweet(params, twitter_keys)
        return res
    else:
        logger_request.warn('Error   account: ' + str(params['screen_name']) + ' status = ' + str(status))
        return None


def wait(session):
    """
    APIへのアクセス過多を防ぐためにプログラムを停止する時間を求め、その時間だけsleepする
    """
    # Set Logger
    logger_wait = getLogger('Wait')
    logger_wait.setLevel(DEBUG)
    logger_wait.addHandler(handler)
    # Too much requests!! Wait until the access limit is reset.
    check_time_url = 'https://api.twitter.com/1.1/application/rate_limit_status.json'
    ctu = session.get(check_time_url)
    ctu_json = json.loads(ctu.text)
    reset = ctu_json['resources']['statuses']['/statuses/user_timeline']['reset'] + 1
    wait_time = reset - mktime(datetime.datetime.now().timetuple()) + 20
    if wait_time > 0:
        logger_wait.debug('Wait ' + str(wait_time) + ' seconds')
        sleep(wait_time)
    else:
        logger_wait.warn('Wait 120 seconds. The watch of this computer may be wrong.')
        # If wait_time is negative, the watch may be some time fast.
        # To avoid some error, wait 120 seconds for the moment.
        sleep(120)
    restart = session.get(check_time_url)
    restart_json = json.loads(restart.text)
    remaining = restart_json['resources']['statuses']['/statuses/user_timeline']['remaining']
    if int(remaining) < int('200'):
        wait(session)
    return None


def save_tweet(screen_name: str, save_path: str, twitter_keys: list):
    """
    取得したつぶやきを、gzipで圧縮し保存
    """
    # Set Logger
    logger_gta = getLogger('save_tweet')
    logger_gta.setLevel(DEBUG)
    logger_gta.addHandler(handler)
    # Show twitter screen name
    logger_gta.debug('Getting tweet of ' + screen_name)
    params = {'screen_name': screen_name, 'count': '200'}
    # つぶやきの取得
    save_list = getTweet(screen_name, params, twitter_keys)
    if (save_list == []) or (save_list is None):
        logger_gta.warn('Failed to get tweet of ' + screen_name)
        return None
    # TweetをJSON形式で保存する
    try:
        # jsonファイルをgzip形式で圧縮し保存
        with gzip.GzipFile(save_path + ".gz", "w") as gf:
            json_str = json.dumps(save_list, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': ')) + "\n"
            json_bytes = json_str.encode("utf-8")
            gf.write(json_bytes)
        logger_gta.debug('Successfully Saved tweet data of ' + screen_name + ' to ' + save_path)
    except ValueError:
        logger_gta.warn('failed to write json file')
        return None
    return save_path


@click.command()
@click.option("--key", "-k", help="Twitter API Keysを記述したtomlファイルのPath")
@click.option("--screen_name_list", "-s", help="Screen Nameが記述されたファイルのパス")
@click.option("--output", "-o", help="出力のjsonファイルを置くパス")
def main(key: str, screen_name_list: str, output: str) -> list:
    """
    Twitter APIの鍵やscreen nameの読み込みを行う
    screen nameそれぞれに対してつぶやきを取得し保存する
    """
    # Set Logger
    logger_main = getLogger('setup')
    logger_main.setLevel(DEBUG)
    logger_main.addHandler(handler)
    logger_main.debug('Started to collect tweets')
    # get Twitter API Keys
    with open(key) as f:
        twitter_toml = toml.load(f)
    # Twitterの鍵を読み込み
    twitter_keys = [twitter_toml["consumerKey"], twitter_toml["consumerSecret"], twitter_toml["accessToken"], twitter_toml["accessTokenSecret"]]
    # get the text of screen name list
    if screen_name_list is not None:
        with open(screen_name_list) as sf:
            sl = sf.readlines()
        screen_names = list(map(lambda x: x.replace('\n', '').replace('\r', ''), sl))
    else:
        # screen nameを標準入力から読み込む
        logger_main.warn('screen_name.txtが存在しません。標準入力から取得します')
        screen_name = sys.stdin.readline()
        screen_names = [screen_name.replace("\n", "").replace("\r", "")]
    # 出力するディレクトリが存在しなければ作成
    if exists(output) is False:
        mkdir(output)
    for sn in screen_names:
        jsonfilename = output + "/" + sn + ".json"
        save_tweet(sn, jsonfilename, twitter_keys)
        # 最後に取得してアカウントを保存
        with open("./ScreenNameLatest.txt", "w") as f:
            f.write(sn)
    return None


if __name__ == '__main__':
    main()
