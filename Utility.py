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
  nonfullmessage = ["" for i in xrange(num_nonevents)]
  fullmessage = ["" for i in xrange(num_events)]
  non_subject = [[] for i in xrange(num_nonevents)]
  subject = [[] for i in xrange(num_events)]
  non_message = [[] for i in xrange(num_nonevents)]
  message = [[] for i in xrange(num_events)]

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
        subject[event_count] = ["no", "subject"]
      else:
        subject[event_count] = split_data(subject_raw)
      message_raw = (book.cell(row,3).value)
      if message_raw == "":
        message[event_count] = ["no", "message"]
      else: 
        message[event_count] = split_data(message_raw)
      fullmessage[event_count] = uni_to_ascii(message_raw)
      event_count += 1
    else:
      non_time[nonevent_count] = book.cell(row,0).value
      send_raw = book.cell(row,1).value
      non_sender[nonevent_count] = send_raw[send_raw.find("<")+1:send_raw.find(">")].encode('ascii','ignore') # assumes <"name"> sender format
      subject_raw = (book.cell(row,2).value)
      if subject_raw == "":
        non_subject[nonevent_count] = ["no", "subject"]
      else:
        non_subject[nonevent_count] = split_data(subject_raw)
      message_raw = (book.cell(row,3).value)
      if message_raw == "":
        non_message[nonevent_count] = ["no", "message"]
      else:
        non_message[nonevent_count] = split_data(message_raw)
      nonfullmessage[nonevent_count] = uni_to_ascii(message_raw)
      nonevent_count += 1

  # return tuple of dicts with each field type
  event_data = {'time':time, 'sender':sender, 'subject':subject, 'message':message, 'fullmessage':fullmessage}
  non_event_data = {'time':non_time, 'sender': non_sender, 'subject':non_subject, 'message':non_message, 'fullmessage':nonfullmessage}
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
  fullmessage = ["" for i in xrange(num_rows)]

  # iterate through excel, reading strings
  for row in xrange(1,num_rows+1):
    time[row-1] = book.cell(row,0).value
    send_raw = book.cell(row,1).value
    sender[row-1] = send_raw[send_raw.find("<")+1:send_raw.find(">")].encode('ascii','ignore') # assumes <"name"> sender format
    subject_raw = (book.cell(row,2).value)
    if subject_raw == "":
      subject[row-1] = ["no", "subject"]
    else:
      subject[row-1] = split_data(subject_raw)
    message_raw = (book.cell(row,3).value)
    if message_raw == "":
      message[row-1] = ["no", "message"]
    else:
      message[row-1] = split_data(message_raw)
    fullmessage = uni_to_ascii(message_raw)

  # return dict with each field type
  test_data = {'time':time, 'sender':sender, 'subject':subject, 'message':message, 'fullmessage':fullmessage}

  # print book.cell(42,3).value.encode('ascii','backslashreplace'), split_data(book.cell(42,3).value)

  return test_data


def read_event_ids(filename,numtypes):
  # open book
  workbook = xlrd.open_workbook(filename)
  book = workbook.sheet_by_index(0)

  # count number of events and nonevents
  num_rows = book.nrows - 1
  return [book.cell(row, numtypes).value for row in xrange(1,num_rows+1)]

"""
Input: unicode string
Output: ascii string, with punctuation appropriately transformed
"""
def uni_to_ascii(text):
  ascii_text = text.replace(u'\u2028', ' ') # bullet points
  ascii_text = ascii_text.replace(u'@', ' ')
  ascii_text = ascii_text.replace(u':', ' ')
  ascii_text = ascii_text.replace(u'\xa0', ' ') # spaces
  ascii_text = ascii_text.encode('ascii','ignore')
  return ascii_text

"""
Input: unicode string
Output: array of ascii words.
Assumes space separation, though amount of spaces may be unclear. Restricted to module.
"""
def split_data(text):
  ascii_text = uni_to_ascii(text)
  # replace punctuation and misc chars
  punc_list = string.punctuation.replace("'","")
  char_map = string.maketrans(punc_list, ' '*len(punc_list))
  ascii_text = ascii_text.translate(None,punc_list)

  return [x.lower() for x in ascii_text.split()]

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
Input: list of words.
Output: whether time like words are in email. Ignores forwarded and replied emails.
"""

def contains_time(words):
  times = []
  times = times + [str(i)+"am" for i in xrange(1,12)]
  times = times + [str(i)+"pm" for i in xrange(1,12)]
  times = times + ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
  times = times + ["january","february","march","april","may","june","july","august","september","october","november","december"]
  times = times + ["sun","sat","mon","tues","wed","thurs","fri"]
  times = times + ["sunday","saturday","monday","tuesday","wednesday","thursday","friday"]

  return not ("forward" in words or "forwarded" in words or "reply" in words) and any(i in words for i in times)
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
