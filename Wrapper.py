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

# get int features
learning_nonevent_features = [[] for i in xrange(num_nonevents)]
learning_event_features = [[] for i in xrange(num_events)]
test_features = [[] for i in xrange(num_tests)]

for i in xrange(num_nonevents):
  for k in fields:
    if type(learning_data[0][k][0]) is not list:
      continue 
    learning_nonevent_features[i] = (learning_nonevent_features[i] + 
      f.get_features(learning_data[0][k][i]))

for i in xrange(num_events):
  for k in fields:
    if type(learning_data[0][k][0]) is not list:
      continue 
    learning_event_features[i] = (learning_event_features[i] +
      f.get_features(learning_data[1][k][i]))

for i in xrange(num_tests):
  for k in fields:
    if type(learning_data[0][k][0]) is not list:
      continue 
    test_features[i] = (test_features[i] +
      f.get_features(test_data[k][i]))

# then convert to bit vectors
sum_nonevents = u.vertical_sum(learning_nonevent_features)
sum_events = u.vertical_sum(learning_event_features)
avgs_learning = [float(i)/num_learning for i in u.vertical_sum([sum_events,sum_nonevents])]

# print sum_nonevents
# print sum_events
# print avgs_learning

learning_nonevent_bits = [f.get_bits(i,avgs_learning) for i in learning_nonevent_features]
learning_event_bits = [f.get_bits(i,avgs_learning) for i in learning_event_features]
test_bits = [f.get_bits(i,avgs_learning) for i in test_features]

# print "learning nonevent features: ", learning_nonevent_features
# print "learning event features: ", learning_event_features
# print "test features: ", test_features

"""
BAYESIAN
"""

prior = (num_events/float(num_learning),num_nonevents/float(num_learning))
learning_nonevent_bit_sum = u.vertical_sum([[1 if j else 0 for j in i] for i in learning_nonevent_bits])
learning_event_bit_sum = u.vertical_sum([[1 if j else 0 for j in i] for i in learning_event_bits])
posterior = b.get_posterior(learning_event_bit_sum,learning_nonevent_bit_sum)

guesses = [b.bayesian(prior, i, posterior) for i in test_bits]

"""
RESULTS
"""

# print distro (commented while format is still uncertain)
print "Is Event | Email Subject | Email Body"
for i in xrange(len(guesses)):
  print guesses[i], " | ", test_data["subject"][i], " | ", test_data["message"][i]

# TEST ONLY
true_ids = [True if i == 1 else False for i in u.read_event_ids(test_name,4)]
print "guesses: ", guesses
print "trues: ", true_ids
print "accuracy: ", u.get_accuracy(true_ids,guesses)