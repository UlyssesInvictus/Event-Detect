import Utility as u
from operator import itemgetter
import sys
import dateutil.parser as dparser

"""
Input: (long) arrays of words for events and non-events
Output: array of tuples of word and relative frequency between event and nonevent, sorted by relative frequency 
Assumes only one type of category. (Though you can cheat this.)
Works by calculating frequencies on both arrays, then comparing relative frequencies of each.
"""
def get_rares(event_words,nonevent_words):
  # could take a while, these are long arrays
  event_freaks = u.get_frequencies(event_words)
  nonevent_freaks = u.get_frequencies(nonevent_words)

  all_words = list (set(event_freaks) | set(nonevent_freaks))
  relative_freaks = [("blank",0) for i in xrange(len(all_words))]
  word_count = 0
  for word in all_words:
    event_count = 0 if word not in event_freaks else event_freaks[word]
    nonevent_count = 0 if word not in nonevent_freaks else nonevent_freaks[word]
    relative_freaks[word_count] = (word,event_count/float(len(event_freaks)) - nonevent_count/float(len(nonevent_freaks)))
    word_count+=1

  return sorted(relative_freaks,key=lambda tup: tup[1],reverse=True)

"""
Input: array of email words and rare words filename (optional).
Output: array of metrics.
If no rare words argument passed, defaults to a file. If file doesn't already exist, prints notice to call set_rares and fails. 
Metrics TBD. Currently set: number of rare words. Boolean for rare word. 
"""

def get_features(data,type_words,rares):

  if type_words == "sender":
    if "lists.hcs.harvard.edu" in data: # "lists.fas.harvard.edu" in data:
      return [10]
    else:
      return [0]
  # elif type_words == "fullmessage":
  #   try:
  #     current = dparser.parse("blank",fuzzy=True)
  #     result = dparser.parse(data,fuzzy=True)
  #     if result == current:
  #       return [0]
  #     else:
  #       return [10]
  #   except:
  #     return [0]
  elif type_words == "message" or type_words == "subject":
    # get frequencies for words
    word_freq = u.get_frequencies(data)
    
    num_rares = len(rares)

    # calculate feature vector
    # features = [0 for i in xrange(num_rares * 2)]
    # for i in xrange(num_rares):
    #   if rares[i] in word_freq:
    #     features[i] = word_freq[rares[i]]
    #     features[i+num_rares] = 1
    #   else:
    #     features[i] = 0
    #     features[i+num_rares] = 0
    
    # return features
    # exclusivity only; uncomment above "return" to include frequency
    
    num_matching = 0
    features = [0 for i in xrange(80)]
    for i in xrange(80):#num_rares):
      if rares[i] in word_freq:
        features[i] = 10 # found by trial and error
        num_matching+=1
      else:
        features[i] = 0

    features+=[len(data)]
    features+=[num_matching]
    if (("location" in data or "where" in data or "place" in data) and 
        ("time" in data or "when" in data or "date" in data)):
      features+=[10]
    else:
      features+=[0]

    return features
  else:
    return []

def get_bits(features,averages):
  return [features[i] > averages[i] for i in xrange(len(features))]