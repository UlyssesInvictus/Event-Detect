# Event-Detect
CS51 Final Project to detect emails containing events. Inspired by HCS Mail projects.
## Timeline
|Date|Description|
|:--|--:|
|Monday April 20th|Have Data/Learning sets ready|
|Tuesday April 21st|Data Preprocessing/Utility written|
|Wednesday April 22nd|Some features implemented|
|Thursday April 23rd|Bayesian outputs relatively accurate results|
|Friday April 24th |Code clean for functionality checkin|
|Monday April 27th|Rare word feature|
|Tuesday April 28th|More sophisticated distribution selection|
|Wednesday April 29th|Video Work and additional features|
|Thursday April 30th| Code Clean and Ready for Submission|
##Module Descriptions and Updates
###Statistics Module
4-21
Wrote set_fit, behavior is described in comments. Currently, set_fit selects "appropriate" distributions and returns respective p-values for a list of lists of word frequencies. If required, I will modify to return bools and distribution params for learning.
