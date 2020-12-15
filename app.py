from config import TwitterCredentials, FacebookCredentials
from twitter.main import TwitterStream
from flask import Flask,render_template,request,send_file
twc = TwitterCredentials()

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getStream')
def getStream():
    """
    GET REQUEST FORMAT :

    getStream?word=covid&limit=5000

    """
    search_words=[]
    search_words,append(request.args.get('word',None,str))
    limit = request.args.get('limit',500)
    tws = TwitterStream(
        CONSUMER_KEY=twc.CONSUMER_KEY, 
        CONSUMER_SECRET=twc.CONSUMER_SECRET,
        ACCESS_TOKEN=twc.ACCESS_TOKEN, 
        ACCESS_SECRET=twc.ACCESS_SECRET)
    tws.run_stream(search_words,limit)
    return str(search_word)+" "+str(limit)


@app.route('/getTweets')
def getTweets():
    """
    GET REQUEST FORMAT :

    getTweets?word&from_date=&to_date&count_per_day=&total_count=

    """
    search_words=[]
    search_words.append(request.args.get('word',None,str))
    from_date=request.args.get('from_date',None,str)
    to_date=request.args.get('to_date',None,str)
    count_per_day=request.args.get('count_per_day',1,int)
    total_count=request.args.get('total_count',2,int)
    print(from_date,to_date,count_per_day,total_count)
    tws = TwitterStream(
        CONSUMER_KEY=twc.CONSUMER_KEY, 
        CONSUMER_SECRET=twc.CONSUMER_SECRET, 
        ACCESS_TOKEN=twc.ACCESS_TOKEN,
        ACCESS_SECRET=twc.ACCESS_SECRET)
    tws.get_previous_tweet(search_words,from_date,to_date,count_per_day,total_count)

    return send_file(
        'twitter/twitter_previous.csv', 
        attachment_filename=from_date+".csv")

# @app.route('/test')
# def testGet():
#     return send_file(
#         'twitter/twitter_previous.csv', 
#         attachment_filename="test.csv")
if __name__ == "__main__":
    app.run()