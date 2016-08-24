# scrape statblock info from web and format into cards for summoned monsters

import urllib
import urllib2
import pprint
from bs4 import BeautifulSoup
import unicodedata
import string
import math
import datetime

monster_urls = ['http://www.d20pfsrd.com/bestiary/monster-listings/animals/dinosaur/ankylosaurus',
				'http://www.d20pfsrd.com/bestiary/monster-listings/outsiders/azata/bralani',
				'http://www.d20pfsrd.com/bestiary/monster-listings/outsiders/agathion/agathion-vulpinal',
				'http://www.d20pfsrd.com/bestiary/monster-listings/outsiders/genie/djinni',
				'http://www.d20pfsrd.com/bestiary/monster-listings/magical-beasts/unicorn',
				'https://sites.google.com/site/pathfinderogc/bestiary/monster-listings/animals/cetacean/dolphin/orca',
				]
monster_urls = ['http://www.d20pfsrd.com/bestiary/monster-listings/magical-beasts/unicorn']

all_headers = ['Init',
 'Senses',
 'Aura',
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
 'Space',
 'Reach',
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
 'Base',
 'Base Atk',
 'CMB',
 'CMD',
 'Feats',
 'Skills',
 'Languages',
 'SQ',
 'SPECIAL ABILITIES',
 'END',
 'Image Source',
 'Starting Statistics',
 'Image courtesy',]
ignore_headers = ['DEFENSE', 'OFFENSE', 'STATISTICS','END','Image Source','Starting Statistics','Image courtesy','Base']

data1 = ['Bralani',
 'CR 6',
 'XP 2,400',
 'CG Medium',
 'outsider',
 '(',
 'azata',
 ',',
 'chaotic',
 ',',
 'extraplanar',
 ',',
 'good',
 ',',
 'shapechanger',
 ')',
 'Init',
 '+8;',
 'Senses',
 'darkvision 60 ft., low-light vision;',
 'Perception',
 '+15',
 'DEFENSE',
 'AC',
 '20, touch 14, flat-footed 16 (+4 Dex, +6 natural)',
 'hp',
 '66 (7d10+28)',
 'Fort',
 '+9,',
 'Ref',
 '+9,',
 'Will',
 '+6',
 'DR',
 '10/cold iron or evil;',
 'Immune',
 'electricity, petrification;',
 'Resist',
 'cold 10, fire 10;',
 'SR',
 '17',
 'OFFENSE',
 'Speed',
 '40 ft., fly 100 ft. (perfect)',
 'Melee',
 '+1 scimitar',
 '+13/+8 (1d6+8/1820) or slam +12 (1d6+7)',
 'Ranged',
 '+1 composite longbow',
 '+12/+7 (1d8+6/3)',
 'Special Attacks',
 'whirlwind blast',
 'Spell-Like Abilities',
 '(CL 6th)',
 'At Will',
 'blur',
 ',',
 'charm person',
 '(DC 13),',
 'gust of wind',
 '(DC 14),',
 'mirror image',
 ',',
 'wind wall',
 '2/day',
 'lightning bolt',
 '(DC 15),',
 'cure serious wounds',
 'STATISTICS',
 'Str',
 '20,',
 'Dex',
 '18,',
 'Con',
 '19,',
 'Int',
 '13,',
 'Wis',
 '14,',
 'Cha',
 '15',
 'Base Atk',
 '+7;',
 'CMB',
 '+12;',
 'CMD',
 '26',
 'Feats',
 'Blind-Fight',
 ',',
 'Improved Initiative',
 ',',
 'Iron Will',
 ',',
 'Skill Focus',
 '(',
 'Perception',
 ')',
 'Skills',
 'Bluff',
 '+12,',
 'Fly',
 '+22,',
 'Handle Animal',
 '+12,',
 'Perception',
 '+15,',
 'Ride',
 '+14,',
 'Sense Motive',
 '+12,',
 'Stealth',
 '+14',
 'Languages',
 'Celestial, Draconic, Infernal; truespeech',
 'SQ',
 'wind form',
 'SPECIAL ABILITIES',
 'Whirlwind Blast (Su)',
 'When in wind form, a bralani can attack with a scouring blast of wind,\ndealing 3d6 points of damage in a 20-foot line (Reflex DC 17 half). The\nsave DC is Constitution-based.',
 'Wind Form (Su)',
 'A bralani can shift between its humanoid body and a body made of wind\nand mist as a standard action. In humanoid form, it cannot fly or use\nits whirlwind blast. In wind form, it functions as if under the effects\nof a',
 'wind walk',
 'spell. It can make slam attacks and use spell-like abilities in either\nform. A bralani remains in one form until it chooses to assume its\nother form. A change in form cannot be dispelled, nor does the bralani\nrevert to any particular form when killed (both shapes are its true\nform). A',
 'true seeing',
 'spell reveals both forms simultaneously.']
