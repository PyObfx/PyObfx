# -*- coding utf:8 -*-

import random
import string

class StringGenerator:
	def __init__(self, type):
		self.type = type  # 1- Variable | 2- String | 3- All | 4- Japanese | 5- Chinese | 6-Hindi
		self.all = list( string.ascii_uppercase ) + list( string.ascii_lowercase ) + list( string.digits ) + list(
			string.punctuation ) + \
		           list( string.whitespace ) + list( "~`!@#$%^&*()_+-=[]{}|;:<>?,." )
		self.hindi = ["ौ","ै","ा","ी","ू","ब","ह","ग","द","ज","ड","ो","े","्","ि","ु","प","र","क","त","च","ट","म","न","व","ल","स","य"]
		self.japanese = ["う","ぇ","て","ゅ","い","お","っ","あ","ん"]
		self.chinese = ["摆","汜","蓠","戈","人","心","最","杰","圻","丈","中","重","钕","月","弓","一","儿","勒","屁","艾","西","伊", "import"]
		self.rndType = {1: list( string.ascii_uppercase ) + list( string.ascii_lowercase ),
		                2: list( string.ascii_uppercase ) + list( string.ascii_lowercase ) +
		                   list( string.digits ) + list( string.punctuation ) + list( string.whitespace ),
		                3: self.all,
		                4: self.japanese,
		                5: self.chinese,
		                6: self.hindi}
		self.pyKeywords = __import__('keyword').kwlist

	def __before__(self):
		self.before = []

	def generateRandStr(self, length, max_length):
		result = ""
		for _ in range(random.randint(length, max_length)):
			result += random.choice(self.rndType[self.type])
		if result in self.pyKeywords:
			return self.generateRandStr(length, max_length)
		else:	
			return result
			
	def generate(self, length):
		result = ""
		for _ in range(length):
			result += random.choice(self.rndType[self.type])
		if result in self.pyKeywords:
			return self.generate(length)
		else:	
			return result
