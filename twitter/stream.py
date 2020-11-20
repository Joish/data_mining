import json
from tweepy.streaming import StreamListener
import os
import json
import pandas as pd


class Listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

        self.write_file(all_data, type='txt')
        # self.write_file(all_data, type='csv')

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
        # elif type == 'csv':
        #     file_path = os.path.join(cwd, "{}.csv".format(filename))
        #     df = pd.DataFrame.from_dict(content, orient="index")
        #     df.T.to_csv(file_path)
