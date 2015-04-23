import Stats.py as s
from operator import mul

def get_posterior:


def bayesian (prior, posterior):
	event_prob = []
	non_event_prob = []
	for (event, non_event) in posterior:
		event_prob.append(event)
		non_event_prob.append(non_event)
	x = reduce(mul, event_prob, 1)
	y = reduce(mul, non_event_prob, 1)
	return prior[0]*x > prior[1]*y