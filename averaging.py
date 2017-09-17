import shelve
import xml.etree.ElementTree as ET
import urllib
import pandas as pd
import re

#https://www.librarything.com/ajax_newsearch.php?search=+The+Purpose+Driven+Life&searchtype=media

def calculate_avg(id) :

	avg_attr =[]

	result = pd.concat(userBookAttributeList)
	result = result.drop('titleOfBook', 1)

	f2 = pd.DataFrame(columns=result.columns)

	for column in result:
		avg_attr.append(result[column].mean())
	print avg_attr
	f2.loc[len(f2)] = avg_attr
	user_avg[id] = f2
	del avg_attr[:]
	
	
	

	



def remove_non_ascii(text):
   return ''.join([i if ord(i) < 128 else ' ' for i in text])

def work_on_the_book(txt):
    if d[txt] not in namelist :
    	if d[txt] not in namelist2 :
	    	print "bad miss"
    	else :
			attributeList = dpt.loc[dpt['titleOfBook'] == nameList2Dict[d[txt]]]
			userBookAttributeList.append(attributeList.head(1))
			
			
    else :
		attributeList = dpt.loc[dpt['titleOfBook'] == d[txt]]
		userBookAttributeList.append(attributeList.head(1))
		

dpt = pd.read_csv("data.csv")
namelist = dpt['titleOfBook'].tolist()
namelist2 = []
attributeList = []
userBookAttributeList = []
counter = 1
nameList2Dict = {}
userNumberOfBooks = {}
usefulprofiles = shelve.open("UsefulProfiles")
for name in namelist:
	m = re.match(r'\(([0-9]{4})\)',name[-6:])
	if m :
		namelist2.append(name[:-7])
		nameList2Dict[name[:-7]] = name


d = shelve.open("thedictionary")
user_avg = shelve.open("user_avg")
tree = ET.parse('treegen.xml')
root = tree.getroot()

for user in root :
   userId = user.get('id')
   bookstr = user[8].text;
   bookstr = remove_non_ascii(bookstr)
   if bookstr != 'N/A' :
      bookList = bookstr.split(',')
      for book in bookList :
 		f = { 'search' : book}
		cdj =  urllib.urlencode(f);
		shru = "https://www.librarything.com/ajax_newsearch.php?" + cdj +"&searchtype=media"
		if shru not in d :
			book = " " + book
			f = { 'search' : book}
			cdj =  urllib.urlencode(f);
			shru = "https://www.librarything.com/ajax_newsearch.php?" + cdj +"&searchtype=media"
			if shru not in d :
				f = { 'search' : book.lstrip()}
				cdj =  urllib.urlencode(f);
				shru = "https://www.librarything.com/ajax_newsearch.php?" + cdj +"&searchtype=media"
				if shru in d :
					work_on_the_book(shru)
				else :
					print("Not found", book)
			else :
				work_on_the_book(shru)
		else :
			work_on_the_book(shru)
		
      if len(userBookAttributeList) > 2 : 
      	calculate_avg(userId)
      del userBookAttributeList[:]
