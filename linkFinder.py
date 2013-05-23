import time
import re
import sys
import lxml.etree
import lxml.builder
import msvcrt as m

from xml.dom.minidom import parse, parseString

from urllib2 import urlopen, HTTPError
from optparse import OptionParser
#from bs4 import BeautifulSoup as bs
from optparse import OptionParser
from urlparse import urlparse
#mport requests



def main():
  global input_site 
  global inputType
  input_bool = getFile()
  while (input_bool == False):
    input_site = raw_input('Enter website (ex: http://newsite.qa.aistg.com) : ')
		#clean input or end program
    if input_site == 'quit':
			sys.exit()

		#check valid site
    if check(input_site):
			break

    print ('Invalid host address.  Please re-enter or type quit to end.')

	#Get all links on site
  inputType = raw_input('(1)To search Images\n(2)To search Links\n: ')
  if inputType == '1':
    links = getLinks(input_site, 'IMG')
  elif inputType == '2': 
    links = getLinks(input_site, 'LINK')

  print ('Number of links found: ' + str(len(links)))		
	#lets format the output nicely

  
  output(links)
  
def output(links):
  returncodes = {}
  link_pos = 1
  num_links = len(links)
  t0 = time.clock()
  for link in links:
    print (link)
  for link in links:
    print ("checking %d of %d" %(link_pos,num_links))
    try:
      code = urlopen(link).getcode()
    except HTTPError as e :
      print('error %d from %s' %(e.code, link))
      code = e.code
    except:
      code= 0
    
    if code in returncodes:
      returncodes[code].append(link)
    else:
      returncodes[code] = [link]   
    
    link_pos+=1

  print('took %d secs' % (time.clock() - t0))
    #returns themd httpstatus codes that were seen
  print(returncodes.keys())
  httpstatus = None
    #loop to allow the user to print the urls by status code
  while httpstatus != 'quit':      
    httpstatus = raw_input('(1) Inspect Broken links\n(2) Enter a new Address\n(3) Run again\n(4) Quit and Write output to file\n: ')
    if httpstatus == '1':
      httpstatus = raw_input("Enter Status code to check: ") 
      try: 
        for lines in returncodes[int(httpstatus)]:
          print lines
        print ("Press Enter to continue.....")
        m.getch()
      except:
        print ("Status code not found")
        print(returncodes.keys())

    elif httpstatus == '2':
      main()
    elif httpstatus =='4':
      #print 'Writing To XML Log File currentLinks.xml'
      #writeFile(links, returncodes)
      sys.exit()
    elif httpstatus =='3':
      output(links)
    else:
      print('Invalid Input')
	#main done

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
  
def getFile():
  print ("[Checking for file]\n")
  try:
    with open('currentLinks.xml'): pass
  except IOError:
    print ("[file not found, using command line for input]\n")
    return False

  choice = raw_input("\nLinks file found\nwould you like to check links in file?\n1:Yes\n2:No ")  
  if choice == '1':
    readFile()
    sys.exit()
  else:
    return False

def readFile():
  links = []
  with open('currentLinks.xml') as file_in:
    for line in file_in:
      links.append(line)

  urls = {}
  instances = 0
  for link in links:
    urls[link] = True
    instances += 1
    print('%d Found link %s' % (instances, link))
        
  print('Found %d links with %d unique URLs' % (instances, len(urls)))



def writeFile(links, returncodes):
  E = lxml.builder.ElementMaker()
  ROOT = E.root
  DOC = E.doc
  FIELD1 = E.field1
  if inputType == '1':
    name='IMG'
  elif inputType == '2':
    name='LINK'

  output_file = ROOT(FIELD1(input_site, name=name))
  for link in links:
    output_file.append(DOC(FIELD1(link, code=returncodes[int()])))

  print lxml.etree.tostring(output_file, pretty_print=True)
  try:
    f = open("currentLinks.xml", "rw")
    f.write(output_file)
    f.close()
  except:
    print("Unable to open file for writing")

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
#Boolean check for valid website
def check(url_string):
  if urlopen(url_string).getcode() == 200:
    return True
  else:
    return False
"""
