# scrape statblock info from web and format into cards for summoned monsters

import urllib
import urllib2
import pprint
from bs4 import BeautifulSoup

html = "<a> Keep me </a>"

monster_urls = ['http://www.d20pfsrd.com/bestiary/monster-listings/animals/dinosaur/ankylosaurus', 'http://www.d20pfsrd.com/bestiary/monster-listings/outsiders/azata/bralani']

for url in monster_urls:
	monster_page = urllib2.urlopen(url)
	monster_soup = BeautifulSoup(monster_page)
	print '\n\n'
	print [text for text in monster_soup.find_all('table', class_="sites-layout-hbox")[-1].stripped_strings]


'''
bodytext = False
monster_data = []
for line in monster_page:
	if line.startswith('<td align="left" width="85%">'):
		bodytext = True
	if 'sites-layout-tile' in line:
		bodytext = False

	if bodytext:
		print BeautifulSoup(line).findAll(text=True)
		#text = ''.join(text_parts)
'''