data2 = ['Ankylosaurus',
 'CR 6',
 'XP 2,400',
 'N Huge',
 'animal',
 'Init',
 '+0;',
 'Senses',
 'low-light vision',
 ',',
 'scent',
 ';',
 'Perception',
 '+14',
 'DEFENSE',
 'AC',
 '22,',
 'touch',
 '8,',
 'flat-footed',
 '22 (+14',
 'natural',
 ', 2 size)',
 'hp',
 '75 (10d8+30)',
 'Fort',
 '+12,',
 'Ref',
 '+7,',
 'Will',
 '+4',
 'OFFENSE',
 'Speed',
 '30 ft.',
 'Melee',
 'tail +14 (3d6+12 plus stun)',
 'Space',
 '15 ft.;',
 'Reach',
 '15 ft.',
 'STATISTICS',
 'Str',
 '27,',
 'Dex',
 '10,',
 'Con',
 '17,',
 'Int',
 '2,',
 'Wis',
 '13,',
 'Cha',
 '8',
 'Base Atk',
 '+7;',
 'CMB',
 '+17;',
 'CMD',
 '27 (31 vs. trip)',
 'Feats',
 'Great Fortitude',
 ',',
 'Improved Bull Rush',
 ',',
 'Improved Overrun',
 ',',
 'Power Attack',
 ',',
 'Weapon Focus',
 '(tail)',
 'Skills',
 'Perception',
 '+14',
 'SPECIAL ABILITIES',
 'Stun (Ex)',
 "The ankylosaurus's tail can deliver a powerful, stunning blow. A\ncreature struck by this attack must make a DC 23 Fortitude save or be",
 'dazed',
 'for 1\nround. If the strike is a critical hit and the target fails its save,\nit is instead',
 'stunned',
 'for 1d4 rounds. The save DC is Strength-based.',
 'Image Source',
 'Wikipedia',
 '.',
 'Ankylosaurus Companions',
 'Starting Statistics',
 ':',
 'Size',
 'Medium;',
 'Speed',
 '30 ft.;',
 'AC',
 '+9 natural armor;',
 'Attack',
 'tail (1d6);',
 'Ability Scores',
 'Str 10, Dex 14, Con 9, Int 2, Wis 12, Cha 8;',
 'Special Qualities',
 'low-light vision, scent.',
 '7th-Level Advancement',
 ':',
 'Size',
 'Large;',
 'AC',
 '+2 natural armor;',
 'Attack',
 'tail (2d6);',
 'Ability Scores',
 'Str +8, Dex 2, Con +4;',
 'Special Qualities',
 'stun.']

class monster():
	def __init__(self,page_dict):
		''' Takes dict made from scraped table as input '''
		for key, value in page_dict.items():
			setattr(self, key, value)
		print self.name
		
		# General splitting and formatting
		self.format_ac()
		self.get_perception()
		self.strip_spaces()
		
		# Adjust things for Augmented Summons
		self.get_hd()
		self.adj_fort()
		self.strip_spaces()
		
		# Adjust things with Celestial template
		if hasattr(self,"Celestial"):
			self.add_darkvision()
			self.inc_cr()
		
		self.strip_spaces()
		print self.__dict__.keys()

	def format_ac(self):
		# 15, touch 12, flat-footed 12; (+3 Dex, +3 natural, 1 size; +2 deflection vs. evil)
		AC_details = self.AC.partition('(')[2].partition('; ')[2].strip(')')
		self.AC = "{} ({})".format(self.AC.partition(';')[0],AC_details)
		
	def get_perception(self):
		# low-light vision, scent; Perception +10
		self.Perception = self.Senses.partition('+')[2] # 10
		self.Senses = self.Senses.partition(';')[0] # low-light vision, scent
		
	def get_hd(self):
		#  34 (4d10+12) -> 42 (4d10)
		self.hit_die = int(self.hp.partition('(')[2].partition('d')[0].strip())
		total_hp = int(self.hp.partition(' ')[0].strip())+self.hit_die*2 # adjust for increased Con
		self.hp = "{} ({})".format(total_hp,self.hp.partition('(')[2].partition('+')[0])

	def adj_fort(self):
		self.Fort = int(self.Fort.strip())+2 # adjust for increased Con
		
	def add_darkvision(self):
		# low-light vision, scent -> low-light vision, scent, darkvision
		if 'darkvision' not in self.Senses:
			self.Senses = '{}, darkvision'.format(self.Senses)

	def inc_cr(self):
		if self.hit_die > 4:
			self.cr += 1 # CR increases by 1 if monster has 5+ HD

	def add_sr(self):
		pass
	'''
		if 'SR' not in m.keys() or int(m.SR) < m.cr+5:
				m.SR = m.cr +5

		if hit_die < 5:
			try:
				m.Resist = m.Resist + ', cold 5, acid 5, electricity 5'
			except:
				m.Resist = 'cold 5, acid 5, electricity 5'
		elif hit_die < 11:
			try:
				m.Resist = m.Resist + ', cold 10, acid 10, electricity 10'
			except:
				m.Resist = 'cold 10, acid 10, electricity 10'
			try:
				m.DR = m.DR + ', 5/evil'
			except:
				m.DR = '5/evil'
		else:
			try:
				m.Resist = m.Resist + ', cold 15, acid 15, electricity 15'
			except:
				m.Resist = 'cold 15, acid 15, electricity 15'
			try:
				m.DR = m.DR + ', 10/evil'
			except:
				m.DR = '10/evil'
	'''

	def strip_spaces(self):
		# to avoid having to do this manually every time we create an attribute
		for k,v in self.__dict__.items():
			try: # avoid non-string types
				self.k = v.strip()
			except:
				pass

