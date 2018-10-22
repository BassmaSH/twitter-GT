import random
import sys

from twitter import *

import config
import get_trends

sys.path.append(".")

twitter = Twitter(auth=OAuth(config.access_key,
                             config.access_secret,
                             config.consumer_key,
                             config.consumer_secret))
Topics = []
for el in get_trends.load_obj('trending')['title']:
    Topics.append(el)

q = random.choice(Topics)
query1 = twitter.search.tweets(q=q, count=100, result_type="popular")
query2 = twitter.search.tweets(q=q, count=100, result_type="recent")

print("Search complete (%.3f seconds). %s popular reuslts found" % (
    query1["search_metadata"]["completed_in"], len(query1["statuses"])))

print("Search complete (%.3f seconds). %s recent reuslts found" % (
    query2["search_metadata"]["completed_in"], len(query2["statuses"])))

L1 = []
L2 = []
for result in query1["statuses"]:
    if ("media" in result["entities"]) & (len(result["entities"]["urls"]) != 0):
        L1.append(result)
        encoded = ("(%s) @%s %s (type: %s) (retweets: %s, favs: %s) %s" % (
            result["created_at"], result["user"]["screen_name"], result["text"], result["metadata"]["result_type"],
            result["retweet_count"], result["favorite_count"], result["entities"]["media"][0]["media_url"])).encode(
            "utf-8",
            errors='ignore')
        print(encoded)
    elif len(result["entities"]["urls"]) != 0:
        L1.append(result)
        encoded = ("(%s) @%s %s  (type: %s) (retweets: %s, favs: %s)" % (
            result["created_at"], result["user"]["screen_name"], result["text"], result["metadata"]["result_type"],
            result["retweet_count"], result["favorite_count"])).encode("utf-8", errors='ignore')
        print(encoded)

for result in query2["statuses"]:
    if ("media" in result["entities"]) & (len(result["entities"]["urls"]) != 0):
        L2.append(result)
        encoded = ("(%s) @%s %s (type: %s) (retweets: %s, favs: %s) %s" % (
            result["created_at"], result["user"]["screen_name"], result["text"], result["metadata"]["result_type"],
            result["retweet_count"], result["favorite_count"], result["entities"]["media"][0]["media_url"])).encode(
            "utf-8",
            errors='ignore')
        print(encoded)
    elif len(result["entities"]["urls"]) != 0:
        L2.append(result)
        encoded = ("(%s) @%s %s  (type: %s) (retweets: %s, favs: %s)" % (
            result["created_at"], result["user"]["screen_name"], result["text"], result["metadata"]["result_type"],
            result["retweet_count"], result["favorite_count"])).encode("utf-8", errors='ignore')
        print(encoded)

file = open('pTweets.py', 'a')
file.write('data = {}'.format(L1))
file.close()
file = open('rTweets.py', 'a')
file.write('data = {}'.format(L2))
file.close()
