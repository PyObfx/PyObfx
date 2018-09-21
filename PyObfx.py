#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from scripts.argparser import cli_arg_parser
from scripts.obfuscator import Obfuscator

# Show cool ascii art and project description
desc = "PyObfx v1.0"


def print_header():
	print(desc)


def main():
	print_header()
	args = cli_arg_parser()
	obfuscator = Obfuscator(args['file'])
	obfuscator.obfuscate()

if __name__ == "__main__":
	main()