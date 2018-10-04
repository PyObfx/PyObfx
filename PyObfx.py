#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from scripts.argparser import cli_arg_parser
from scripts.obfuscator import Obfuscator
from scripts.banner import print_banner

def main():
    print_banner()
    args = cli_arg_parser()
    obfuscator = Obfuscator(args)
    obfuscator.obfuscate()

if __name__ == "__main__":
    main()
