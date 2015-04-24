import xlrd
import string
from collections import defaultdict

"""
Input: filename of learning data and number of columns of email data
Output: Tuple of arrays of arrays of email data. First element in tuple represents event emails. Second element represents non-event emails.
Assumes certain csv structure to be detailed. Does not assume particular type of data in each column of csv, with exception of boolean identifying whether event or not.
"""
def read_learning_data(filename, numtypes):
  # open book
  workbook = xlrd.open_workbook(filename)
  book = workbook.sheet_by_index(0)

  # count number of events and nonevents
  num_rows = book.nrows - 1
  num_events = 0
  num_nonevents = 0
  for row in xrange(1,num_rows+1):
    if book.cell(row,4).value == 1:
      num_events += 1
    else:
      num_nonevents += 1

  # initalize keys
  non_time = ["" for i in xrange(num_nonevents)]
  time = ["" for i in xrange(num_events)]
  non_sender = ["" for i in xrange(num_nonevents)]
  sender = ["" for i in xrange(num_events)]
  non_subject = [[] for i in xrange(num_nonevents)]
  subject = [[] for i in xrange(num_events)]
  non_message = [[] for i in xrange(num_nonevents)]
  message = [[] for i in xrange(num_events)]

  remove_punctuation_map = dict((ord(char), ord(" ")) for char in string.punctuation)
  del remove_punctuation_map[ord("'")]

  # iterate through excel, reading strings
  event_count = 0
  nonevent_count = 0
  for row in xrange(1,num_rows+1):
    if book.cell(row,4).value == 1:
      time[event_count] = book.cell(row,0).value
      send_raw = book.cell(row,1).value
      sender[event_count] = send_raw[send_raw.find("<")+1:send_raw.find(">")].encode('ascii','ignore') # assumes <"name"> sender format
      subject_raw = (book.cell(row,2).value)
      if subject_raw == "":
        subject[event_count] = ["no", "sender"]
      else:
        subject[event_count] = [x.lower() for x in subject_raw.translate(remove_punctuation_map).encode('ascii','ignore').split()]
      message_raw = (book.cell(row,3).value)
      if message_raw == "":
        message[event_count] = ["no", "message"]
      else: 
        message[event_count] = [x.lower() for x in message_raw.translate(remove_punctuation_map).encode('ascii','ignore').split()]
      event_count += 1
    else:
      non_time[nonevent_count] = book.cell(row,0).value
      send_raw = book.cell(row,1).value
      non_sender[nonevent_count] = send_raw[send_raw.find("<")+1:send_raw.find(">")].encode('ascii','ignore') # assumes <"name"> sender format
      subject_raw = (book.cell(row,2).value)
      if subject_raw == "":
        non_subject[nonevent_count] = ["no", "sender"]
      else:
        non_subject[nonevent_count] = [x.lower() for x in subject_raw.translate(remove_punctuation_map).encode('ascii','ignore').split()]
      message_raw = (book.cell(row,3).value)
      if message_raw == "":
        non_message[nonevent_count] = ["no", "message"]
      else:
        non_message[nonevent_count] = [x.lower() for x in message_raw.translate(remove_punctuation_map).encode('ascii','ignore').split()]
      nonevent_count += 1

  # return tuple of dicts with each field type
  event_data = {'time':time, 'sender':sender, 'subject':subject, 'message':message}
  non_event_data = {'time':non_time, 'sender': non_sender, 'subject':non_subject, 'message':non_message}
  return (non_event_data, event_data)

"""
Input: filename of test data and number of columns of email data
Output: Array of arrays of email data.
Assumes certain csv structure TBD. Does not assume particular type of data in each column of csv, with exception of boolean identifying whether event or not. Same as read_learning_data, but doesn't return tuple.
"""

def read_test_data(filename, numtypes):
  # open book
  workbook = xlrd.open_workbook(filename)
  book = workbook.sheet_by_index(0)

  # initalize keys in the final dictionary
  num_rows = book.nrows - 1
  time = ["" for i in xrange(num_rows)]
  sender = ["" for i in xrange(num_rows)]
  subject = [[] for i in xrange(num_rows)]
  message = [[] for i in xrange(num_rows)]

  # for converting punctuation
  remove_punctuation_map = dict((ord(char), ord(" ")) for char in string.punctuation)
  del remove_punctuation_map[ord("'")]

  # iterate through excel, reading strings
  for row in xrange(1,num_rows+1):
    time[row-1] = book.cell(row,0).value
    send_raw = book.cell(row,1).value
    sender[row-1] = send_raw[send_raw.find("<")+1:send_raw.find(">")].encode('ascii','ignore') # assumes <"name"> sender format
    subject_raw = (book.cell(row,2).value)
    subject[row-1] = [x.lower() for x in subject_raw.translate(remove_punctuation_map).encode('ascii','ignore').split()]
    message_raw = (book.cell(row,3).value)
    message[row-1] = [x.lower() for x in message_raw.translate(remove_punctuation_map).encode('ascii','ignore').split()]

  # return dict with each field type
  test_data = {'time':time, 'sender':sender, 'subject':subject, 'message':message}
  return test_data


def read_event_ids(filename,numtypes):
  # open book
  workbook = xlrd.open_workbook(filename)
  book = workbook.sheet_by_index(0)

  # count number of events and nonevents
  num_rows = book.nrows - 1
  return [book.cell(row, numtypes).value for row in xrange(1,num_rows+1)]

"""
Input: string
Output: array of words.
Assumes space separation, though amount of spaces may be unclear. To be further specified later in work pipeline. Restricted to module.
"""
def split_data(text):
  words = []
  return words

"""
Input: list of words.
Output: dictionary of all words and number of appearances of word.
"""
def get_frequencies(words):
  freq_dict = defaultdict( int )
  for word in words:
    freq_dict[word] += 1
  return dict(freq_dict)

"""
Input: matrix of numbers
Output: array with same length as matrix where elements are vertically summed
"""
# To be replaced by numpy eventually
def vertical_sum(matrix):
  s = [0 for i in range(len(matrix[0]))]
  for i in range(len(matrix[0])):
    for j in range(len(matrix)):
      s[i] += matrix[j][i]
  return s

"""
Input: array of feature vectors per email
Output: array of arrays of values for same feature
"""

def by_features(matrix):
  return zip(*matrix)

"""
Input: array of testing email data, array of output classifications
Output: float representing the percent accuracy of the classifier
"""

def get_accuracy(true_id, classified_id):
  hits = 0
  for i in range(len(true_id)):
    if true_id[i] == classified_id[i]:
      hits += 1
  return (float(hits) / len(true_id))
