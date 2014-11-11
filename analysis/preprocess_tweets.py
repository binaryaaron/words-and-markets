import ujson, datetime, pymongo, csv, afinn_summary, stoplist
from gensim import corpora, models
from datetime import timedelta
from afinn_summary import sentiment
##### globals #####
debug = False
""" The number of topics returned for the time bin by the LSI/LDA models """
number_topics = 80
##### #####
def makeTweetBin(startTime, stopTime):
    """ Cuts the tweets into bins based on times
    uses pymongo to connect to a db that has a bunch of tweets in it.
    Args:
      startTime (datetime): the starting time for the bin in datetime format
      stopTime (datetime): the stopping point for the bin in datetime format
    Returns:
      a list of tweets that match the criteria startTime =< tweets =< stopTime
    """
    print 'making the time-dependent bin of tweets'
    client = pymongo.MongoClient()
    #db = client["tweet_test"]
    db = client["tweetdb"]
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

def filter_words(tweets):
    """ filters a tweet list over a stopword list
    and returns a list of text vectors from that tweet
    Args:
        tweets (list): a list of tweets

    Returns:
        a list of word vectors comprised of the text from each tweet
    """
    print('in filter_words: length of passed tweets = ', len(tweets))
    # these are no longer needed but left for testing
    #stopwords = ['for', 'if','was','a', 'and', 'the', 'of', 'to', 'in', '-',
            #'this', 'rt', 'i', '&amp','by','via','it',
            #'up','on','is','you','at','u','&','&amp;' ]
    words = []
    words = [[ word for word in 
                tweet['text'].lower().split() 
                    if word not in stoplist.stoplist] 
                        for tweet in tweets]
    return words


def make_corpus(text):
    """ makes a Gensim corpus and Dictionary object from text

    Args:
        text (list): a list of word lists
    Returns:
        tuple: a tuple of the corpus and dict
    """
    print 'in make_corpus: length of passed text = ', len(text) 
    print 'making Dictionary'
    temp_dict = corpora.Dictionary(text)
    print 'filtering extreme words'
    temp_dict.filter_extremes(no_below = 5, no_above=0.8)
    temp_dict.filter_tokens()
    temp_dict.compactify()
    print 'making corpus'
    tmp_corpus = [temp_dict.doc2bow(item) for item in text]
    return [tmp_corpus, temp_dict]

def lsi_model(tmp_corpus, temp_dict):
    """ creates an latent semantic indexing model from 
    a corpus of words and a dictionary using gensim
    Args:
        tmp_corpus (list): a list of words from dict
        temp_dict (Dictionary): a gensim Dictionary
    Returns: 
        a list of word vectors that comprise the top 20 topics from an LSI
        model for easy processing. 
    """
    print 'starting lsi model'
    lsi = models.LsiModel(tmp_corpus, id2word=temp_dict,
            num_topics=number_topics)
    lsi_topics = lsi.show_topics(formatted=False)
    words = []
    for topic in lsi_topics:
        for item in topic:
            words.append(item[1])
    return words
        
def lda_model(tmp_corpus, temp_dict):
    """ creates an latent dirlectic analysis model from 
    a corpus of words and a dictionary using gensim
    Args:
        tmp_corpus (list): a list of words from dict
        temp_dict (Dictionary): a gensim Dictionary
    Returns: 
        a list of word vectors that comprise the top 20 topics from an LDA
        model for easy processing. 
    """
    print 'starting lda model'
    lda = models.LdaMulticore(tmp_corpus, id2word=temp_dict,
            num_topics=number_topics)
    lda_topics = lda.show_topics(formatted=False)
    words = []
    for topic in lda_topics:
        for item in topic:
            words.append(item[1])
    return words


def write_csv(row):
    """ Convenience function for writing a list of fields to a csv file by
    appending to the opened file
    Args:
        row (list): the list to write in the csv file
    """
    if debug:
        print('writing row')
    with open('tweet_sentiment_scores.csv', 'a') as f:
        writer = csv.writer(f, delimiter = ',')
        #for r in row:
        #writer.writerow(r)
        writer.writerow(row)


if __name__ == '__main__':
    """ Driver for the script that loops over the mongo db until a final time
    block is reached.
    """
    final_end_time = datetime.datetime(2014,11,2,18)
    start_time = datetime.datetime(2014,10,18,6)
    end_time = start_time + timedelta(hours = 1)
    if debug:
        print('debug!')
        end_time = start_time + timedelta(hours = 1)
    
    rows = []
    while start_time < final_end_time:
        print 'working on timeframe', start_time, end_time
        row = []
        hour_bin = makeTweetBin(start_time, end_time)
        print 'length of current bin = ', len(hour_bin)
        if len(hour_bin) == 0:
            print 'skipping empty hour'
            start_time = start_time + timedelta(hours=1)
            end_time = start_time + timedelta(hours=1)
            continue
        num_tweets = len(hour_bin)
        words = filter_words(hour_bin)
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
        write_csv(row)
        start_time = start_time + timedelta(hours=1)
        end_time = start_time + timedelta(hours=1)
        if debug:
            end_time = start_time + timedelta(hours = 1)
        del(hour_bin)
        del(words)
        del(dicts)

    write_csv(rows)
        
