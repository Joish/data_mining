import json
from tweepy.streaming import StreamListener
from twitter.twitter_util import write_file, handle_html_tags, get_required_data


class Listener(StreamListener):
    def __init__(self,limit):
        self.cap = limit
        
    def on_data(self, data):
        all_data = json.loads(data)

        data = get_required_data(all_data)

        if data:
            if write_file('twitter_stream', data, self.cap, type='csv'):
                return False
    
        return True

    def on_error(self, status):
        print("SOME ERROR HAS OCCURED - {}".format(status))
