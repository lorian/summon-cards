# scrape statblock info from web and format into cards for summoned monsters

import urllib
import urllib2
import pprint
from bs4 import BeautifulSoup
import unicodedata

all_headers = ['Init',
 'Senses',
 'DEFENSE',
 'AC',
 'hp',
 'Fort',
 'Ref',
 'Will',
 'DR',
 'Immune',
 'Resist',
 'SR',
 'OFFENSE',
 'Speed',
 'Melee',
 'Ranged',
 'Special Attacks',
 'Spell-Like Abilities',
 'STATISTICS',
 'Str',
 'Dex',
 'Con',
 'Int',
 'Wis',
 'Cha',
 'Base Atk',
 'CMB',
 'CMD',
 'Feats',
 'Skills',
 'Languages',
 'SQ',
 'SPECIAL ABILITIES',]
ignore_headers = ['DEFENSE', 'OFFENSE', 'STATISTICS']

monster_urls = ['http://www.d20pfsrd.com/bestiary/monster-listings/animals/dinosaur/ankylosaurus',
				'http://www.d20pfsrd.com/bestiary/monster-listings/outsiders/azata/bralani']
monster_info = dict()
for url in monster_urls:
	monster_page = urllib2.urlopen(url)
	monster_soup = BeautifulSoup(monster_page, "lxml")

	print '\n\n'
	# monster stats are in last table of given class
	info_table = [unicodedata.normalize('NFKD', text).encode('ascii','ignore')
					for text in monster_soup.find_all('table', class_="sites-layout-hbox")[-1].stripped_strings]
	pprint.pprint( info_table)

	monster_info['name'] = info_table[0]
	monster_info['size'] = info_table[3]
	# take advantage of awkward but consistant list ordering
	list_of_lookups = ['Init', 'Perception', 'Speed',
						'hp', 'Fort', 'Ref', 'Will', 'DR', 'SR', 'Immune', 'Resist',
						'Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha', 'Base Atk', 'CMB', 'CMD',
						'Languages', 'Reach']
	for l in list_of_lookups:
		try:
			monster_info[l] = info_table[info_table.index(l) +1]
		except:
			print "missing {}".format(l)
	# more complex lookups that could take up multiple table entries: (lookup, next entry)
	list_of_lookups = [('AC','hp'), ('Senses','Perception'), ('Feats','Skills'),
						('Melee','Ranged'), ('Melee','Space'), ('Melee','Special Attacks'),
						('Ranged','Space'), ('Ranged','Special Attacks')]
	for (s,e) in list_of_lookups:
		try:
			start_index = info_table.index(s) +1
			end_index = info_table.index(e) -1
			print info_table[start_index:end_index]
		except:
			print "missing {}/{}".format(s,e)

	# handle skills special since they have no clear end point: look for string, +num pairs
	print '\n\n'
	pprint.pprint(monster_info)
