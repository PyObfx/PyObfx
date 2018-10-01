
#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from scripts.argparser import cli_arg_parser
from scripts.obfuscator import Obfuscator
from scripts.banner import print_banner

# Show cool ascii art and project description
desc = "PyObfx v1.0"



def main():
	print_banner()
	args = cli_arg_parser()
	obfuscator = Obfuscator(args['file'])
	obfuscator.obfuscate()

if __name__ == "__main__":
	main()

