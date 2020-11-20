import json
from tweepy.streaming import StreamListener


class Listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        print(all_data)

        return True

    def on_error(self, status):
        print("SOME ERROR HAS OCCURED - {}".format(status))
