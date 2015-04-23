import sys

import Utility as u
import Features as f
import Bayes as b

"""
PREPROCESSING
"""

print "Enter name of file containing learning set: "
learning_name = raw_input()
print "Enter name of file containing test set: "
test_name = raw_input()

learning_data = u.read_learning_data(learning_name,0)
test_data = u.read_test_data(test_name, 0)
fields = list(test_data.keys)
num_fields = len(fields)
num_nonevents = len(learning_data[0][fields[0]])
num_events = len(learning_data[1][fields[0]])
num_tests = len(test_data[fields[0]])

"""
FEATURES
"""


learning_nonevent_features = [[] for i in xrange(num_nonevents)]
learning_event_features = [[] for i in xrange(num_events)]
test_features = [[] for i in xrange(num_tests)]

for i in xrange(num_nonevents):
  for k in fields:
    learning_nonevent_features[i] = (learning_nonevent_features[i] + 
      f.get_features(learning_data[0][k][i]))

for i in xrange(num_events):
  for k in fields:
    learning_event_features[i] = (learning_event_features[i] +
      f.get_features(learning_data[1][k][i]))

for i in xrange(num_tests):
  for k in fields:
    test_features[i] = (test_features[i] +
      f.get_features(test_data[k][i]))

print learning_nonevent_features
print learning_event_features
print test_features

sys.exit(0)

"""
BAYESIAN
"""

distro = bayesian.process(learning_features) # uncertain what format distro is, but we'll get to that
guesses = [False for i in range(test_data)]
for i in xrange(len(events)):
  guesses[i] = bayesian.guess(test_features, distro)

"""
RESULTS
"""

# print distro (commented while format is still uncertain)
print "Is Event | Email Body"
for i in xrange(len(guesses)):
  print guesses[i] + " | " + test_data[i]


