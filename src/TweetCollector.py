from slistener import SListener
import twitterDevKeys
import time, tweepy, sys, getopt

## note that these access tokens and keys are for one app, the second set of
## keys will be shown below these





def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h:kj", ["help", "key=" ])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "help"):
            sys.exit()
        elif opt == '-k':
            auth = tweepy.OAuthHandler(twitterDevKeys.consumer_key,
                    twitterDevKeys.consumer_secret)
            auth.set_access_token(twitterDevKeys.access_token,
                    twitterDevKeys.access_token_secret)
            print "Accessing with %s key" % (twitterDevKeys.access_token)
            key = 1

        elif opt == '-j':
            auth = tweepy.OAuthHandler(twitterDevKeys.consumer_key2,
                    twitterDevKeys.consumer_secret2)
            auth.set_access_token(twitterDevKeys.access_token2, twitterDevKeys.access_token_secret2)
            print "Accessing with %s key" % (twitterDevKeys.access_token2)
            key = 2

        else: 
            auth = tweepy.OAuthHandler(twitterDevKeys.consumer_key,
                    twitterDevKeys.consumer_secret)
            auth.set_access_token(twitterDevKeys.access_token, twitterDevKeys.access_token_secret)
            print "Accessing with %s key" % (twitterDevKeys.access_token)
            key = 1

    api = tweepy.API(auth)

    if key == 1:
        track  = ['AAPL', 'apple', 'mac', 'tim cook', 'GOOG', 'google', 'gmail',
                'youtube'] 
    elif key == 2:
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
    main(sys.argv[1:])
