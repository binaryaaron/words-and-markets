from tweepy import StreamListener
import sys, tweepy, time
import json, time, sys
import twitterDevKeys

class StdOutListener(StreamListener):
	def __init__(self):
		self.counter = 0
		self.engCounter = 0
		self.fprefix = 'twtrFbAmznTweets'
		self.output  = open('../data/' + self.fprefix + '.' 
				+ time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
		print self.output
		self.delout  = open('../data/delete.txt', 'a')

	def on_data(self, data):
		#		# Prints the text of the tweet
		decoded = json.loads(data)
		try:
			if decoded['lang'] != 'en' or decoded['lang']== None:
				self.engCounter += 1
#				print "not english"
				return True
		except KeyError:
			print 'null lang field'
			return True
#		print(decoded['user']['screen_name'], decoded['text'].encode('ascii',
#			'ignore'))
#		print 'writing to file'
		self.output.write(data)
		self.counter += 1
		if self.counter >= 20000:
			self.output.close()
			self.output = open('../data/' + self.fprefix + '.' 
					+ time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
			self.counter = 0
		return 

#	def on_status(self, status):
#		print 'got a tweet'
#		if status.lang == 'en':
#			print 'writing to file'
#		self.output.write(status)
#		self.counter += 1
#		if self.counter >= 20000:
#			self.output.close()
#			self.output = open('../data/' + self.fprefix + '.' 
#					+ time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
#			self.counter = 0
#		return True
#		if status.lang != 'en':
#			print "not english"
#			return True
#		print status.text
#		print ''
#		return True


	def on_error(self, status_code):
		print('Got an error with status code: ' + str(status_code))
		return True # To continue listening

	def on_timeout(self):
		print('Timeout...')
		return True # To continue listening

if __name__ == '__main__':
	listener = StdOutListener()
	consumer_key = twitterDevKeys.consumer_key
	consumer_secret = twitterDevKeys.consumer_secret
	access_token = twitterDevKeys.access_token
	access_token_secret = twitterDevKeys.access_token_secret

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	stream = tweepy.Stream(auth, listener)
	while True:
		try:
			stream.filter(track=['twrt', 'amazon', 'amzn', 'prime', 'aws','fb', 'facebook'])
		except:
			print 'caught exception'

