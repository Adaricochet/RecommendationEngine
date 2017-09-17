#!/usr/bin/python
def remove_non_ascii(text):
   return ''.join([i if ord(i) < 128 else ' ' for i in text])

import xml.etree.ElementTree as ET
import urllib
from bs4 import BeautifulSoup
import urllib2
import ssl
import json

bookset = set();
urllist = [];
tree = ET.parse('treegen.xml')
root = tree.getroot()
for child in root:
   bookstr = child[8].text;
   bookstr = remove_non_ascii(bookstr)
   bookstr = str(bookstr.encode('utf-8').decode('ascii', 'ignore'))
   if bookstr != 'N/A' :
      bookList = bookstr.split(',')
      for book in bookList :
         bookset.add(book)
f1=open('./testfile3', 'w+')
f1.write(str(bookset))
for child in bookset:
   f = { 'search' : child}
   cdj =  urllib.urlencode(f);
   shru = "https://www.librarything.com/ajax_newsearch.php?" + cdj +"&searchtype=media"
   urllist.append(shru);
root = ET.Element("root")
doc = ET.SubElement(root, "doc")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
k =0;
for u in urllist :
   k= k+1
   rf = urllib2.urlopen(u,context = ctx)
   rEnc = rf.read()
   rEnc = json.loads(rEnc);
   rHtml = rEnc['text'].decode('base64')
   rf.close()
   soup1 = BeautifulSoup(rHtml,"html.parser")
   if soup1.table :
      one = soup1.find_all('tr')
      td = one[0].find_all('td')
      a = td[0].find_all('a')
      #print a[0]['href']
      path = "https://www.librarything.com" + a[0]['href']
      redditFile = urllib2.urlopen(path,context = ctx)
      redditHtml = redditFile.read()
      redditFile.close()
      
      soup = BeautifulSoup(redditHtml,"html.parser")
      book = ET.SubElement(doc,"book",author= soup.h2.text,title =soup.h1.text,urlgenerated =u);
      
      url = 'https://www.librarything.com/ajaxinc_showbooktags.php'

      values = {'work' : a[0]['href'][6:],
          'all' : '0',
          'print' : '1' ,
          'doit':'1',
          'lang':''}
      user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
      headers = { 'User-Agent' : user_agent }
      data = urllib.urlencode(values)
      req = urllib2.Request(url, data, headers)
      response = urllib2.urlopen(req,context=ctx)
      the_page = response.read()
      soup2 = BeautifulSoup(the_page,"html.parser")
      f = open('xyz.txt','w+')
      f.write(the_page)
      f.close()
      myspans = soup2.findAll("span", { "class" : "tag" })
      
      for span in myspans:
         #print span
         book_attr = span.text.split('(')[0].strip();
         attr_count =span.text.split('(')[1][0];
         ET.SubElement(book,"attribute",count = attr_count).text = book_attr;
      
   if k == 10 :
      tree = ET.ElementTree(root)
      tree.write("xml_datasheet.xml")
      k=0
      
tree = ET.ElementTree(root)
tree.write("xml_datasheet.xml")
