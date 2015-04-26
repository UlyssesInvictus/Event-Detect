import sys

import Utility as u
import Features as f
import Bayes as b

"""
PREPROCESSING
"""

print "Enter name of file containing learning set: "
learning_name = "data/learning_data.xlsx"#raw_input()
print "Enter name of file containing test set: "
test_name = "data/test_data.xlsx"#raw_input()
print "Enter name of rare words file; leave blank to generate in rares.txt"
rare_name = raw_input()#"test.txt"#"human.txt"#"test.txt"#raw_input()

learning_data = u.read_learning_data(learning_name,0)
test_data = u.read_test_data(test_name, 0)
fields = list(test_data)
num_fields = len(fields)
num_nonevents = len(learning_data[0][fields[0]])
num_events = len(learning_data[1][fields[0]])
num_learning = num_nonevents+num_events
num_tests = len(test_data[fields[0]])

"""
FEATURES
"""
# set rares
if rare_name == "":
  rare_name = "rares.txt"
  # create by frequency
  all_event_words = []
  all_nonevent_words = []
  # concat all words...this could take a while
  for k in fields:
    if type(learning_data[0][k][0]) is not list:
      continue
    for i in xrange(num_events):
      all_event_words = all_event_words + learning_data[1][k][i]
    for i in xrange(num_nonevents):
      all_nonevent_words = all_nonevent_words + learning_data[0][k][i]
  rares = f.get_rares(all_event_words,all_nonevent_words)
  rarefile = open('rares.txt','w')
  for rare,count in rares[0:39]:
    rarefile.write(rare+'\n')
  rarefile.close()

# get int features
learning_nonevent_features = [[] for i in xrange(num_nonevents)]
learning_event_features = [[] for i in xrange(num_events)]
test_features = [[] for i in xrange(num_tests)]

for i in xrange(num_nonevents):
  for k in fields:
    if type(learning_data[0][k][0]) is not list:
      continue 
    learning_nonevent_features[i] = (learning_nonevent_features[i] + 
      f.get_features(learning_data[0][k][i], rare_name))

for i in xrange(num_events):
  for k in fields:
    if type(learning_data[0][k][0]) is not list:
      continue 
    learning_event_features[i] = (learning_event_features[i] +
      f.get_features(learning_data[1][k][i], rare_name))

for i in xrange(num_tests):
  for k in fields:
    if type(learning_data[0][k][0]) is not list:
      continue 
    test_features[i] = (test_features[i] +
      f.get_features(test_data[k][i], rare_name))

# then convert to bit vectors
# first, sum all vectors to get average
sum_nonevents = u.vertical_sum(learning_nonevent_features)
sum_events = u.vertical_sum(learning_event_features)
avgs_learning = [float(i)/num_learning for i in u.vertical_sum([sum_events,sum_nonevents])]

# print sum_nonevents
# print sum_events
# print avgs_learning

# print "learning nonevent features: ", learning_nonevent_features
# print "learning event features: ", learning_event_features
# print "test features: ", test_features

"""
BAYESIAN
"""

# get prior
prior = (num_events/float(num_learning),
  num_nonevents/float(num_learning))
# get posterior

event_by_features = u.by_features(learning_event_features)
nonevent_by_features = u.by_features(learning_nonevent_features)


# two curves
event_posterior = [(b.mean(feature),b.stdev(feature)) for feature in event_by_features]
nonevent_posterior = [(b.mean(feature),b.stdev(feature)) for feature in nonevent_by_features]
two_posterior = (event_posterior,nonevent_posterior)

# one curve
all_by_features = u.by_features(learning_event_features+learning_nonevent_features)
one_posterior = [(b.mean(feature), b.stdev(feature)) for feature in all_by_features]

# # guess!
guesses = [b.two_bayesian(prior, i, two_posterior) for i in test_features]

# guesses = [b.one_bayesian(prior, i, one_posterior) for i in test_features]


"""
RESULTS
"""

print "Is Event (First 30 Emails) | First 10 Words of Email Subject | First 10 Words of Email Body"
for i in xrange(min(30,len(guesses))):
  subject = ' '.join(test_data["subject"][i][:min(10,len(test_data["subject"][i]))])
  message = ' '.join(test_data["message"][i][:min(10,len(test_data["message"][i]))]) 
  print guesses[i], " | ", subject, " | ", message

# TEST ONLY
true_ids = [True if i == 1 else False for i in u.read_event_ids(test_name,4)]
# print "guesses: ", guesses
# print "trues: ", true_ids
print "accuracy: ", u.get_accuracy(true_ids,guesses)
print "prior: ", prior
num_right_true = 0
num_real_true = 0 
num_right_false = 0
num_real_false = 0
for i in xrange(len(true_ids)):
  if true_ids[i] and guesses[i]:
    num_right_true+=1
  if true_ids[i]:
    num_real_true+=1
  if not true_ids[i] and not guesses[i]:
    num_right_false+=1
  if not true_ids[i]:
    num_real_false+=1
print "num right true: ", num_right_true
print "num real true: ", num_real_true
print "num right false: ", num_right_false
print "num real false: ", num_real_false
# print "posterior: ", posterior
