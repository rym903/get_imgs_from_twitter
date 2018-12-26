import csv
import os
import re
import tweepy
import lxml.html

#from bs4 import BeautifulSoup
from dotenv import load_dotenv
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

import storage

def download_image(url, dst_path):
    try:
        data = urlopen(url)
#        with open(dst_path, mode="wb") as f:
#            f.write(data.read())
        storage.upload_image_file(data, dst_path)
    except URLError as e:
        print(e)

def get_img_path_and_name_from_url(url, tweet, imgs_cnt): 
    #url = match.groups(1)[0]
    #print("url = {}".format(url))
    tree = lxml.html.parse(urlopen(url))
    img_html = tree.getroot()
    try:
        img_div = img_html.xpath("//div[@class='AdaptiveMedia-photoContainer js-adaptive-photo ']")[0]
    except IndexError:
        return "", ""
    img_url = img_div.get("data-image-url")
    #print(img_url)
    ext = re.search("\.([^\.]*)$", img_url)
    ext = ext.groups(1)[0]
    img_name = str(tweet[0]) + "-" + tweet[3] + "." + ext
    #print("img_name = {}".format(img_name))
    return img_url, img_name

load_dotenv()
consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv("API_SECRET_KEY")
access_key = os.getenv("ACCESS_TOKEN")
access_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#ツイート取得
tweet_data = []
account_name = "xnQyi504ZOpbrsy"
account_name = "creantics"
for tweet in \
    api.user_timeline(screen_name=account_name, count=200, tweet_mode="extended"):
#    tweepy.Cursor(api.user_timeline,screen_name = account_name,exclude_replies = True).items():
#        status = api.get_status(tweet.id)
        tweet_data.append([
        tweet.id,
        tweet.created_at,
        tweet.full_text.replace('\n',''),
        tweet.user.screen_name
#        tweet.favorite_count,
#        status.text,
#        tweet.retweet_count
        ])
#        print(status.text)


#csv出力
#with open('tweets_20170805.csv', 'w',newline='',encoding='utf-8') as f:
#    writer = csv.writer(f, lineterminator='\n')
#    writer.writerow(["id","created_at","text","full_text"])
#    writer.writerows(tweet_data)
#pass

#個々のツイートからimg_urlを取得
imgs_cnt = 0
for tweet in tweet_data:
    tweet_honbun = tweet[2]
    match = re.search("(https://t\.co/.{10})", tweet_honbun)
    if match:
        urls = match.groups(1)
        for url in urls:
            print("url={}".format(url))
            try:
                img_url, img_name = get_img_path_and_name_from_url(url, tweet, imgs_cnt)
                if img_url != "":
                    download_image(img_url, img_name)
                    imgs_cnt += 1
            except (UnicodeEncodeError, HTTPError):
                continue

print("imgs_cnt = {}".format(imgs_cnt))
