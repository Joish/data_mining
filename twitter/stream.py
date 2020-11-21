import json
from tweepy.streaming import StreamListener
import os
import json
import re
import csv


class Listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

        condition = 'user' in all_data.keys() and 'retweeted_status' in all_data.keys(
        ) and 'extended_tweet' in all_data['retweeted_status'] and all_data['lang'] == 'en'
        if condition:
            data = {
                'user_name': all_data['user'].get('name', 'None'),
                'user_location': all_data['user'].get('location', 'None'),
                'user_description': all_data['user'].get('description', 'None'),
                'user_created': all_data['user'].get('created_at', 'None'),
                'user_followers': all_data['user'].get('followers_count', 'None'),
                'user_friends': all_data['user'].get('friends_count', 'None'),
                'user_favorities': all_data['user'].get('favourites_count', 'None'),
                'user_verified': all_data['user'].get('verified', 'None'),
                'date': all_data.get('created_at', 'None'),
                # 'text': all_data['text'],
                'text': all_data['retweeted_status']['extended_tweet'].get('full_text', 'None'),
                # 'hashtag': all_data['entities'].get('hashtags', []),
                'hashtag': [_['text'] for _ in all_data['retweeted_status']['extended_tweet']['entities'].get('hashtags', [])],
                'source': self.handle_html_tags(all_data.get('source', 'None')),
                'is_retweet': all_data.get('retweeted', 'None')
            }

            self.write_file(data, type='csv')
            # print(all_data)
            # exit()

        return True

    def on_error(self, status):
        print("SOME ERROR HAS OCCURED - {}".format(status))

    def write_file(self, content, type='txt'):
        filename = 'twitter'
        cwd = os.path.dirname(os.path.realpath(__file__))
        if type == 'txt':
            file_path = os.path.join(cwd, "{}.txt".format(filename))
            f = open(file_path, "a")
            f.write(json.dumps(content))
            f.write("\n")
            f.close()
        elif type == 'csv':
            file_path = os.path.join(cwd, "{}.csv".format(filename))
            with open(file_path, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=content.keys())
                writer.writerows([content])

    def handle_html_tags(self, data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)
