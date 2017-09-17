import xml.etree.ElementTree as ET
import urllib
from bs4 import BeautifulSoup
import urllib2
import ssl
import json
import eventlet
import shelve
def remove_non_ascii(text):
   return ''.join([i if ord(i) < 128 else ' ' for i in text])


d = shelve.open("thedictionary")
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

for child in bookset:
   f = { 'search' : child}
   cdj =  urllib.urlencode(f);
   shru = "https://www.librarything.com/ajax_newsearch.php?" + cdj +"&searchtype=media"
   urllist.append(shru);

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for u in urllist :

   rf = urllib2.urlopen(u,context = ctx)
   rEnc = rf.read()
   rEnc = json.loads(rEnc);
   rHtml = rEnc['text'].decode('base64')
   rf.close()
   soup1 = BeautifulSoup(rHtml,"html.parser")
   if soup1.table :
      one = soup1.find_all('tr')
      td = one[0].find_all('td')
      a = td[1].find_all('a')
      d[u] = a[0].text
