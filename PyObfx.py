#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from scripts.argparser import cli_arg_parser
from scripts.obfuscator import Obfuscator
from scripts.banner import print_banner
from scripts.packer import *

# test function. If this works, I'll move it into another file.
def pack_dispatcher(obfuscated_file, packer_name='bz2'):
    function_dispatcher = {
            'bz2': bz2_pack(obfuscated_file)
    }
    try:
        packed = function_dispatcher[packer_name]
        print(packed)
    except KeyError:
        print("Something went wrong")


def main():
    print_banner()
    args = cli_arg_parser()
    obfuscator = Obfuscator(args['file'])
    ctx = obfuscator.obfuscate(True)
    pack_dispatcher(ctx)


if __name__ == "__main__":
    main()
