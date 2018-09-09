#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from scripts.io import read_file
from scripts.tokenizer import Tokenizer
from scripts.argparser import function_dispatcher
from scripts.obfuscator import Obfuscator

# Show cool ascii art and project description
desc = "PyObfx v1.0"


def print_header():
	print(desc)


def main():
	print_header()
	args = function_dispatcher()
	pyfile = read_file(args['file'])
	tokenizer = Tokenizer(pyfile)
	tokens = tokenizer.tokenize()
	obfuscator = Obfuscator(pyfile, tokens)
	obfuscator.obfuscate()

if __name__ == "__main__":
	main()
