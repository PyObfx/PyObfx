#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os, io

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
    # Avoid charmap and encoding issues
    with io.open(filename, "w", encoding="utf-8") as file:
        file.write(content)
