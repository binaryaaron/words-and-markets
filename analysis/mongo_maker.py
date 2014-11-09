import sys, glob, errno, pymongo, datetime, ujson
from datetime import timedelta




def convert_date(tweet):
    for (key, value) in tweet.items():
        try:
            tweet[key] = datetime.datetime.strptime(value,'%a %b %d %H:%M:%S +0000 %Y')
        except:
            pass
    return tweet

def make_filelist(path):
	#initial array for the read-in tweets
	files = glob.glob(path)   
	files.sort()
	return files
	#pprint (files)


def insert_tweets(filename):
	client = pymongo.MongoClient()
	db = client["tweet_test"]
	tweets = db.tweets
	try:
		for line in open(filename): # No need to specify 'r': this is the default.
			current_tweet = ujson.loads(line)
			current_tweet = convert_date(current_tweet)
			#changes time from UST to EST
			current_tweet['created_at'] = current_tweet['created_at'] + timedelta(hours = -5)
			tweets.insert(current_tweet)
	except IOError as exc:
		if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
			raise # Propag

if __name__ == '__main__':
	path = ''
	files = make_filelist(path)
	for filename in files:
		print('attempting to insert the following file into the db')
		print(filename)
		insert_tweets(filename)


