import sys, glob, errno, pymongo, datetime, ujson
from datetime import timedelta

def convert_date(tweet):
  """Converts the date in the tweet from twitter's api format to a python
    datetime object for easy use 
    Args:
      tweet (json): a tweet 
    """
    for (key, value) in tweet.items():
      try:
        tweet[key] = datetime.datetime.strptime(value,'%a %b %d %H:%M:%S +0000 %Y')
      except:
        pass
    return tweet

def make_filelist(path):
  """Makes a list of files through which the program may iterate
    Args:
      path (str): a string indicating the path in which the tweets are stored
    """
    #initial array for the read-in tweets
    files = glob.glob(path)   
    files.sort()
    return files
  #pprint (files)


def insert_tweets(filename):
  """Inserts the tweets into a mongo db in EST 
    Args:
      filename (str): the filename that contains tweet json objects
    """
    client = pymongo.MongoClient()
    db = client["tweetdb"]
    tweets = db.tweets
    try:
      for line in open(filename): 
        current_tweet = ujson.loads(line)
        current_tweet = convert_date(current_tweet)
        #changes time from UST to EST
        current_tweet['created_at'] = current_tweet['created_at'] + timedelta(hours = -5)
        tweets.insert(current_tweet)
    except IOError as exc:
      if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
        raise # Propag

if __name__ == '__main__':
  path = '/home/agonzales/git/mining-moods-markets/data/*.json'
    files = make_filelist(path)
    for filename in files:
      print('attempting to insert the following file into the db')
      print(filename)
      insert_tweets(filename)

