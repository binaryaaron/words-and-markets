from slistener import SListener
import time, tweepy, sys

access_token= "165837734-B4v6m0pIvXsXncbdofsxHUP9vjRAdiTR9EMrQRbQ"
access_token_secret = "mTPYXBdSNuvSXdAZwT1Q8UP1aUtTZyzGD3b86UaRv4LYt"
consumer_key = "STtyAAdlg6XPC5LTOkGiZSQu0"
consumer_secret = "bB8nCS2h8WWCq7jVXTqrXOBJEci3FDS0vC68RYNQEhpglQ5Gw3"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api      = tweepy.API(auth)


def main( mode = 1 ):
    #track  = ['AAPL', 'apple', 'iphone', 'tim cook', 'ipad', 'mac']
    track  = ['AAPL', 'apple', 'mac', 'tim cook', 'GOOG', 'google', 'gmail', 'youtube', 
            'windows', 'microsoft', 'msft'] 
            #'twitter', 'tweet', 'twtr', 'amazon', 'amzn', 'prime', 'aws' ]
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
