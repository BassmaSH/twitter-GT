import logging
import sys
import time

from twitter import *

import config
import pTweets

sys.path.append(".")

twitter = Twitter(auth=OAuth(config.access_key,
                             config.access_secret,
                             config.consumer_key,
                             config.consumer_secret))


def tweet_url(t):
    return "https://twitter.com/%s/status/%s" % (t['user']['screen_name'], t['id'])


def get_replies(tweet, n):
    user = tweet['user']['screen_name']
    tweet_id = tweet['id']
    max_id = None
    logging.info("looking for replies to: %s" % tweet_url(tweet))
    q = ("to:%s" % user).encode("utf-8", errors='ignore')
    R = dict()
    print('q', q)
    replies = []
    i = 0
    while len(R) <= n and i <= 10:
        print(len(replies))
        try:
            r = twitter.search.tweets(q=q, since_id=tweet_id, max_id=max_id, count=100)
            replies += r['statuses']
            for reply in replies:
                if reply['in_reply_to_status_id'] == int(tweet_id):
                    # print((reply['in_reply_to_status_id']), int(tweet_id))
                    R[reply['id']] = [reply]
            i += 1
        except TwitterError as e:
            logging.error("caught twitter api error: %s", e)
            time.sleep(60)
            continue
    for id in R.keys():
        if R[id][0]['retweet_count'] + R[id][0]['favorite_count'] >= 1:
            print('YES')
            rR = get_replies(R[id][0], int(n / 2))
            for idr in rR.keys():
                R[id].append(rR[idr])
    return R


file = open('pReplies.py', 'w')
L = []
tweet = pTweets.data[2]
R = get_replies(tweet, 10)

file.write('data = {}'.format(R))
file.close()
