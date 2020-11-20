import os
from .stream import Listener


class FacebookStream():
    def __init__(self, ACCESS_TOKEN):
        self.ACCESS_TOKEN = ACCESS_TOKEN

        self.run()

    def get_filter_list(self):
        cwd = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(cwd, "filter_list.txt")
        f = open(file_path, "r")
        filter_list = f.read().split("\n")
        filter_list = [_.replace(" ", '') for _ in filter_list if _]
        return filter_list

    def run(self):
        print("STARTING FACEBOOK STREAM")
