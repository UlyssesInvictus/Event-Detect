import sys

import Utility as u
import Features as f
import Bayes as b
import os
import random

class Detector:
  def set_rares(self):
    # get filenames etc.
    print "Chose file to output to (leave blank to default to rares.txt):"
    rare_name = raw_input()
    rare_name = "rares.txt" if rare_name == "" else rare_name
    num_rares = 0
    while num_rares == 0:
      print "Choose number of rares:"
      try:
        num_rares = int(raw_input())
      except:
        print "Not a positive int."
      else:
        if num_rares < 1:
          print "Not a positive int."
          num_rares = 0
    print "Enter name of file containing learning set: "
    learning_name = "data/small_data.xlsx"#raw_input()
    try:
      learning_data = u.read_learning_data(learning_name,0)
    except:
      print "Error reading learning data. Check file and filename."
      return
    fields = list(learning_data[0])  
    num_fields = len(fields)
    num_nonevents = len(learning_data[0][fields[0]])
    num_events = len(learning_data[1][fields[0]])

    # create by frequency
    all_event_words = []
    all_nonevent_words = []
    # concat all words...this could take a while
    for k in ["message","subject"]:
      if type(learning_data[0][k][0]) is not list:
        continue
      for i in xrange(num_events):
        all_event_words = all_event_words + learning_data[1][k][i]
      for i in xrange(num_nonevents):
        all_nonevent_words = all_nonevent_words + learning_data[0][k][i]
    rares = f.get_rares(all_event_words,all_nonevent_words)
    rarefile = open('rares.txt','w')
    for rare,count in rares[0:num_rares]:
      rarefile.write(rare+'\n')
    rarefile.close()

  def learn(self,data=[], rare=""):

    """
    PREPROCESSING
    """
    if data == []: # for test 
      print "Enter name of file containing learning set: "
      learning_name = "data/test_data.xlsx"#raw_input()
      learning_data = u.read_learning_data(learning_name,0)
    else:
      learning_data = data
    fields = list(learning_data[0])
    num_fields = len(fields)
    num_nonevents = len(learning_data[0][fields[0]])
    num_events = len(learning_data[1][fields[0]])
    num_learning = num_nonevents+num_events

    if rare == "":
      print "Enter name of rare words file; leave blank to default to rares.txt"
      rare_name = "rares.txt"#"test.txt"#"human.txt"#"test.txt"#raw_input()
      if not os.path.isfile(rare_name):
        print "Rare file does not exist. Set rares or check filename."
        return
    else:
      rare_name = rare
    """
    FEATURES
    """

    # get rares 
    with open(rare_name) as rf:
      rares = rf.readlines()
    rares = [r.lower().rstrip() for r in rares]

    # get features
    learning_nonevent_features = [[] for i in xrange(num_nonevents)]
    learning_event_features = [[] for i in xrange(num_events)]

    for i in xrange(num_nonevents):
      for k in fields:
        learning_nonevent_features[i] = (learning_nonevent_features[i] + 
          f.get_features(learning_data[0][k][i], k, rares))

    for i in xrange(num_events):
      for k in fields:
        learning_event_features[i] = (learning_event_features[i] +
          f.get_features(learning_data[1][k][i], k, rares))


    """
    DISTRIBUTION STORAGE
    """

    # get prior
    prior = (num_events/float(num_learning),
      num_nonevents/float(num_learning))
    
    # get posterior
    event_by_features = u.by_features(learning_event_features)
    nonevent_by_features = u.by_features(learning_nonevent_features)
    event_posterior = [(b.mean(feature),b.stdev(feature)) for feature in event_by_features]
    nonevent_posterior = [(b.mean(feature),b.stdev(feature)) for feature in nonevent_by_features]

    # store in file
    distributionfile = open('distribution.txt','w')
    distributionfile.write("Prior (Event/Nonevent):\n")
    distributionfile.write(str(prior[0]) + " " + str(prior[1]) + "\n")
    distributionfile.write("Event posterior means: \n")
    for i in event_posterior:
      distributionfile.write(str(i[0]) + " ")
    distributionfile.write("\n")
    distributionfile.write("Event posterior stdevs: \n")
    for i in event_posterior:
      distributionfile.write(str(i[1]) + " ")
    distributionfile.write("\n")
    distributionfile.write("Nonevent posterior means: \n")
    for i in nonevent_posterior:
      distributionfile.write(str(i[0]) + " ")
    distributionfile.write("\n")
    distributionfile.write("Nonevent posterior stdevs: \n")
    for i in nonevent_posterior:
      distributionfile.write(str(i[1]) + " ")
    distributionfile.write("\n")
    distributionfile.close()

    # sklfile = open('skl.txt','w')
    # sklfile.write(str(num_events) + "\n")
    # sklfile.write(str(num_nonevents) + "\n")
    # for i in xrange(num_events):
    #   for j in learning_event_features[i]:
    #     sklfile.write(str(j) + " ")
    #   sklfile.write("\n")
    # for i in xrange(num_nonevents):
    #   for j in learning_nonevent_features[i]:
    #     sklfile.write(str(j) + " ")
    #   sklfile.write("\n")
    # sklfile.close()

  def guess(self,data=[], rare=""):

    """
    PREPROCESSING
    """

    if data == []:
      print "Enter name of file containing test set: "
      guess_name = "data/test_data.xlsx"#raw_input()
      guess_data = u.read_test_data(guess_name, 0)
    else:
      guess_data = data
    fields = list(guess_data)
    num_fields = len(fields)
    num_guesses = len(guess_data[fields[0]])

    if rare == "":
      print "Enter name of rare words file; leave blank to default to rares.txt"
      rare_name = "rares.txt"#"test.txt"#"human.txt"#"test.txt"#raw_input()
      if not os.path.isfile(rare_name):
        print "Rare file does not exist. Set rares or check filename."
        return
    else:
      rare_name = rare

    """
    CALCULATE TEST FEATURES
    """

    # get rares 
    with open(rare_name) as rf:
      rares = rf.readlines()
    rares = [r.lower().rstrip() for r in rares]

    guess_features = [[] for i in xrange(num_guesses)]
    for i in xrange(num_guesses):
      for k in fields:
        guess_features[i] = (guess_features[i] +
          f.get_features(guess_data[k][i], k, rares))

    """
    RETRIEVE DISTRIBUTION AND RUN BAYESIAN
    """

    if not os.path.isfile('distribution.txt'):
      print "Distribution not yet set. Run learn first."
      return

    try:
      distributionfile = open('distribution.txt','r')
      distributionfile.readline() # prior title
      prior = map(float, distributionfile.readline().split())
      distributionfile.readline() # event posterior means title
      event_means = map(float, distributionfile.readline().split())
      distributionfile.readline() # event posterior stdevs title
      event_stdevs = map(float, distributionfile.readline().split())
      distributionfile.readline() # nonevent posterior means title
      nonevent_means = map(float, distributionfile.readline().split())
      distributionfile.readline() # nonevent posterior stdevs title
      nonevent_stdevs = map(float, distributionfile.readline().split())
      distributionfile.close()

      event_posterior = [(event_means[i], event_stdevs[i]) for i in xrange(len(event_means))]
      nonevent_posterior = [(nonevent_means[i], nonevent_stdevs[i]) for i in xrange(len(nonevent_means))]
      two_posterior = (event_posterior,nonevent_posterior)
    except Exception as e:
      print e
      print "Problem reading distribution file. Rerun learn."
      return

    if len(guess_features[0]) != len(event_means):
      print "Number of features does not match distribution. Check test set and rerun learn."
      return

    # # guess!
    guesses = [b.two_bayesian(prior, i, two_posterior) for i in guess_features]


    # fi = open('skl.txt','r')
    # a = int(fi.readline().rstrip())
    # c = int(fi.readline().rstrip())
    # ef = [map(float, fi.readline().split()) for i in xrange(a)]
    # nef = [map(float, fi.readline().split()) for i in xrange(c)]
    # fi.close()
    # e = [1 for i in ef]
    # y = e + [0 for i in nef]
    # x = ef + nef
    # from sklearn.naive_bayes import MultinomialNB
    # clf = MultinomialNB()
    # clf.fit(x, y)
    # guesses = [clf.predict(i) for i in guess_features]

    """
    RESULTS
    """

    print "Is Event (First 40 Emails) | First 10 Words of Email Subject | First 10 Words of Email Body"
    for i in xrange(min(40,len(guesses))):
      subject = ' '.join(guess_data["subject"][i][:min(10,len(guess_data["subject"][i]))])
      message = ' '.join(guess_data["message"][i][:min(10,len(guess_data["message"][i]))]) 
      print guesses[i], " | ", subject, " | ", message

    # print "guesses: ", guesses
    # print "posteriror: ", two_posterior
    print "prior: ", prior

    return guesses

  def test(self, data, rare):

    """
    PREPROCESSING
    """

    # some useful variables

    fields = list(data[0])
    num_fields = len(fields)
    num_nonevents = len(data[0][fields[0]])
    num_events = len(data[1][fields[0]])
    num_data = num_nonevents + num_events
    num_test = num_data/3
    num_learning = num_data - num_test

    # randomly sample

    learning_indices = random.sample(xrange(num_data), num_learning)
    test_indices = list(set(xrange(num_data)) - set(learning_indices))

    learning_data = ({}, {})
    for field in fields:
      learning_data[0][field] = []
      learning_data[1][field] = []
    test_data = {}
    for field in fields:
      test_data[field] = []

    for i in learning_indices:
      for field in fields:
        if i < num_nonevents:
          learning_data[0][field].append(data[0][field][i])
        else:
          learning_data[1][field].append(data[1][field][i - num_nonevents])
    for i in test_indices:
      for field in fields:
        if i < num_nonevents:
          test_data[field].append(data[0][field][i])
        else:
          test_data[field].append(data[1][field][i - num_nonevents])

    """
    TESTING
    """

    # learn and guess

    self.learn(data=learning_data,rare=rare)
    guesses = self.guess(data=test_data,rare=rare)

    # TEST ONLY
    true_ids = [False if i < num_nonevents else True for i in test_indices]
    # print "trues: ", true_ids
    accuracy = u.get_accuracy(true_ids,guesses)
    print "accuracy: ", accuracy
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

    return (accuracy, num_right_true / float(num_real_true), num_right_false / float(num_real_false))


  def multi_test(self):

    print "Enter name of file containing data set: "
    data_name = "data/small_data.xlsx"#raw_input() 
    data = u.read_learning_data(data_name,0)

    print "Enter name of rare words file; leave blank to default to rares.txt"
    rare_name = "rares.txt"#"test.txt"#"human.txt"#"test.txt"#raw_input()
    if not os.path.isfile(rare_name):
      print "Rare file does not exist. Set rares or check filename."
      return

    num_tests = 0
    while num_tests == 0:
      print "Choose number of runs:"
      try:
        num_tests = int(raw_input())
      except:
        print "Not a positive int."
      else:
        if num_tests < 1:
          print "Not a positive int."
          num_tests = 0


    results = [(0,0,0) for i in xrange(num_tests)]
    acc_mean = 0
    true_mean = 0
    false_mean = 0

    print "Running " + str(num_tests) + " tests"

    for i in xrange(num_tests):
      print "Test **" + str(i) + "**" 
      results[i] = self.test(data=data, rare=rare_name)
      acc_mean+=results[i][0]
      true_mean+=results[i][1]
      false_mean+=results[i][2]

    print "Mean accuracy: ", acc_mean/(num_tests)
    print "Mean true: ", true_mean/(num_tests)
    print "Mean false: ", false_mean/(num_tests)

    return (acc_mean,true_mean,false_mean)

"""
===================================================================================================
"""
"""
ACTUALLY DO THINGS
"""
"""
===================================================================================================
"""

print "Welcome to Event-Detect, a CS51 Project"
d = Detector()

choice = 1

while choice != 0:
  print "Choose option:"
  print "1. Set rares: store most common event words for feature calculation using learning set"
  print "2. Learn: store prior and posteriors using learning set"
  print "3. Guess: make series of guesses using guess set"
  print "4. Test: Test accuracy of algorithm using a learning set"
  print "0. Exit"
  try:
    choice = int(raw_input())
  except:
    choice = -1

  if choice < 0  or choice > 4:
    print "Not a valid choice. Select again."
  else:
    if choice == 1:
      d.set_rares()
    elif choice == 2:
      d.learn()
    elif choice == 3:
      g = d.guess()
      print g
    elif choice == 4:
      d.multi_test()




