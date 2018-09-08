#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import os

#BASEDIR  = os.path.dirname(os.path.realpath(__file__))


def read_file(filename):
    with open(filename) as file:
        data = file.read()
    return data

if __name__ == '__main__':
    pass