def scrape_url(url):
	monster_info = dict()

	monster_page = urllib2.urlopen(url)
	monster_soup = BeautifulSoup(monster_page, "lxml")
	# monster stats are in last table of given class
	info_table = [unicodedata.normalize('NFKD', text).encode('ascii','ignore')
					for text in monster_soup.find_all('table', class_="sites-layout-hbox")[-1].stripped_strings]
	#info_table = data1
	print '\n\n'
	pprint.pprint( info_table)

	offset = 0
	if not info_table[1].startswith('CR '): # something else in top rows
		for i,r in enumerate(info_table):
			if r.startswith('CR'):
				offset = i-1
				break
	monster_info['name'] = info_table[0+offset]
	monster_info['cr'] = int(info_table[1+offset].partition(' ')[2]) # for celestial SR
	monster_info['size'] = info_table[3+offset]
	monster_info['type'] = info_table[4+offset]


	if 'animal' in monster_info['type']:
		monster_info['Celestial'] =  True
		monster_info['name'] = 'Celestial ' + monster_info['name']

	for header in set(all_headers) - set(ignore_headers):
		content = []
		offset = 1
		try:
			next_line = info_table[info_table.index(header) +offset]
			while next_line not in all_headers:
				content.append(next_line)
				offset +=1
				try:
					next_line = info_table[info_table.index(header) +offset]
				except:
					next_line = 'END'
			monster_info[header] = ''.join([(c if c in string.punctuation else " "+c) for c in content]).strip().rstrip(',').rstrip(';')
		except ValueError:
			if header == 'Base Atk':
				monster_info[header] = info_table[info_table.index('Base') +2].strip() # sometimes Base Atk is broken into two words
			else:
				print "missing {}".format(header)

	if 'Reach' in monster_info.keys() and monster_info['Reach'] == '5 ft.':
		del monster_info['Reach']

	return monster_info

def process_attacks(attacks):
	# Adjust attack and damage for Augmented Summons
	each_attack = attacks.split(', ')
	# warning: need to handle Weapon Finesse later
	# warning: need to adjust for if only one attack
	#		<b>Melee</b> gore +8 (1d8+4)
	#	2 hooves +5 (1d3+2)
	adj_attacks = []
	for atk in each_attack:
		breakdown = atk.split('+')
		name = breakdown[0] #2 hooves
		atk = int(breakdown[1].partition(' ')[0])+2 #5
		dmg_die = breakdown[1].partition(' ')[2] #(1d3
		dmg = int(breakdown[2].partition(')')[0])+2 #2
		adj_attacks.append("{}+{} {}+{})".format(name,atk,dmg_die,dmg))
	return "\n\t\t".join(adj_attacks)

