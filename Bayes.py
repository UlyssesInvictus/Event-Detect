import Stats as s
from operator import mul
import math
from scipy.stats import norm
from scipy.stats import expon

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

def per_height(x, mean, stdev):
  x_exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
  x_height = (1 / (math.sqrt(2*math.pi) * stdev)) * x_exponent
  m_height = (1 / (math.sqrt(2*math.pi) * stdev))
  return x_height

def cdf(x,mean,variance):
  # return norm.cdf(x,loc=mean,scale=stdev)
  return expon.cdf(x,loc=0,scale=1/mean)

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
	# filtered=[]
	# event_prob = []
	# non_event_prob = []
	# for i in range(len(bit_features)):
	# 	if bit_features[i] == True:
	# 		filtered.append(posterior[i])
	# for (event, non_event) in filtered:
	# 	event_prob.append(event)
	# 	non_event_prob.append(non_event)
	# x = reduce(mul, event_prob, 1)
	# y = reduce(mul, non_event_prob, 1)
	# return prior[0]*x > prior[1]*y
  
  event_prob = [0 for i in xrange(len(features))]
  nonevent_prob = [0 for i in xrange(len(features))]
  for i in xrange(len(features)):
    if posterior[0][i][1] == 0:
      if features[i] != 0:
        event_prob[i] = 0.00001
      else:
        event_prob[i] = 1
    else:
      event_prob[i] = per_height(features[i],posterior[0][i][0],posterior[0][i][1])
    if posterior[1][i][1] == 0:
      if features[i] != 0:
        nonevent_prob[i] = 0.00001
      else:
        nonevent_prob[i] = 1
    else:
      nonevent_prob[i] = per_height(features[i],posterior[1][i][0],posterior[1][i][1])


  event_total = prior[0]*reduce(mul, event_prob, 1)
  nonevent_total = prior[1]*reduce(mul, nonevent_prob, 1)
 
  print event_total, nonevent_total
  return event_total > nonevent_total
  

def one_bayesian (prior, features, posterior):
  event_prob = [0 for i in xrange(len(features))]
  nonevent_prob = [0 for i in xrange(len(features))]
  for i in xrange(len(features)):
    if posterior[i][1] == 0:
      event_prob[i] = 1
      nonevent_prob[i] = 1
    else:
      prob = cdf(features[i], posterior[i][0], posterior[i][1])
      event_prob[i] = prob
      nonevent_prob[i] = 1 - prob

  event_total = prior[0] * reduce(mul, event_prob, 1)
  nonevent_total = prior[1] * reduce(mul, nonevent_prob, 1)
 
  print event_total, nonevent_total
  return event_total > nonevent_total
