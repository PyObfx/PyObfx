#!/usr/bin/python3.6
# -*- coding: utf-8 -*-


from scripts.io import tokenize, read_file

def main():
	print("PyObfx v1.0")

if __name__ == "__main__":
    #main()
    print(tokenize(read_file('PyObfx.py')))