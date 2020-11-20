from config import TwitterCredentials, FacebookCredentials
from twitter.main import TwitterStream

twc = TwitterCredentials()
tws = TwitterStream(CONSUMER_KEY=twc.CONSUMER_KEY, CONSUMER_SECRET=twc.CONSUMER_SECRET,
                    ACCESS_TOKEN=twc.ACCESS_TOKEN, ACCESS_SECRET=twc.ACCESS_SECRET)

# fbc = FacebookCredentials()
# fbs = FacebookStream(ACCESS_TOKEN=fbc.ACCESS_TOKEN)
