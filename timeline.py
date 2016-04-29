#!/usr/bin/env python

from __future__ import print_function

import argparse
import time

import twitter

TWITTER_CONSUMER_KEY = '<TWITTER_CONSUMER_KEY>'
TWITTER_CONSUMER_SECRET = '<TWITTER_CONSUMER_SECRET>'
TWITTER_ACCESS_TOKEN_KEY = '<TWITTER_ACCESS_TOKEN_KEY>'
TWITTER_ACCESS_TOKEN_SECRET = '<TWITTER_ACCESS_TOKEN_SECRET>'

argparser = argparse.ArgumentParser()
argparser.add_argument('SCREEN_NAME', action='store')
args = argparser.parse_args()

api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY, consumer_secret=TWITTER_CONSUMER_SECRET, access_token_key=TWITTER_ACCESS_TOKEN_KEY, access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

fpath = args.SCREEN_NAME.lstrip('@') + '.txt'

max_id = None
with open(fpath, 'wb') as f:
	for i in range(50):
		tweets = api.GetUserTimeline(screen_name=args.SCREEN_NAME, count=200, max_id=max_id)

		if len(tweets) < 1:
			break

		for status in tweets:
			try:
				text = status.text

				print(text, file=f)
				print(text)
			except:
				continue

			if not max_id:
				max_id = status.id - 1
			elif status.id < max_id:
				max_id = status.id - 1

		time.sleep(1)