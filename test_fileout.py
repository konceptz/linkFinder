import time
import re
import sys
import lxml.etree
import lxml.builder
import msvcrt as m
from xml.dom.minidom import parse, parseString

from xml.dom.minidom import parse, parseString

from urllib2 import urlopen, HTTPError
from optparse import OptionParser
#from bs4 import BeautifulSoup as bs
from optparse import OptionParser
from urlparse import urlparse

def main():
	"""input_file = open("currentLinks.xml", 'r')
	dom = parseString(input_file)
	print dom
	"""
	lines = []
	dom = parse("currentLinks.xml")
	for node in dom.getElementsByTagName('Code'):
		lines.append(node.toxml())

	for line in lines:
		print line[17:-7]

main()