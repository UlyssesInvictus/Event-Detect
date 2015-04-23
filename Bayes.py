import Stats.py as s
from operator import mul

def get_posterior (event_vec, non_event_vec):
	zipped = zip(event_vec, non_event_vec)
	post= []
	for (a, b) in zipped:
		post.append((a/(a+b), b/(a+b)))
	return post


"""
input - prior: list, entry one is prior prob of event, entry two is prior prob of non_event
		posterior: list of tuples, entry one of tuple is penalty for event, entry two
					is penalty for non_event
output- bool for event
"""
def bayesian (prior, posterior):
	event_prob = []
	non_event_prob = []
	for (event, non_event) in posterior:
		event_prob.append(event)
		non_event_prob.append(non_event)
	x = reduce(mul, event_prob, 1)
	y = reduce(mul, non_event_prob, 1)
	return prior[0]*x > prior[1]*y