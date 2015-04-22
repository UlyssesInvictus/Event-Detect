# Utilities file 
# CS51 Final Project 

# Utilities: Open and read input xlsx file. Parses by row. Returns the time, sender, subject, and message as a dict. 
# The subject and message are returned as a list of strings. The message is scrubbed of punctuation. 
# As requested by Jimmy, the entire thing is returned as a LIST OF DICTIONARIES 
    import xlrd
        
        def open(path):
        workbook = xlrd.open_workbook(path)
        book = workbook.sheet_by_index(0)  
        # get the first worksheet
        # Step 2: split_words (Split string of words in an array using spaces as delimiter. Strip punctuation) 
        import string
        remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        dlist=[]
        for x in xrange(1,10):
            time= book.cell(x,0).value
            sender= book.cell(x,1).value[book.cell(x,1).value.find("<")+1:book.cell(x,1).value.find(">")].encode('ascii','ignore')
            subject= (book.cell(x,2).value).translate(remove_punctuation_map).encode('ascii','ignore').split() 
            message= (book.cell(x,3).value).translate(remove_punctuation_map).encode('ascii','ignore').split() 
            dlist.append(dict(message=message,subject=subject,sender=sender,time=time))
        print(dlist)



