import Preprocessing.py as preprocess
import Features.py as feature
import Bayesian.py as bayesian


"""
PREPROCESSING
"""

print "Enter name of file containing learning set: "
learning_name = raw_input()
print "Enter name of file containing test set: "
test_name = raw_input()

learning_data = preprocess.parse(learning_name)
test_data = preprocess.parse(test_name)

"""
FEATURES
"""

learning_features = [[] for i in range(learning_data)]
test_features = [[] for i in range(test_data)]

for i in xrange(len(learning_features)):
  learning_features[i] = feature.parse(learning_data[i])

for i in xrange(len(test_features)):
  test_features[i] = feature.parse(test_data[i])

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

  
