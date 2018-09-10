#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

class Obfuscator:
	def __init__(self, file_content, tokens):
		self.file_content = file_content
		self.tokens = tokens

	def obfuscate(self, string_obfuscation=1):
		string_obfuscators = {1: self.obfuscate_string1, 2: self.obfuscate_string2}
		string_obfuscator = string_obfuscators[string_obfuscation]
		for s in filter(lambda s: s != '"' and s != "'", self.tokens['strings']):
			print(s, string_obfuscator(s)) #printing encrypted string for now

	def obfuscate_string1(self, s):
		out = [0]
		for c in s:
			out.extend([(ord(c) / 3) + (out[-1] % 2), 0])
		return out

	def deobfuscate_string1(self, s):
		out = ''
		for i in range(1, len(s), 2):
			out += chr(int((s[i] - (s[i-1] % 2)) * 3))
		return out

	def obfuscate_string2(self, s):
		rot13 = str.maketrans(
			'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
			'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm'
		)
		return s.translate(rot13)

	def deobfuscate_string2(self, s):
		rot13 = str.maketrans(
			'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm',
			'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz'
		)
		return s.translate(rot13)
