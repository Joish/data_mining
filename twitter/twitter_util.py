import os
import re
import csv
import json
from datetime import date, timedelta


def write_file(filename, content, type='txt'):
    # filename = 'twitter_stream'
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


def read_filter_list_from_file():
    cwd = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(cwd, "filter_list.txt")
    f = open(file_path, "r")
    filter_list = f.read().split("\n")
    filter_list = [_.strip() for _ in filter_list if _]
    return filter_list


def get_required_data(all_data, flag='stream'):
    data = {}

    if flag == 'stream':
        condition = 'user' in all_data and 'retweeted_status' in all_data \
            and 'extended_tweet' in all_data['retweeted_status'] and\
            all_data['lang'] == 'en' and 'full_text' in all_data['retweeted_status']['extended_tweet']

        if condition:
            text = all_data['retweeted_status']['extended_tweet']['full_text']
            hashtag = [_['text'] for _ in all_data['retweeted_status']
                       ['extended_tweet']['entities'].get('hashtags', [])]
    else:
        condition = 'user' in all_data and 'retweeted_status' in all_data \
            and 'full_text' in all_data['retweeted_status'] and \
                'entities' in all_data and all_data['lang'] == 'en'

        if condition:
            text = all_data['retweeted_status']['full_text']
            hashtag = [_['text']
                       for _ in all_data['entities'].get('hashtags', [])]

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
            'text': apply_text_filters(text),
            'hashtag': hashtag,
            'source': handle_html_tags(all_data.get('source', 'None')),
            'is_retweet': all_data.get('retweeted', 'None')
        }

    return data


def handle_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def apply_text_filters(text):

    text = re.sub(
        r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", text)
    text = text.encode('ascii', errors='ignore').decode('utf-8')

    return text


def get_list_of_date_between(start, end):
    start_date_split = start.split("-")
    end_date_split = end.split("-")

    sdate = date(int(start_date_split[0]), int(start_date_split[1]),
                 int(start_date_split[2]))   # start date
    edate = date(int(end_date_split[0]), int(end_date_split[1]),
                 int(end_date_split[2]))   # end date

    edate = edate + timedelta(days=1)

    delta = edate - sdate       # as timedelta

    date_list = [str(sdate + timedelta(days=i)) for i in range(delta.days + 1)]
    return date_list
