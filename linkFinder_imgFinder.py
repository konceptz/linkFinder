import time
import re
import sys

from urllib2 import urlopen, HTTPError
from optparse import OptionParser
#from bs4 import BeautifulSoup as bs
from optparse import OptionParser
from urlparse import urlparse
import requests

def main():
	while (True):
		input_site = raw_input('Enter website (ex: http://newsite.qa.aistg.com) : ')
			#clean input or end program
		if input_site == 'quit':
			sys.exit()

		#check valid site
		if check(input_site):
			break
		print ('Invalid host address.  Please re-enter or type quit to end.')

	#Get all links on site
	choice = raw_input('(1)To search Images\n(2)To search Links\n: ')
	if choice == '1':
		links = getLinks(input_site, 'IMG')
	if choice == '2': 
		links = getLinks(input_site, 'LINK')

	print ('Number of links found: ' + str(len(links)))		
	#lets format the output nicely

 	returncodes = {}
   	x = 1
   	y = len(links)
   	t0 = time.clock()
  
    
   	for link in links:
# when there is a 403 like code it assigns it to 0       
   	    try:    
   	        code = urlopen(link).getcode()
   	    except HTTPError as e :
            #print e.__class__.__name__
            #print e.code
   	        print('error %d from %s' %(e.code, link))
            # %S is string and %d decimal look up others
   	        code = e.code
   	    except:
   	        code= 0
              
   	    if code in returncodes:
   	        returncodes[code].append(link)
   	    else: 
   	        returncodes[code] = [link]   
   	    print('Checking URL %d of %d' %(x,y))
   	    x+=1
   	print('took %d secs' % (time.clock() - t0))
    #returns the httpstatus codes that were seen
   	print(returncodes.keys())
   	httpstatus = None
    #loop to allow the user to print the urls by status code
   	while httpstatus != 'quit':      
   	    httpstatus = raw_input('Enter status code that is avalible or type quit spelling counts :P: ')
   	    
   	    if httpstatus == 'url':
   	    	main()
   	    elif httpstatus =='quit':
        	print 'exiting'
   	    else:
   	        try:    
   	            #print(returncodes[int(httpstatus)] ) 
   	            for lines in returncodes[int(httpstatus)]:
   	            	print lines
   	        except:
   	            print('Invalid Input')
	#main done


#Boolean check for valid website
def check(url_string):
	if urlopen(url_string).getcode() == 200:
		return True
	else:
		return False


#Returns a list of links on a site
#abstracted in case we want to process HTML in a different way, later
def getLinks(url_string, type_of_link):
	return process(url_string, type_of_link)
	    
#cleans links
def clean(pattern, url):
	urls = {}
	instances = 0
	for link in pattern:
		if link[0:2] == '//':
			print('URL does not specify host, prepending http:')
			link = 'http:'+link
		elif link[0] == '/':
			print('URL does not specify host, prepending '+urlparse(url).hostname)
			link = 'http://'+urlparse(url).hostname+link

        urls[link] = True
        instances += 1
        print('%d Found link %s' % (instances, link))
	return urls

#Process html into dictionary
def process(url, type_of_link):
    #url = host+page
    print('Opening %s...' % url)
    #scrapes the page source
    content = urlopen(url).read()

    print('Compiling RegExp...')
    if type_of_link == 'LINK':
    	print("link processing RegEx")
    	pattern = re.compile(r'<a .*?href=["|\'](?!#)(.+?)["\']');
    elif type_of_link == 'IMG':
    	print("IMG processing for Regex")
    	pattern = re.compile(r'<img .*?src=["|\'](?!#)(.+?)["\']');
    # we can avoid duplicates by using a hash - will save time later
    urls = {}
    instances = 0
    for link in pattern.findall(content):

        if link[0:2] == '//':
            print('URL does not specify host, prepending http:')
            link = 'http:'+link
        elif link[0] == '/':
            print('URL does not specify host, prepending '+urlparse(url).hostname)
            link = 'http://'+urlparse(url).hostname+link

        urls[link] = True
        instances += 1
        print('%d Found link %s' % (instances, link))
        
        
    print('Found %d links with %d unique URLs' % (instances, len(urls)))
#list of urls
    return urls.keys()
  
main()




#This is useless but can server as a soup way to process HTML
"""
def tight(soup, type_of_link):
	print("Tight HTML Processing for " +type_of_link)
	links = {}
	if type_of_link == 'IMG':
		print ("Getting all <src img> links and testing link status")
		links = [x['src'] for x in content_soup.findAll('img')] #unclean links list
	if type_of_link == 'LINK':
		print ("Getting all <a href> links and testing link status")
		links = [x['href'] for x in content_soup.findAll('a')] 
	cleaned = clean(links, urlparse(url_string).hostname)
	return cleaned
"""


#Previously Used way to check for valid URL.  Now we pass to urlopen and get code.
#So the internet checks for valid url instead of manual regex.
"""
#testes the url to make sure it is valid From Tim b
def check(test_str):
    pattern = r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))'
    if not re.search(pattern, test_str):
        valid = False
        print 'Invalid url format : %r' % (test_str,)
    else:
        print 'Valid url format   : %r' % (test_str,)
        valid = True
    return valid
"""
