import time
import re
#reg expression = re
import sys
from urllib2 import urlopen, HTTPError
from optparse import OptionParser
from pprint import pprint as p
#Authors Terrnan O. and Sammy S.


            
            

class lfind():
    
    
    def __init__(self):
        self.urls_to_check = []
        self.urls_checked_already = []
        self.codes_already_known = {} 
        
    
    
    
    
    def get_links(self, url):
        #urls_checked_already used here
        self.begurl='http://'
        self.page='/'
        self.patternurl = re.compile(r'.*.com/')
        #checks new url to see if it will work with urlopen
        #print url[0:4]
        if url[0:4] == 'http':
                print 'has http'
                #print url
        if url[0:4] != 'http':
            url = self.begurl+url
            print 'no http'
            print url
        if not re.search(self.patternurl, url):
            url = url + self.page
            print 'has no /'
            print url
        else: 
            pass  
        #scrapes the page source
        print('Opening %s...' % url)
        self.content = urlopen(url).read()

        self.pattern = re.compile(r'<a .*?href=["|\'](?!#)(.+?)["\']');

        # we can avoid duplicates by using a hash - will save time later
        self.instances = 0
        for link in self.pattern.findall(self.content):
            
            if link[0:2] == '//':
                #print('URL does not specify url, prepending http:')
                link = 'http:'+ link
            elif link[0] == '/':
                #print('URL does not specify url, prepending '+self.host)
                link = self.host+link
            if self.host in link and link not in self.urls_checked_already and link not in self.urls_to_check:
                self.urls_to_check.append(link)
            
            self.instances += 1
            
            #print('%d Found link %s' % (self.instances, link)) 
        print('Found %d links with %d unique urls_to_check' % (self.instances, len(self.urls_to_check)))
        p(self.urls_to_check)
        #dont need this really updates above
        return self.urls_to_check
            
            
    def get_codes(self):
        # uses urls_to_check urls_checked_already codes_already_known
        self.x = 1
        self.y = len(self.urls_to_check)
        self.t0 = time.clock()
        print 'getcodes'  
        for link in self.urls_to_check:
            if link not in self.urls_checked_already:
                self.urls_checked_already.append(link)  
        # when there is a 403 like code it assigns it to 0       
            try:    
                self.code = urlopen(link).getcode()
            except HTTPError as e :
                #print e.__class__.__name__
                #print e.code
                print('error %d from %s' %(e.code, link))
                # %S is string and %d decimal look up others
                self.code = e.code
            except:
                self.code= 0
                  
            if self.code in self.codes_already_known:
                self.codes_already_known[self.code].append(link)
            else: 
                self.codes_already_known[self.code] = [link]   
            print('Checking URL %d of %d' %(self.x,self.y))
            self.x+=1
        print('took %d secs' % (time.clock() - self.t0))
        #returns the httpstatus codes that were seen
        print 'got urls_checked_already in getcodes length is'
        #p(self.urls_checked_already)
        print len(self.urls_checked_already)
        return self.codes_already_known
        
    
    
       
        
    def check(self, test_str):
        self.pattern = r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))'
        if not re.search(self.pattern, test_str):
            self.valid = False
            print 'Invalid url format : %r' % (test_str,)
        else:
            print 'Valid url format   : %r' % (test_str,)
            self.valid = True
        return self.valid        
                
            
    def urlformat(self, url):
        print url
        print 'checking url'
        self.begurl='http://'
        self.page='/'
        self.patternurl = re.compile(r'.*.com/')
        if url[0:3] == 'http':
            url = url
            print 'has http'
            print url
        elif url[0:3] != 'http':
            url = self.begurl+url
            print 'no http'
            print url
        #if not re.search(self.patternurl, url):
         #   url = url + self.page
         #   print 'has no /'
         #   print url
        return url    
        
        
        
        
    def test_url(self, url, host, max_depth, current_depth):
        # uses urls_to_check urls_checked_already codes_already_known
        self.host = self.urlformat(host)
        self.get_links(url)
        print '*******************************current depth ouside if*********************'
        print current_depth
        
        if current_depth < max_depth:
            if url is host:
                self.get_codes()
                #p(self.codes_already_known[200])
            for url in self.codes_already_known[200]:
                print '*******************************current depth for*********************'
                print current_depth
                if url not in self.urls_checked_already:
                    self.test_url(url, host, max_depth, current_depth+1)
        #self.get_codes()    
        #return self.codes_already_known 
        return self.urls_checked_already
        
#------------------------------------------SETUP----------------------------            
checker=lfind()
#set url
#urls_checked_already = {}
#codes_already_known = {}
site = 'ringpop.stage.aistg.com'
#check = checker.check(site)
#if check == False:
 #   sys.exit()
#else: pass    
p(checker.test_url(site, site, 2, 0))



#urls_to_check = checker.get_links(site, urls_checked_already) #gives me return something
#codes = checker.get_codes(urls_to_check, urls_checked_already, codes_already_known)
#print codes

        
            
            