#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
実行環境: Python3.6.3
このプログラムはアカウント名(screen name)を標準入力に与えるとそのアカウントのつぶやきを過去に遡って採取します．
採取したつぶやきデータをjson形式で保存します
その中身はdictionaryを要素とするlistです．

指定したアカウントが鍵垢だったり，そもそも存在しない場合，データを取得せず異常終了します．
なおつぶやきデータ中に含まれる時刻(created_at)はUTCです．
'''

from requests_oauthlib import OAuth1Session
import json
from time import sleep, mktime
import datetime
from logging import getLogger, FileHandler, DEBUG, Formatter
from os import mkdir, listdir
from os.path import exists
from multiprocessing import Process, Queue
import codecs
import sys
from argparse import ArgumentParser

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

# 1回のリクエストで取得できるユーザのつぶやきデータの総数は200
request_maximum = '200'


def getTweet(screen_name: str, params: dict, twitter_keys: list):
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
            return None
        tweet = json.loads(res.text)
        if len(tweet) != 0:
            save_list.extend(tweet)
            params = {'screen_name': screen_name, 'count': request_maximum, 'max_id': tweet[-1]['id'] - 1}
        else:
            return save_list
    return None


def requestTweet(params: dict, twitter_keys: list):
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
                            request_maximum)
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
    if int(remaining) < int(request_maximum):
        wait(session)
    return None


def getTweetandSave(screen_name: str, save_path: str, twitter_keys: list):
    # Set Logger
    logger_gta = getLogger('getTweetandSave')
    logger_gta.setLevel(DEBUG)
    logger_gta.addHandler(handler)
    # Show twitter screen name
    logger_gta.debug('Getting tweet of ' + screen_name)
    params = {'screen_name': screen_name, 'count': request_maximum}
    save_list = getTweet(screen_name, params, twitter_keys)
    if (save_list == []) or (save_list is None):
        logger_gta.warn('Failed to get tweet of ' + screen_name)
        return None
    # TweetをJSON形式で保存する
    try:
        # code UTF-8
        f = codecs.open(save_path, 'w', 'utf-8')
        json.dump(save_list, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        f.close()
        logger_gta.debug('Successfully Saved tweet data of ' + screen_name + ' to ' + save_path)
    except ValueError:
        logger_gta.warn('failed to write json file')
        return None
    return save_path


def get_tweet_concurrent(q, save_dir: str, twitter_keys: list):
    while q.empty() is False:
        screen_name = q.get()
        save_path = save_dir + str(screen_name) + '.json'
        getTweetandSave(screen_name, save_path, twitter_keys)
    return None


def get_tweet_and_save(screen_name_list: list, save_dir: str, twitter_keys_list: list):
    # Set Logger
    logger_gts = getLogger('get_tweet_and_save')
    logger_gts.setLevel(DEBUG)
    logger_gts.addHandler(handler)
    # screen name queue
    q = Queue()
    for scn in screen_name_list:
        q.put(scn)
    jobs = []
    for tk in twitter_keys_list:
        job = Process(target=get_tweet_concurrent, args=(q, save_dir, tk))
        jobs.append(job)
        job.start()
    [j.join() for j in jobs]
    return None


def setup() -> list:
    def read_keys(key_path: str):
        with open(key_path) as f:
            lines = f.readlines()
            twitter_keys = tuple(map(lambda x: x.replace('\n', '').replace('\r', ''), lines))
        if len(tuple(twitter_keys)) != 4:
            logger_main.warn('invalid key file')
            return None
        return twitter_keys

    parser = ArgumentParser(description="Twitter REST APIを用いて、あるスクリーンネームの人の過去のつぶやきを取れるだけ収集します。")
    # determine where to save files
    parser.add_argument('-o', '--out',
                        action='store',
                        default='./collected_tweet/',
                        const='./collected_tweet/',
                        nargs='?',
                        type=str,
                        help='path to save Tweet data')
    # input file
    parser.add_argument('-i', '--inputfile',
                        action='store',
                        default='',
                        const='',
                        nargs='?',
                        type=str,
                        help='path to save Tweet data')
    args = parser.parse_args()
    save_dir = args.out
    # Set Logger
    logger_main = getLogger('setup')
    logger_main.setLevel(DEBUG)
    logger_main.addHandler(handler)
    logger_main.debug('Started to collect tweets')
    # Set Twitter API Keys
    key_dir = './twitter-api-keys/'
    if exists(key_dir):
        key_files = listdir(key_dir)
        key_list = [read_keys(key_path) for key_path in list(map(lambda x: key_dir + x, key_files)) if read_keys(key_path) is not None]
    else:
        logger_main.warn('No directory for twitter keys')
        exit(0)
    # get the text of screen name list
    try:
        # Screen nameが一列に並べられたファイルを読み込みます
        screen_name = args.inputfile
        with open(screen_name) as sf:
            sl = sf.readlines()
        screen_name_list = list(map(lambda x: x.replace('\n', '').replace('\r', ''), sl))
    except OSError:
        # screen nameを標準入力から読み込む
        logger_main.warn('screen_name.txtが存在しません。標準入力から取得します')
        screen_name = sys.stdin.readline()
        screen_name_list = [screen_name.replace("\n", "").replace("\r", "")]
    if exists(save_dir) is False:
        mkdir(save_dir)
    return [screen_name_list, save_dir, key_list]


if __name__ == '__main__':
    screen_name_list, save_dir, key_list = setup()
    get_tweet_and_save(screen_name_list, save_dir, key_list)
