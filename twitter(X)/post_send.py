from VersaLog import *
from .eew import EEW
from dotenv import load_dotenv

import time
import os
import tweepy



#secretsで設定した値をとる
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

#オブジェクト作成
client = tweepy.Client(
	consumer_key = CONSUMER_KEY,
	consumer_secret = CONSUMER_SECRET,
	access_token = ACCESS_TOKEN,
	access_token_secret = ACCESS_SECRET
)


def sendpost():
    eew_instance = EEW(api="https://api.p2pquake.net/v2/history?codes=551&limit=1")
    last_eq_id   = None

    while True:
        mess, eq_id = eew_instance.Get()
        if mess and eq_id != last_eq_id:
            client.create_tweet(text=f'{mess}')
            last_eq_id = eq_id
            
            return True, "ポストしました"
        else:
            pass
        
        time.sleep(5)