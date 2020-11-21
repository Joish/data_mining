import os
from .stream import Listener
from tweepy import Stream
from tweepy import OAuthHandler


class TwitterStream():
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET):
        self.CONSUMER_KEY = CONSUMER_KEY
        self.CONSUMER_SECRET = CONSUMER_SECRET
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.ACCESS_SECRET = ACCESS_SECRET

        self.run()

    def get_filter_list(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(cwd, "filter_list.txt")
        f = open(file_path, "r")
        filter_list = f.read().split("\n")
        filter_list = [_.replace(" ", '') for _ in filter_list if _]
        return filter_list

    def run(self):
        print("STARTING TWITTER STREAM")

        auth = OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_SECRET)

        twitterStream = Stream(auth, Listener())

        filter_list = self.get_filter_list()
        print("FILTER LIST : {}".format(filter_list))

        twitterStream.filter(track=filter_list, languages=["en"])
