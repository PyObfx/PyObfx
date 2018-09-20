#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from scripts.io import read_file
from scripts.argparser import cli_arg_parser
from scripts.obfuscator import Obfuscator
from scripts.strgen import StringGenerator

# Show cool ascii art and project description
desc = "PyObfx v1.0"


def print_header():
	print(desc)


def main():
	print_header()
	args = cli_arg_parser()
	pyfile = read_file(args['file'])
	obfuscator = Obfuscator(pyfile)
	obfuscator.obfuscate()

if __name__ == "__main__":
	main()
