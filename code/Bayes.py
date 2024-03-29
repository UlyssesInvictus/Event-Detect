import Stats as s
from operator import mul
import math
from scipy.stats import norm
from scipy.stats import expon
import random

def mean(numbers):
  return sum(numbers)/float(len(numbers))

def stdev(numbers):
  avg = mean(numbers)
  variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
  return math.sqrt(variance)

def variance(numbers):
  avg = mean(numbers)
  variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
  return variance

def height(x, mean, stdev):
  x_exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
  x_height = (1 / (math.sqrt(2*math.pi) * stdev)) * x_exponent
  return x_height

"""
Purely for learning phase
"""

def get_posterior (event_vec, non_event_vec):
  zipped = zip(event_vec, non_event_vec)
  post= []
  for (a, b) in zipped:
    if a+b == 0.0:
      post.append((0.5,0.5))
    else:
      post.append((float(a)/(a+b), float(b)/(a+b)))
  return post


"""
input: 
    prior: tuple, entry one is prior prob of event, entry two is prior prob of non_event
    bit_features: features vector
		posterior: list of tuples, entry one of tuple is penalty for event, entry two
					is penalty for non_event
output: bool for event
"""
def two_bayesian (prior, features, posterior):
 
  event_prob = [0 for i in xrange(len(features))]
  nonevent_prob = [0 for i in xrange(len(features))]
  for i in xrange(len(features)):
    if posterior[0][i][1] == 0:
      if features[i] != 0:
        event_prob[i] = 0.000001
      else:
        event_prob[i] = 1
    else:
      event_prob[i] = 20*height(features[i],posterior[0][i][0],posterior[0][i][1])
    if posterior[1][i][1] == 0:
      if features[i] != 0:
        nonevent_prob[i] = 0.000001
      else:
        nonevent_prob[i] = 1
    else:
      nonevent_prob[i] = 20*height(features[i],posterior[1][i][0],posterior[1][i][1])


  event_total = prior[0]*reduce(mul, event_prob, 1)
  nonevent_total = prior[1]*reduce(mul, nonevent_prob, 1)
 
  # print event_total, nonevent_total
  return event_total > nonevent_total 

