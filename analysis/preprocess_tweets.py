import csv
from gensim import corpora, models
import ujson, datetime, pymongo
from datetime import datetime
import afinn_summary
from afinn_summary import sentiment

"""
Cuts the tweets into bins
may need to remake to account for reducing passes over the tweet db
"""
def makeTweetBin(startTime, stopTime, tweets):
    client = pymongo.MongoClient()
    db = client["tweet_test"]
    tweets = db.tweets
    bin = []
    bin = [ tweet for tweet in 
               tweets.find({
                    "created_at": {
                        "$lt": end_time,
                        "$gte": start_time}
                   }) 
          ]
    return bin

"""
filters a tweet list over a stopword list
and returns a list of text vectors from that tweet
"""
def filter_words(tweets):
    stopwords = ['for', 'if','was','a', 'and', 'the', 'of', 'to', 'in', '-',
    'this', 'rt', 'i']
    text = [[ word for word in tweet['text'].lower().split() 
            if word not in stopwords]
                 for tweet in tweets]
    return text



def make_corpus(text):
"""
Makes and returns a gensima corpus and Dictionary from a text vector
"""
    tempDict = corpora.Dictionary(text)
    tempDict.filter_extremes(no_below = 10)
    tempDict.filter_tokens()
    tempDict.compactify()
    tmp_corpus = [tempDict.doc2bow(item) for item in text]
    return [tempDict, tmp_corpus]

def lsi_model(tmp_corpus, temp_dict):
"""
returns the words from a 20-topic summary of an LSI model
"""
    lsi = models.LsiModel(tmp_corpus, id2word=temp_dict, num_topics=20)
    lsi_topics = lsi.show_topics(formatted=False)
    words = []
    for topic in lsi_topics:
        for item in topic:
            words.append(item[1])
    return words
        
def lda_model(tmp_corpus, temp_dict):
"""
returns the words from a 20-topic summary of an lda model
"""
    lda = models.LdaMulticore(tmp_corpus, id2word=temp_dict, num_topics=20)
    lda_topics = lda.show_topics(formatted=False)
    words = []
    for topic in lsi_topics:
        for item in topic:
            words.append(item[1])
    return words


def write_csv():
    with open('some.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(someiterable)


if __name__ == '__main__':
    final_end_time = datetime.datetime(2014,11,2,16)
    start_time = datetime.datetime(2014,11,2,8)
    end_time = start_time + timedelta(hours = 1)
    
    print('attempting to starting this horrid process')
    while start_time < final_end_time:
        print('working on timeframe', start_time)
        row = []
        hour_bin = makeTweetBin(start_time, end_time)
        num_tweets = len(hour_bin)
        words = filter_words(bin)
        corpora = make_corpus(words)
        lsi_words = lsi_model(corpora[0], corpora[1])
        lda_words = lda_model(corpora[0], corpora[1])
        lsi_score = sentiment(lsi_words)
        lda_score = sentiment(lda_words)
        row.append(start_time)
        row.append(num_tweets)
        row.append(lsi_words)
        row.apend(lda_words)
        row.append(lsi_score)
        row.append(lda_score)
        start_time = start_time + timedelta(hours=1)
        end_time = start_time + timedelta(hours=1)
        




