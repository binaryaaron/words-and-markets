from tweepy import StreamListener
import sys, tweepy, time
import json, time, sys
import pymongo
import twitterDevKeys
import datetime
from datetime import timedelta

client = pymongo.MongoClient()
db = client["tweetdb"]
tweets = db.tweets

keys_to_delete = [
  "following",
  "profile_background_color",
  "profile_background_image_url", 
  "profile_background_image_url_https",
  "profile_background_tile", 
  "profile_banner_url", 
  "profile_image_url",
  "profile_image_url_https", 
  "profile_link_color",
  "profile_use_background_image", 
  "profile_sidebar_border_color",
  "profile_sidebar_fill_color",
  "profile_background_tile",
  "profile_image_url",
  "follow_request_sent",
  "profile_link_color",
  "favourites_count",
  "url",
  "contributors_enabled",
  "utc_offset",
  "id",
  "listed_count",
  "protected",
  "profile_text_color",
  "geo_enabled",
  "notifications",
  "description",
  "statuses_count",
  "following",
  "show_all_inline_media",
  "default_profile_image",
  "default_profile"
]

class StdOutListener(StreamListener):
  def __init__(self):
    self.counter = 0
    self.tweetCount = 0
    self.engCounter = 0
    self.fprefix = 'msftGoogAaplTweets'
    self.output  = open('../data/' + self.fprefix + '.' 
                    + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
    print self.output
    print keys_to_delete
    self.delout  = open('../data/delete.txt', 'a')

  def on_data(self, data):
    decoded = json.loads(data)
    #print('printing unrefined tweet\'s user info \n')
    #print(decoded['user'])
    #print(decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
    try:
      if decoded['lang'] != 'en' or decoded['lang']== None:
        self.engCounter += 1
        #print "not english"
        return True
    except KeyError:
      #print 'null lang field'
      return True

    empty_keys = [k for k,v in decoded.iteritems() if not v]
    for k in empty_keys:
      del decoded[k]
    #tweet_keys = [k for k,v in decoded.iteritems()]
    try: 
      retweeted_status = decoded['retweeted_status']
    except KeyError:
      retweeted_status = False


    for thing in keys_to_delete:
      try:
        #print('deleting ' + thing ) 
        del decoded['user'][thing]
        if retweeted_status:
          #del decoded['retweeted_status']['user'][thing]
          del decoded['retweeted_status']
          empty_keys = [k for k,v in retweeted_status.iteritems() if not v]
          for k in empty_keys:
            del decoded['retweeted_status'][k]
      except KeyError:
        sys.exc_clear()
        #print "key not found"

    #print('printing the refined tweet \'s user info \n')
    #print(decoded['user'])

    try:
      decoded['created_at'] = datetime.datetime.strptime(decoded['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
      decoded['user']['created_at'] = datetime.datetime.strptime(decoded['user']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    except:
      pass
      print 'failed to parse date'
    
    try:
      tweets.insert(decoded)
    except IOError as exc:
      print exc
      if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
        print exc
        raise # Propag

    return # end of function

  def on_error(self, status_code):
    print('Got an error with status code: ' + str(status_code))
    print status_code
    return True # To continue listening

  def on_timeout(self):
    print('Timeout...')
    return True # To continue listening


if __name__ == '__main__':
  listener = StdOutListener()
  consumer_key = twitterDevKeys.consumer_key2
  consumer_secret = twitterDevKeys.consumer_secret2
  access_token = twitterDevKeys.access_token2
  access_token_secret = twitterDevKeys.access_token_secret2

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)

  stream = tweepy.Stream(auth, listener)
  try:
    #stream.filter(track=['ebola', 'aapl', 'apple', 'mac', 'tim cook', 'goog',
              #'google', 'gmail', 'youtube', 'microsoft', 'msft',
              #'nadella'])
    stream.sample()
  except:
    print "Unexpected error:", sys.exc_info()[0]
    print sys.exc_info()


