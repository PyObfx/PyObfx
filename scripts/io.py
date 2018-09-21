#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os

#BASEDIR  = os.path.dirname(os.path.realpath(__file__))


class FileTypeException(Exception):
    pass


def read_file(filename):
    if os.path.splitext(filename)[1] != '.py':
        raise FileTypeException("Only Python(.py) file.")

    with open(filename) as file:
        data = file.read()
    return data

def write_file(filename, content):
    if os.path.splitext(filename)[1] != '.py':
        raise FileTypeException('Only Python(.py) file.')

    with open(filename, 'w') as file:
        file.write(content)
