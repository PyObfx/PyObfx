#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from scripts.argparser import cli_arg_parser
from scripts.obfuscator import Obfuscator
from scripts.banner import print_banner
from scripts.packer import *

# test function. If this works, I'll move it into another file.
def pack_dispatcher(obfuscated_file, packer_name='bz2'):
        packer_name += "_pack"
        packer_name(obfuscated_file)



def main():
	print_banner()
	args = cli_arg_parser()
	obfuscator = Obfuscator(args['file'])
	obfuscator.obfuscate()

if __name__ == "__main__":
	main()

