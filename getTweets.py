# -*- coding: utf-8 -*-
'''
実行環境: Python3.6.1
このプログラムはアカウント名(screen name)を標準入力に与えるとそのアカウントのつぶやきを過去に遡って採取します．
採取したつぶやきデータをjson形式で本プログラムのあるディレクトリのjsonフォルダに保存をします
その中身はdictionaryを要素とするlistです．

指定したアカウントが鍵垢だったり，そもそも存在しない場合，データを取得せず異常終了します．
なおつぶやきデータ中に含まれる時刻(created_at)はUTCです．
'''

from requests_oauthlib import OAuth1Session
import json
from time import sleep, mktime
import datetime
from sys import exit
from logging import getLogger, FileHandler, DEBUG, Formatter
from timeout_decorator import timeout

'''
Twitterのスクリーンネーム(@につづく名前)，取得したTwitterのつぶやきデータを保存するリスト，リクエストを投げる際に必要なパラメータを
引数にとる．
返り値はつぶやきデータの入ったリストである．
ネットワークに繋がっていなかったり異常がある場合は強制終了する
'''

TWITTER_CONSUMER_KEY = ""
TWITTER_CONSUMER_SECRET = ""
TWITTER_ACCESS_TOKEN_KEY = ""
TWITTER_ACCESS_TOKEN_SECRET = ""

# Logger settings
handler = FileHandler('getTweet.log', mode='a', encoding='utf_8')
handler.setLevel(DEBUG)
formatter = Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
handler.setFormatter(formatter)

# 1回のリクエストで取得できるユーザのつぶやきデータの総数は200
request_maximum = '200'


def getTweet(screen_name, save_list, params):
    # Set Logger
    logger_getTweet = getLogger('getTweet')
    logger_getTweet.setLevel(DEBUG)
    logger_getTweet.addHandler(handler)
    res = requestTweet(params)
    if res is None:
        return None
    tweet = json.loads(res.text)
    save_list.extend(tweet)
    # API上限に達するまで取得し続ける．API上限に達すると配列tweetの長さが0になる
    if len(tweet) != 0:
        params = {'screen_name': screen_name, 'count': request_maximum, 'max_id': tweet[-1]['id'] - 1}
        save_list = getTweet(screen_name, save_list, params)
    return save_list


def requestTweet(params):
    # Set Logger
    logger_request = getLogger('requestTweet')
    logger_request.setLevel(DEBUG)
    logger_request.addHandler(handler)
    # Start Session
    session = OAuth1Session(TWITTER_CONSUMER_KEY,
                            TWITTER_CONSUMER_SECRET,
                            TWITTER_ACCESS_TOKEN_KEY,
                            TWITTER_ACCESS_TOKEN_SECRET,
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
        res = requestTweet(params)
        return res
    if status == 404:
        logger_request.warn('Screen name: ' + str(params['screen_name']) + ' was NOT FOUND')
        return None
    if status == 429:
        logger_request.debug('Too Many Requests')
        wait(session)
        logger_request.debug('Restart')
        res = requestTweet(params)
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


@timeout(900)
def Main():
    # Set Logger
    logger_main = getLogger('Main')
    logger_main.setLevel(DEBUG)
    logger_main.addHandler(handler)
    with open('twitter_keys.txt') as f:
        lines = f.readlines()
        keys = list(map(lambda x: x.replace('\n', ''), lines))
        global TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN_KEY, TWITTER_ACCESS_TOKEN_SECRET
        TWITTER_CONSUMER_KEY = keys[0]
        TWITTER_CONSUMER_SECRET = keys[1]
        TWITTER_ACCESS_TOKEN_KEY = keys[2]
        TWITTER_ACCESS_TOKEN_SECRET = keys[3]

    # get std input
    screen_name = input()
    # Show twitter screen name
    logger_main.debug('Getting tweet of ' + screen_name)
    params = {'screen_name': screen_name, 'count': request_maximum}
    save_list = []
    save_list = getTweet(screen_name, save_list, params)
    if (save_list == []) or (save_list is None):
        logger_main.warn('Failed to get tweet of ' + screen_name)
        exit(1)
    try:
        f = open('./json/' + str(screen_name) + '.json', 'w')
        json.dump(save_list, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    except ValueError:
        logger_main.warn('failed to write json file')
        exit(1)
    except OSError:
        logger_main.warn('could not open file.')
        exit(1)
    finally:
        f.close()
        logger_main.debug('Successfully Saved tweet of ' + screen_name + ' to ./json/' + screen_name + '.json')
        exit(0)


if __name__ == '__main__':
    logger_timeout = getLogger('global')
    logger_timeout.setLevel(DEBUG)
    logger_timeout.addHandler(handler)
    from timeout_decorator import TimeoutError
    try:
        Main()
    except TimeoutError:
        logger_timeout.warn('TIME OUT')
        exit(1)
