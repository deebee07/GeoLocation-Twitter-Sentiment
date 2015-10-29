#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-stream-format:
#  - ultra-real-time stream of twitter's public timeline.
#    does some fancy output formatting.
#-----------------------------------------------------------------------

from twitter import *
import re
import sys
import math
import re
import pandas

search_term = "Chocolate"

#-----------------------------------------------------------------------
# import a load of external features, for text display and date handling
# you will need the termcolor module:
#
# pip install termcolor
#-----------------------------------------------------------------------
from time import strftime
from textwrap import fill
from termcolor import colored
from email.utils import parsedate

#-----------------------------------------------------------------------
# load our API credentials 
#-----------------------------------------------------------------------
config = {}
execfile("config.py", config)

reload(sys)
sys.setdefaultencoding('utf-8')

# AFINN-111 is as of June 2011 the most recent version of AFINN
filenameAFINN = 'Dict/DictSent.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ 
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))

# Word splitter pattern
pattern_split = re.compile(r"\W+")




def sentiment(text):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence. 
    """
    words = pattern_split.split(text.lower())
    sentiments = map(lambda word: afinn.get(word, 0), words)
    if sentiments:
        # How should you weight the individual word sentiments? 
        # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
        sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
        
    else:
        sentiment = 0
    return sentiment




#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
auth = OAuth(config["access_token"], config["access_secret"],config["consumer_key"], config["consumer_secret"])
stream = TwitterStream(auth = auth, secure = True)

#-----------------------------------------------------------------------
# iterate over tweets matching this filter text
#-----------------------------------------------------------------------
tweet_iter = stream.statuses.filter(track = search_term,geocode = '-81.474144, 34,100')






pattern = re.compile("%s" % search_term, re.IGNORECASE)
i = 1
positive=0
negative=0
neutral=0
for tweet in tweet_iter:
		if(i<100):
			# turn the date string into a date object that python can handle
			timestamp = parsedate(tweet["created_at"])

			# now format this nicely into HH:MM:SS format
			timetext = strftime("%H:%M:%S", timestamp)

			# colour our tweet's time, user and text
			time_colored = colored(timetext, color = "white", attrs = [ "bold" ])
			user_colored = colored(tweet["user"]["screen_name"], "green")
			text_colored = tweet["text"]

			# replace each instance of our search terms with a highlighted version
			text_colored = pattern.sub(colored(search_term.upper(), "yellow"), text_colored)

			# add some indenting to each line and wrap the text nicely
			indent = " " * 11
			text_colored = fill(text_colored, 80, initial_indent = indent, subsequent_indent = indent)
			print "TWEET NUMBER " + str(i)
			# now output our tweet
			print "(%s) @%s" % (time_colored, user_colored)
			print "%s" % (text_colored)
			i=i+1
			sentiments = map(sentiment, [ tweet['text'] ])
			Sentimentscore=sum(sentiments)/math.sqrt(len(sentiments))
			if Sentimentscore>0.0:
				positive=positive+1
				print "POSITIVE TWEET"
					  			
			elif Sentimentscore<0.0:
				negative=negative+1
				print "NEGATIVE TWEET"
					  			
			elif Sentimentscore==0.0 :
				neutral=neutral+1
				print "NEUTRAL TWEET"	  			 
		else:
			break

print "SEARCHED TERM DONALD"
print "GEO LOCATION SAN JOSE"
print "TOTAL TWEETS ANALYZED 100"
print "COUNT OF POSITIVE IS "+str(positive)+ "  COUNT OF NEGATIVE IS "+str(negative) + "  COUNT OF NEUTRAL IS "+ str (neutral)

