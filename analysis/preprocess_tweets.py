import csv
from gensim import corpora, models
import ujson, datetime, pymongo
from datetime import timedelta
import afinn_summary
from afinn_summary import sentiment
debug = True
"""
Cuts the tweets into bins
may need to remake to account for reducing passes over the tweet db
"""
def makeTweetBin(startTime, stopTime):
    print('starting makeTweetBin')
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
    print('in makeTweetBin: ', len(bin))
    return bin

"""
filters a tweet list over a stopword list
and returns a list of text vectors from that tweet
"""
def filter_words(tweets):
    print('in filter_words: length of passed tweets = ', len(tweets))
    stopwords = ['for', 'if','was','a', 'and', 'the', 'of', 'to', 'in', '-',
    'this', 'rt', 'i']
    words = []
    words = [[ word for word in tweet['text'].lower().split() if word not in stopwords] for tweet in tweets]
    return words


def make_corpus(text):
    print('in make_corpus: length of passed text = ', len(text))
    temp_dict = corpora.Dictionary(text)
    temp_dict.filter_extremes(no_below = 10)
    temp_dict.filter_tokens()
    temp_dict.compactify()
    tmp_corpus = [temp_dict.doc2bow(item) for item in text]
    return [tmp_corpus, temp_dict]

def lsi_model(tmp_corpus, temp_dict):
    if debug:
        print('starting lsi model')
    lsi = models.LsiModel(tmp_corpus, id2word=temp_dict, num_topics=20)
    lsi_topics = lsi.show_topics(formatted=False)
    words = []
    for topic in lsi_topics:
        for item in topic:
            words.append(item[1])
    return words
        
def lda_model(tmp_corpus, temp_dict):
    if debug:
        print('starting lda model')
    lda = models.LdaMulticore(tmp_corpus, id2word=temp_dict, num_topics=20)
    lda_topics = lda.show_topics(formatted=False)
    words = []
    for topic in lda_topics:
        for item in topic:
            words.append(item[1])
    return words


def write_csv(row):
    if debug:
        print('writing row')
    with open('some.csv', 'wb') as f:
        writer = csv.writer(f, delimiter = ',')
        for r in row:
            writer.writerow(r)


if __name__ == '__main__':
        
    final_end_time = datetime.datetime(2014,11,2,16)
    start_time = datetime.datetime(2014,11,2,8)
    end_time = start_time + timedelta(hours = 1)
    if debug:
        print('debug!')
        end_time = start_time + timedelta(hours = 1)
    
    rows = []
    print('attempting to starting this horrid process')
    while start_time < final_end_time:
        print('working on timeframe', start_time, end_time)
        row = []
        hour_bin = makeTweetBin(start_time, end_time)
        print('length of current bin = ', len(hour_bin))
        num_tweets = len(hour_bin)
        words = filter_words(hour_bin)
        print('word length = ', len(words))
        dicts = make_corpus(words)

        lsi_words = lsi_model(dicts[0],dicts[1])
        if not debug:
            lda_words = lda_model(dicts[0],dicts[1])
        lsi_score = sentiment(lsi_words)
        if not debug:
            lda_score = sentiment(lda_words)
        row.append(start_time)
        row.append(num_tweets)
        row.append(lsi_words)
        if not debug:
            row.append(lda_words)
        row.append(lsi_score)
        if not debug:
            row.append(lda_score)
        print('this is the row')
        print(row)
        rows.append(row)
        start_time = start_time + timedelta(hours=1)
        end_time = start_time + timedelta(hours=1)
        if debug:
            end_time = start_time + timedelta(hours = 1)
        del(hour_bin)
        del(words)
        del(dicts)

    write_csv(rows)
        
