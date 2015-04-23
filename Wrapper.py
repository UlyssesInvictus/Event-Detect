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
rare_name = ""#"human_rares.txt"#raw_input()

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
  for rare,count in rares[0:51]:
    rarefile.write(rare+'\n')
  rarefile.close()

print rares[0:26]

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

# then supply averages to bit calculation
learning_nonevent_bits = [f.get_bits(i,avgs_learning) for i in learning_nonevent_features]
learning_event_bits = [f.get_bits(i,avgs_learning) for i in learning_event_features]
test_bits = [f.get_bits(i,avgs_learning) for i in test_features]

# print "learning nonevent features: ", learning_nonevent_features
# print "learning event features: ", learning_event_features
# print "test features: ", test_features

"""
BAYESIAN
"""

# get prior
prior = (num_events/float(num_learning),num_nonevents/float(num_learning))
# get posterior
# first, convert all T/F entries into 1/0 and sum ints
learning_nonevent_bit_sum = u.vertical_sum([[1 if j else 0 for j in i] for i in learning_nonevent_bits])
learning_event_bit_sum = u.vertical_sum([[1 if j else 0 for j in i] for i in learning_event_bits])
# then calculate posterior
posterior = b.get_posterior(learning_event_bit_sum,learning_nonevent_bit_sum)
# guess!
guesses = [b.bayesian(prior, i, posterior) for i in test_bits]

"""
RESULTS
"""

# print distro (commented while format is still uncertain)
print "Is Event | First 10 Words of Email Subject | First 10 Words of Email Body"
for i in xrange(len(guesses)):
  subject = ' '.join(test_data["subject"][i][:min(10,len(test_data["subject"][i]))])
  message = ' '.join(test_data["message"][i][:min(10,len(test_data["message"][i]))])
  print guesses[i], " | ", subject, " | ", message

# TEST ONLY
true_ids = [True if i == 1 else False for i in u.read_event_ids(test_name,4)]
# print "guesses: ", guesses
# print "trues: ", true_ids
print "accuracy: ", u.get_accuracy(true_ids,guesses)
# print "prior: ", prior
# print "posterior: ", posterior