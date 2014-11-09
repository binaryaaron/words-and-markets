import math,re,sys
reload(sys)
sys.setdefaultencoding('utf-8')
 
# AFINN-111 is as of June 2011 the most recent version of AFINN
filenameAFINN = '/home/agonzales/git/mining-moods-markets/src/AFINN/AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ 
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))
 
# Word splitter pattern
pattern_split = re.compile(r"\W+")
 
def sentiment(text):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence. 
    """
    #words = pattern_split.split(text)
    words = text
    #print(words)
    sentiments = map(lambda word: afinn.get(word, 0), words)
    if sentiments:
        # How should you weight the individual word sentiments? 
        # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
        sentiment = float(sum(sentiments)/math.sqrt(len((sentiments))))
        
    else:
        sentiment = 0
    return sentiment
