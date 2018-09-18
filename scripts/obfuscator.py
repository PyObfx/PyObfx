#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import random

class Obfuscator:
    def __init__(self, file_content, tokens):
        self.file_content = file_content
        self.tokens = tokens
        self.ints = [random.randint(1, 5) for _ in range(3)]
        self.deobfuscators = {
            1: "lambda n: (n - ({} % {})) - {}".format(*self.ints[::-1]),
            2: "lambda n: int((n ^ {}) / {})".format(*self.ints[:2]),
            3: "lambda n: n - sum({})".format(str(self.ints))
        }

    string_deobfuscator = "lambda s: ''.join(chr({}(ord(c))) for c in s)" # str.format with int deobfuscator name
    string_deobfuscator2 = lambda self, obfuscation: "lambda s: ''.join(chr(({})(ord(c))) for c in s)".format(self.deobfuscators[obfuscation])

    def _escape(self, s):
        return s.replace('"', r'\"').replace("'", r"\'")

    def obfuscate(self, obfuscation=1):
        obfuscators = {1: self.obfuscation1, 2: self.obfuscation2, 3: self.obfuscation3}
        obfuscator = obfuscators[obfuscation]
        for s in filter(lambda s: s != '"' and s != "'", self.tokens['strings']):
            obfuscated_string = self._escape(''.join(chr(obfuscator(ord(c))) for c in s))
            print(s, obfuscated_string) # printing encrypted string for now

        for i in self.tokens['integers']:
            print(i, obfuscator(int(i)))

    obfuscation1 = lambda self, n: (n + self.ints[0]) + (self.ints[2] % self.ints[1])
    obfuscation2 = lambda self, n: (n * self.ints[1]) ^ self.ints[0]
    obfuscation3 = lambda self, n: n + sum(self.ints)