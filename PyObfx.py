#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from scripts.io import read_file
from scripts.tokenizer import tokenize
from scripts.argparser import function_dispatcher

# Show cool ascii art and project description
desc = "PyObfx v1.0"
def print_header(): 
	print(desc)

def main():
	print_header()
	args = function_dispatcher()
	pyfile = read_file(args['file'])
	print(pyfile) # Print file content for now

if __name__ == "__main__":
    main()
