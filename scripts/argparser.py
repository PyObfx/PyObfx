#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import argparse
"""
Once, there was a world. A world filled with a magic. A world with lots of
different races. The world kingdoms wish to conquer. With this greed in their
eyes, kingdoms'd sacrificed tons of fine warriors, magicians even civillians.
One day, people heard news from the north. A new kingdom had found. A kingdom 
that devours everything on its path. They kill people, rape women and raze towns.
People call them savages. Savages that lost their humanity under their lord. Lord
Azkward. A man chaos gods chose for their invasion. An invincible man. With the
power of chaos gods, his invasion's starting from North...
"""


def cli_arg_parser():
    parser = argparse.ArgumentParser()
    # List args
    # This can be replaced after with -p option that automatically
    # obsf each .py file in the given -p ath.
    parser.add_argument("-f", "--file",
                        help="File to be obfscated.", required=True)
    # Dic format
    return vars(parser.parse_args())


def function_dispatcher():
    args = cli_arg_parser()
    # Testing purposes. Since [file] is a required param, obviously it wont
    # be empty.
    if args['file']:
        return args
    return None
# Testing if its working
# function_dispatcher()
