#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import os as oss
import random as rnd
import time as wow_time

test_str = "<- Test ->"
real_test_str   =   "x"
test_float = 9.9
test_int = 0
test_bool = True
hi = "Hi! \n"

def main():
    print(test_float)
    print(test_int)
    print(test_bool)
    print(hi + " " + test_str)
    print(rnd.randint(5, 15))
    wow_time.sleep(1)
    def awesome():
    	print("awesome")
    	print("\t+\'is this really working?\'\n" + "\t-\"oh, it is\"")
    awesome()

if __name__ == "__main__":
    main()