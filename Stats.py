from scipy import stats
import numpy
"""
input- list of lists (each sublist are the frequencies of a single word, each entry of sublist taken from an email)
output -  list of lists (each sublist contains p-values of frequencies for a word, each entry of sublist is an email)
Since we can only have positive number of emails, we expect our data to be right-skewed, this leads us to suggest that other non-Gaussian distributions would be a better model.
"""

def set_fit(freq_list):
    # initialize list
    lst = []
    # iterate through list of lists
    for x in freq_list:
        # initialize sublist
        sublst =[]
        # if skewed (.5 is arbitrary) use exponential
        if stats.skew(x)>.5:
            for y in x:
                sublst.append(1-stats.expon.cdf(y, 1/numpy.nanmean(x)))
        # if no variance, gaussian will not function, disregard this feature
        elif numpy.nanvar(x) == 0:
            sublst = [1]*len(x)
        # if unskewed generate p-value from Gaussian distribution
        else:
            for y in x:
                sublst.append(1-stats.norm.cdf(y, numpy.nanmean(x), numpy.nanvar(x)))
        # append sublists
        lst.append(sublst)
    return lst

"""
input- resulting probability vectors from different features
output- amalgamated probability vector, weighted correctly for final pass to Bayesian.
We will obtain probability information from each of our features, so we wish to provide a method to determine the weights of each one.
"""

def feature_weighter(prob_lsts):
  p = []
  return p