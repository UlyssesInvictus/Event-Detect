# Event-Detect

# Project: Email NLP
CS51 Final Project to detect emails containing events. Inspired by HCS Mail projects.

## Team members: 
-Frances Ding		francesding@college.harvard.edu 
-Raynor Kuang		raynorkuang@college.harvard.edu 
-Jimmy Lin		hlin01@college.harvard.edu 
-Daniel Wang 		danielwang01@college.harvard.edu 


## Overview 
Harvard students receive dozens of emails on a daily basis, many of which contain important event information but are ultimately lost in an overcrowded inbox. To address this problem, we plan to implement a natural language processor that will detect and flag email information related to Harvard campus events. Our flagging system will make use of naive Bayesian filters to detect key words and phrases associated with events on campus. We will be making use of Harvard Computer Society’s email listserv data to test our code, and to make necessary adjustments to the filtering specifications of the language processor. Our overarching goal for this project is to be able to 

## Features List

### Core features

-Flag emails which contain event information

### Cool extensions
-Delete or lump together emails that are identical but from different senders
-Extract event information from emails publicizing events and construct a calendar

## Technical Specifications 

## Next Steps 
We decided to write our project in python so the first step will be a brief python walkthrough for our group members who are unfamiliar with the language. We are all committing an hour to reading through a basic python tutorial linked here (http://www.stavros.io/tutorials/python/). We will be establishing basic checkups with each other before merging any branches to master and laying down ground rules on documenting our code. 
Logistics aside, we will be reading through documentation and work on simple Bayesian functions to get an idea of how we want to implement event detection from emails. We are committing to reading through the introductory portions here (http://en.wikipedia.org/wiki/Naive_Bayes_classifier#Probabilistic_model ) and to read through the simple examples in this presentation (http://www.cs.ucr.edu/~eamonn/CE/Bayesian%20Classification%20withInsect_examples.pdf ). We will be looking into how to implement this algorithmically as well as developing intuition as to how we should weight our data based on keywords, the presence of dates, 

We will also be looking into creating a testing csv from either our own emails or from Harvard Computer Society’s data retrieved from Mailman.
Additionally we will have our github repository set up by the end of this week.



