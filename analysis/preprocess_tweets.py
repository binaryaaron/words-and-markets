from gensim import corpora, models
import json, datetime
from datetime import datetime
"""
A date hook for json filtering. goal is to convert the date in the tweet 
to a datetime object
"""
def date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.datetime.strptime(value,'%a %b %d %H:%M:%S +0000 %Y')
        except:
            pass
    return json_dict


"""
Takes a string and returns a list of tweets
"""
def readJsonFile(file):
    tweets = []
    for line in open(file):
        try: 
            tweets.append(json.loads(line, object_hook=date_hook))
        except:
            pass
    return tweets

"""
Cuts the tweets into bins
may need to remake to account for reducing passes over the tweet db
"""
def makeTweetBin(startTime, stopTime, tweets):
    tweet_bin = [tweet for tweet in datetweets 
            if tweet['created_at'] >= startTime and tweet['created_at'] >= endTime ]
    return tweet_bin

"""
filters a tweet list over a stopword list
and returns a list of text vectors from that tweet
"""
def filter_words(tweets):
    stopwords = ['for', 'if','was','a', 'and', 'the', 'of', 'to', 'in', '-',
    'this']
    text = [[ word for word in tweet['text'].lower().split() 
            if word not in stopwords]
                 for tweet in tweets]
    return text


"""
Filters out words that only occur once
Major time killer, lots of iterations here
"""
def filter_low_freq_words(text):
    all_tokens = sum(text,[])
    tokens_once_2 = set(word for word in set(all_tokens) if
            all_tokens.count(word) ==1)
    print len(tokens_once_2)
    print 'unique tokens'
    text = [[word for word in tweet if word not in tokens_once_2]
                    for tweet in text]
    return text

"""
Makes and returns a gensima corpus and Dictionary from a text vector
"""
def makeCorpus(text):
    tempDict = corpora.Dictionary(text)
    #print(tempDict)
    tmp_corpus = [tempDict.doc2bow(item) for item in text]
    #print(tmp_corpus[0])
    return [tempDict, tmp_corpus]


