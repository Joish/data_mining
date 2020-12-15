import os
import json
from twitter.stream import Listener
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

        # Code to read wordlist from file
        # self.filter_list = read_filter_list_from_file()
        
        # print("FILTER LIST : {}".format(self.filter_list))
        # print(self.filter_list)
        # self.run_stream()
        # self.get_previous_tweet(from_date="2020-11-15",
        #                         to_date="2020-11-20", count_per_day=1000,
        #                         total_count=1000)

    def run_stream(self, filter_list, limit=50):
        print("STARTING TWITTER STREAM")
        print("Filter words :",filter_list)
        count = 0
        twitterStream = Stream(self.auth, Listener(limit))
        twitterStream.filter(track=filter_list, languages=["en"])
        count+=1

    def get_previous_tweet(self, filter_list, from_date, to_date, count_per_day=1000, total_count=500):

        try:
            for keyword in filter_list[:5]:
                search_words = "#{}".format(keyword)
                # search_words = "{}".format(keyword)
                # search_words = search_words.replace(" ", " #")
                print(search_words)
                file_write_count = 0

                dates = get_list_of_date_between(from_date, to_date)
                for date in dates[1:]:
                    tweets = Cursor(self.api.search,
                                    q=search_words,
                                    tweet_mode='extended',
                                    lang="en",
                                    until=date).items(count_per_day)

                    ind = 0
                    for tweet in tweets:
                        data = get_required_data(tweet._json, flag='previous')
                        # print(data)
                        if data:
                            write_file('twitter_previous', data, type='csv')
                            file_write_count += 1

                        print("COUNT : ", file_write_count)

                        if total_count == file_write_count:
                            exit()

                        # if data and ind % 100 == 0:
                        #     print(
                        #         "{} - {} of {}".format(data['date'], ind, count))
                        # ind += 1
                        # print(ind)
        except TweepError as e:
            print(e)
            # break
