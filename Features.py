import Ultity.py as u
from collections import defaultdict



def extract_words(email_dict):
	full_list = []
	for sublst in email_dict["message"]:
		full_list.append(sublst)
	freq_dict= defaultdict( int )
	for word in full_list:
		freq_dict[word] += 1


"""
Input: arrays of email strings for events and non-events, filename (optional), and number of rare words (optional).
Output: array of relative differences of words. Side-effect of creating a file with rare words line by line. 
Defaults to filename and number if args not passed.
Assumes only one type of category.
Works by concatenating all calls to split_words for both event and non-events, then comparing relative frequencies of each. Sets as rare words the words most distinctive of events.
"""
def set_rares(event_words,unevent_words,filename="rares.txt",num_rares=25):
  relative_frequences = {}
  sorted_relative = []
  return sorted_relative

"""
Input: array of email data and rare words files (optional).
Output: array of metrics.
If no rare words argument passed, defaults to a file. If file doesn’t already exist, prints notice to call set_rares and fails. 
Metrics TBD. Currently set: number of rare words. Boolean for rare word. 
"""

def get_features(data,filename="rares.txt"):
  features = []
  return features