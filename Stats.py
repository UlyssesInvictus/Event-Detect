
"""
input- array of arrays (each subarray are the frequencies of a single word)
output - vector of bools for appropriate distribution (considering option of Gaussian or Exponential) 
Since we can only have positive number of emails, we expect our data to be right-skewed, this leads us to suggest that other non-Gaussian distributions would be a better model.
"""
def set_fit(stuff):
  bool_stuff = []
  return bool_stuff

"""
input- resulting probability vectors from different features
output- amalgamated probability vector, weighted correctly for final pass to Bayesian.
We will obtain probability information from each of our features, so we wish to provide a method to determine the weights of each one.
"""

def feature_weighter(bools):
  p = []
  return p