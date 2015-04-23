import xlrd
import string
from collections import defaultdict

"""
Input: filename of learning data and number of columns of email data
Output: Tuple of arrays of arrays of email data. First element in tuple represents event emails. Second element represents non-event emails.
Assumes certain csv structure to be detailed. Does not assume particular type of data in each column of csv, with exception of boolean identifying whether event or not.
"""
def read_learning_data(filename, numtypes):
  event_data = []
  unevent_data = []
  return (event_data,unevent_data)

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
  full_list = []
  freq_dict= defaultdict( int )
  for word in words:
    freq_dict[word] += 1
  return freq_dict
