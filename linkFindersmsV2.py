import time
import re
#reg expression = re

from urllib2 import urlopen, HTTPError
from optparse import OptionParser
#Authors Terrnan O. and Sammy S.






def main():
    valid = False   
    while not valid:
        site = raw_input('Enter URL example: www.google.com/ : ')
        if site == 'quit': return
        print "you entered" '' 'http://' + site
        if 'http' not in site:
            host = 'http://' + site
            print 'Appending to site' '' 'http://' + site
        else:
            host = site    
            
        valid = check(host)
       
    page = '/'
    links = getlinks(host,page)
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
                print(returncodes[int(httpstatus)] ) 
            except:
                print('Invalid Input')
            
def getlinks(host,page):
    url = host+page
    print('Opening %s...' % url)
    #scrapes the page source
    content = urlopen(url).read()

    print('Compiling RegExp...')
    pattern = re.compile(r'<a .*?href=["|\'](?!#)(.+?)["\']');

    # we can avoid duplicates by using a hash - will save time later
    urls = {}
    instances = 0
    for link in pattern.findall(content):

        if link[0:2] == '//':
            print('URL does not specify host, prepending http:')
            link = 'http:'+link
        elif link[0] == '/':
            print('URL does not specify host, prepending '+host)
            link = host+link

        urls[link] = True
        instances += 1
        print('%d Found link %s' % (instances, link))
        
        
    print('Found %d links with %d unique URLs' % (instances, len(urls)))
#list of urls
    return urls.keys()
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

main()
