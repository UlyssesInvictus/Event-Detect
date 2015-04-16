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
Assumes certain csv structure TBD. Does not assume particular type of data in each column of csv, with exception of boolean identifying whether event or not. Same as read_learning_data, but doesn’t return tuple.
"""
def read_test_data(filename, numtypes):
  test_data = []
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
Input: array of words.
Output: dictionary of all words and number of appearances of word.
"""
def get_frequences(words):
  frequencies = {}
  return frequencies