def print_card(m, spell_level):
	print m.name
	precombat = ['card:\n',
				'	has styling: false\n',
				'	notes:\n',
				'	time created: {}\n'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), #2016-01-10 22:46:26
				'	time modified: {}\n'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
				'	name: {}\n'.format(m.name),
				'	level: {0}\n'.format(spell_level),
				'	precombat:\n',
				'		<b>Init</b> {}; {} {}\n'.format(m.Init, m.size, m.type),
				'		<b>Senses</b> {} <b>Per</b> +{}\n'.format(m.Senses, m.Perception),
				'		<b>Speed</b> {}\n'.format(m.Speed),
				]

	# DEFENSE
	defense = ['	defense:\n',
				'		<b>AC</b> {}\n'.format(m.AC),
				'		<b>HP</b>{}'.format(m.hp),
				'		Fort +{}, Ref {}, Will {}\n'.format(m.Fort,m.Ref,m.Will),
				]
	'''


	try:
		defense[2] += ' <b>DR</b> {}'.format(m.DR)
	except:
		pass
	try:
		defense[2] += ' <b>SR</b> {}'.format(m.SR)
	except:
		pass
	defense[2] += '\n'

	try:
		defense.append('		<b>Immune</b> {}\n'.format(m.Immune))
	except:
		pass
	try:
		defense.append('		<b>Resist</b> {}\n'.format(m.Resist))
	except:
		pass

	# OFFENSE
	# adjust CMB and CMD for my feat
	if '(' in m.CMB: #+10 (+14 grapple) warning: 31 (35 vs. trip, 37 vs. overrun)
		base_cmb = int(m.CMB.strip('+').partition(' (')[0])+2
		extra_cmb = int(m.CMB.partition('(')[2].partition(' ')[0].strip('+'))+2
		cmb = "{} (+{} {}".format(base_cmb,extra_cmb,m.CMB.partition('(')[2].partition(' ')[2])
	else:
		cmb = int(m.CMB.strip('+'))+2
	if '(' in m.CMD: #27 (31 vs. trip)
		base_cmd = int(m.CMD.partition(' (')[0])+2
		extra_cmd = int(m.CMD.partition('(')[2].partition(' ')[0])+2
		cmd = "{} ({} {}".format(base_cmd,extra_cmd,m.CMD.partition('(')[2].partition(' ')[2])
	else:
		cmd = int(m.CMD.strip('+'))+2

	offense = ['	offense:\n',]

	if 'Reach' in m.keys():
		offense.append('		<b>reach</b> {}\n'.format(m.Reach))
	if 'Melee' in m.keys():
		offense.append('		<b>Melee</b> {}\n'.format(process_attacks(m.Melee)))
	if 'Ranged' in m.keys():
		offense.append('		<b>Ranged</b> {}\n'.format(m.Ranged))
	if 'Special Attacks' in m.keys():
		offense.append('		<b>Special Attack</b> {}\n'.format(m.Special Attacks))
	if 'Spell-Like Abilities' in m.keys():
		offense.append('		<b>SLAs</b> {}\n'.format(m.Spell-Like Abilities))

	offense.extend(['\n',
					'		<b>CMB</b> +{}\n'.format(cmb),
					'		<b>CMD</b> {}\n'.format(cmd),
					])

	# DETAILS
	details = ['	describe:\n',]
	if 'Skills' in m.keys():
		details.append('\n		<b>Skills</b> {}\n'.format(m.Skills)) # want to drop boring skills
	if 'Languages' in m.keys():
		details.append('\n		<b>Languages</b> {}\n'.format(m.Languages))
	if 'Feats' in m.keys():
		details.append('\n		<b>Feats</b> {}\n'.format(m.Feats)) # want to drop boring feats
	if 'Celestial' in m.keys():
		details.append('\n		<b>Smite evil</b> 1/day as a swift action; adds +{} to atk and +{} to dmg against a target evil foe until dead\n'
					.format(max(math.floor((float(m.Cha)-10)/2),0),m.hp.partition('(')[2].partition('d')[0]))

	details.append('	stats: Str {}, Dex {}, Con {}, Int {}, Wis {}, Cha {}; Base Atk {}\n'
					.format(int(m.Str)+4,m.Dex,int(m.Con)+4,m.Int,m.Wis,m.Cha,m.Base Atk.rstrip(';')))
	'''
	'''
				'\t\t<b>Grab</b> If you hit with bite, you can attempt to start a grapple as a free action without provoking an attack of opportunity. Each successful grapple check during successive rounds automatically deals bite damage.\n',
				'\n',
				'\t\t<b>Pounce</b> When you make a charge (2x move, +2 atk, -2 AC), you can make a full attack (including rake attacks).\n',
				'\n',
				'\t\t<b>Rake</b> When you begin the turn grappling, you gain two free claw attacks against a grappled foe.\n',
	'''

	content = precombat + defense #+ offense + defense + details
	print '\n\n'
	pprint.pprint(content)
	return content

spell_level = "SM V"
for url in monster_urls:
	monster_dict = scrape_url(url)
	m = monster(monster_dict)
	content = print_card(m, spell_level)
	with open('card.txt','w') as c:
		c.writelines(content)

