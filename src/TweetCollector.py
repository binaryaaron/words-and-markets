from slistener import SListener
import time, tweepy, sys

## note that these access tokens and keys are for one app, the second set of
## keys will be shown below these
access_token= "165837734-B4v6m0pIvXsXncbdofsxHUP9vjRAdiTR9EMrQRbQ"
access_token_secret = "mTPYXBdSNuvSXdAZwT1Q8UP1aUtTZyzGD3b86UaRv4LYt"
consumer_key = "STtyAAdlg6XPC5LTOkGiZSQu0"
consumer_secret = "bB8nCS2h8WWCq7jVXTqrXOBJEci3FDS0vC68RYNQEhpglQ5Gw3"

access_token2= "165837734-eRt5czqtEfmKwchItkO0Mt9WVOa5kQQndOaLGPCl"
access_token_secret2 = "kMSfPqTJG5qOoQqw8BJYF6fe9e2Zcbrwbi3IEURExgkd6"
consumer_key2 = "4b2nMeO5i1AjTuriHhZSRXTzb"
consumer_secret2 = "uZZwhLHs0JUbim7GymmteyFBrC4UQz78QWGVRHs3j6MfroyyCT"




auth = tweepy.OAuthHandler(consumer_key2, consumer_secret2)
auth.set_access_token(access_token2, access_token_secret2)
api      = tweepy.API(auth)


def main( mode = 1 ):
	#track  = ['AAPL', 'apple', 'iphone', 'tim cook', 'ipad', 'mac']
	#track  = ['AAPL', 'apple', 'mac', 'tim cook', 'GOOG', 'google', 'gmail', 'youtube', 
			#'windows', 'microsoft', 'msft'] 
	track = ['twitter', 'tweet', 'twtr', 'amazon', 'amzn', 'prime', 'aws' ]
	follow = []

	listen = SListener(api, 'stocktweets')
	stream = tweepy.Stream(auth, listen)

	print "Streaming started on %s keywords and %s users ..." % (len(track), len(follow))

	try: 
		stream.filter(track = track, follow = follow)
		#stream.sample()
	except:
		print "error!"
		stream.disconnect()

if __name__ == '__main__':
	main()
