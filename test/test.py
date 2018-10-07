#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
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
    def awesome():
    	print("awesome")
    	print("\t+\'is this really working?\'\n" + "\t-\"oh, it is\"")
    awesome()

if __name__ == "__main__":
    main()