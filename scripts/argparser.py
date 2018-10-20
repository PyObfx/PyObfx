#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import argparse

def cli_arg_parser():
    """
    Parses the arguments from CLI and returns to the dictionary
    where keys are the options/flags

    ex: when -f triggered, there'll be 'file' key in the dictionary.
    and values are accessible with list syntax `[]`
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",
                        help="File to be obfscated.", required=True)
    parser.add_argument("-p",
                        "--pack",
                        help="Available packers: bz2, gz, lzma")
    parser.add_argument("-s",
                        "--silent",
                        action="store_true",
                        help="Just quietness")
    parser.add_argument("-o", "--out",
                        help="Destination for the output file")
    parser.add_argument("--no-log",
                        action="store_true",
                        help="Not save log file(s)")
    parser.add_argument("--str-gen",
                        help="Available string generators: jp, ch, in")
    # Return to dictionary
    return vars(parser.parse_args())

