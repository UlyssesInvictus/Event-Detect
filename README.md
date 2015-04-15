# Event-Detect

# Project: Email NLP
CS51 Final Project to detect emails containing events. Inspired by HCS Mail projects.

## Table of Contents
1. [Team members](#team-members)
2. [Overview](#overview)
3. [Features List](#features-list)
  - [Core features](#core-features)
  - [Cool extensions](#cool-extensions)
4. [Technical Specifications](#technical-specifications)
  - [Preprocessing](#preprocessing)
  - [Features Selection](#features-selection)
  - [Naive Bayesian Classification](#naive-bayesian-classification)
5. [Next Steps](#next-steps)
6. [Notes and Useful Links](#notes-and-useful-links)

## Team members 
- Frances Ding		francesding@college.harvard.edu 
- Raynor Kuang		raynorkuang@college.harvard.edu 
- Jimmy Lin		hlin01@college.harvard.edu 
- Daniel Wang 		danielwang01@college.harvard.edu 


## Overview 
Harvard students receive dozens of emails on a daily basis, many of which contain important event information but are ultimately lost in an overcrowded inbox. To address this problem, we plan to implement a natural language processor that will detect and flag email information related to Harvard campus events. Our flagging system will make use of naive Bayesian filters to detect key words and phrases associated with events on campus. We will then use Harvard Computer Society’s email listserv data to train, evaluate, and make necessary adjustments to the filtering specifications of the language processor. Our overarching goal for this project is to be able to construct a naive Bayesian filter capable of reliably predicting and flagging texts with event-related information. As the focus of the project is implementing the filter, the flagged data will be outputted in the same format as the input. We hope our solution will provide an algorithmically interesting and applicable tool for Harvard Computer Society, as well as students and staff. 

## Features List

### Core features

- Pre-training
  - Training data will be hand-labeled collections of emails categorized as “event” or “non-event”, gathered from personal accounts and HCS servers
  - Classifier algorithm will be implemented as a naive Bayes classifier
as demonstrated [here] (http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/)
  - Using a probabilistic determination based on keyword occurrence to categorize “event” or “non-event”
- Post-training
  - Accept a CSV file of email text data to be analyzed
  - Flag emails which contain event information
  - Output the event emails in some format, to be determined later depending on design and ease-of-use decisions

### Cool extensions
- Include other headers (To:, From:, MIME data, etc.) in features building so that classifier uses this data as well
- Delete or lump together events in identical emails but from different senders so that the output is concise
- Extract event information, such as date, time, and location, from emails publicizing events and construct a calendar
further categorize events via the naive Bayesian classifier as “free food providing” or not
- Implement a different algorithm for the classifier and compare performance
  - Naive Bayes vs. SVM
- Use professionally developed classifier with our features selector to test possible improvements

## Technical Specifications 
### Preprocessing
- Learning data: manually store a good number of emails as learning data for the classifier (this is the boring part split amongst everyone)
- Should be stored as a .csv with two columns: string of email and boolean of is_event
- Small fraction to be fed into features builder; bigger fraction to be fed into features selection and classifier; all to eventually be fed in as proof of concept

### Features Selection
- Convert a string (email body) into vector of features  
- Function: parse text for words it does contain
  - Sub-function: build boolean vector marking that presence
  - Potentially very long for very long emails; better strategy may be to just check for “signal” words as below?
  - Function not for use outside module
- Function: count number of appearances of certain signal words
  - Sub-function: build int vector counting those words
  - Human part: deciding what those signal words are
  - Function not for use outside module 
- Function: output features vector using above functions as subroutines
  - Function for use outside module in Bayesian
  - Not final: potentially incorporate other features?

### Naive Bayesian Classification
- Routine: partitioning data
  - Receive .csv from preprocessing and partition into:
    - Learning data: small, representative sample of event emails for training classifier
    - Test data: medium, representative sample of emails to test learned classifications
      - Manually modify features selection if this result is inadequate
    - Fresh data: large, unknown sample of emails to test final classifier on (i.e. release software)
- Function: applying features selection
  - Convert features vectors into single vector for use by classifier
  - Not for use outside module
- Functions: statistical values
  - Function: Mean
    - Convert features vector into vector of means
  - Function: Standard deviation
    - Convert features vector into vector of st. devs.
  - Routine: partition these vectors by class (i.e. overall measures for event and non-event emails)
  - Not for use outside module except as interesting statistic visualization
- Routine: calculate probabilities of each attribute (the “training”)
  - Function: calculate Gaussian probability density function for a certain mean and st. dev.
  - Routine: calculate for all attribute/class combination (i.e. entire features vector for both event and non-events)
  - Routine: combine Gaussian probabilities into probability of event/non-event for each feature
- Function: prediction
  - Make predictions based on probabilities to features vectors of test data
  - Potentially exportable as a function for use in other projects
- Function: accuracy
  - Compare predictions to actual measures of test data
  - Build better features or increase learning set size if accuracy poor
  - Not for use outside module	



## Next Steps 
We decided to write our project in python so the first step will be a brief python walkthrough for our group members who are unfamiliar with the language. We are all committing an hour to reading through a basic python tutorial linked [here](http://www.stavros.io/tutorials/python/). We will be establishing basic checkups with each other before merging any branches to master and laying down ground rules on documenting our code. 

Logistics aside, we will be reading through documentation and work on simple Bayesian functions to get an idea of how we want to implement event detection from emails. We are committing to reading through the introductory portions [here](http://en.wikipedia.org/wiki/Naive_Bayes_classifier#Probabilistic_model) and to read through the simple examples in [this presentation](http://www.cs.ucr.edu/~eamonn/CE/Bayesian%20Classification%20withInsect_examples.pdf). We will be looking into how to implement this algorithmically as well as developing intuition as to how we should weight our data based on keywords, the presence of dates, or other such indicators.

In particular, we will be deciding what “features” of event-like email can be most easily and accurately represented in features vectors for use in the Bayesian classifier.

We will also be looking into creating a testing csv from either our own emails or from Harvard Computer Society’s data retrieved from Mailman.

## Notes and Useful Links 

[http://www.nltk.org/book/ch06.html](http://www.nltk.org/book/ch06.html)

Textbook chapter describing how to perform classification. Sections 1 (introduction) and 5 (Bayes Classification) are particularly useful. Accompanying NLTK package (Natural Language Toolkit) is also useful as reference point for our code.

[http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/](http://machinelearningmastery.com/naive-bayes-classifier-scratch-python/)

A guide to developing a Bayes classifier from scratch, with example data and code.

[https://github.com/codebox/bayesian-classifier](https://github.com/codebox/bayesian-classifier)

A developed package for Bayesian classification. Many nice UI features. Useful as a reference.

[https://pypi.python.org/pypi/Bayesian/0.3.1](https://pypi.python.org/pypi/Bayesian/0.3.1)

Also a developed package for Bayesian classification, but with worse UI.


