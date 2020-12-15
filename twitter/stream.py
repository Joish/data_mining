import json
from tweepy.streaming import StreamListener
from twitter.twitter_util import write_file, handle_html_tags, get_required_data


class Listener(StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)

        data = get_required_data(all_data)

        if data:
            write_file('twitter_stream', data, type='csv')
            self.rows+=1
        # print(all_data)
        # exit()
    
        return True

    def on_error(self, status):
        print("SOME ERROR HAS OCCURED - {}".format(status))
