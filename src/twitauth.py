import tweepy
access_token= "165837734-B4v6m0pIvXsXncbdofsxHUP9vjRAdiTR9EMrQRbQ"
access_token_secret = "mTPYXBdSNuvSXdAZwT1Q8UP1aUtTZyzGD3b86UaRv4LYt"
consumer_key = "STtyAAdlg6XPC5LTOkGiZSQu0"
consumer_secret = "bB8nCS2h8WWCq7jVXTqrXOBJEci3FDS0vC68RYNQEhpglQ5Gw3"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
        print tweet.text




