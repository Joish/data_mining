import os
import json
from .stream import Listener
from tweepy import Stream, OAuthHandler, API, Cursor, TweepError
from twitter.twitter_util import read_filter_list_from_file, get_required_data, write_file, get_list_of_date_between


class TwitterStream():
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET):
        self.CONSUMER_KEY = CONSUMER_KEY
        self.CONSUMER_SECRET = CONSUMER_SECRET
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.ACCESS_SECRET = ACCESS_SECRET

        self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api = API(self.auth, wait_on_rate_limit=True)

        self.filter_list = read_filter_list_from_file()
        print("FILTER LIST : {}".format(self.filter_list))

        # self.run_strem()
        self.get_previous_tweet(from_date="2020-11-18",
                                to_date="2020-11-20", count=500)

    def run_strem(self):
        print("STARTING TWITTER STREAM")

        twitterStream = Stream(self.auth, Listener())

        twitterStream.filter(track=self.filter_list, languages=["en"])

    def get_previous_tweet(self, from_date, to_date, count=1000):

        try:
            for keyword in self.filter_list[:5]:
                search_words = "#{}".format(keyword)
                # search_words = search_words.replace(" ", " #")
                print(search_words)

                dates = get_list_of_date_between(from_date, to_date)
                for date in dates[1:]:
                    tweets = Cursor(self.api.search,
                                    q=search_words,
                                    lang="en",
                                    until=date).items(count)

                    ind = 0
                    for tweet in tweets:
                        data = get_required_data(tweet._json, flag='previous')
                        # print(data['date'])
                        if data:
                            write_file('twitter_previous', data, type='csv')

                        if ind % 100 == 0:
                            print(
                                "{} - {} of {}".format(data['date'], ind, count))
                        ind += 1
        except TweepError as e:
            print(e)
            # break
