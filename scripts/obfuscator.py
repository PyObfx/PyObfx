#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import random
from scripts.tokenizer import Tokenizer

class Obfuscator:
    def __init__(self, file_content):
        self.file_content = file_content
        self.tokenizer = Tokenizer(self.file_content)
        self.tokens_all = self.tokenizer.get_tokens()
        self.ints = [random.randint(1, 5) for _ in range(3)]
        self.deobfuscators = {
            1: "lambda n: (n - ({} % {})) - {}".format(*self.ints[::-1]),
            2: "lambda n: int((n ^ {}) / {})".format(*self.ints[:2]),
            3: "lambda n: n - sum({})".format(str(self.ints))
        }
        self.obf_types = {0:"string", 1:"int", 2:"float", 3:"bool"}

    string_deobfuscator = "lambda s: ''.join(chr({}(ord(c))) for c in s)" # str.format with int deobfuscator name
    string_deobfuscator2 = lambda self, obfuscation: "lambda s: ''.join(chr(({})(ord(c))) for c in s)".format(self.deobfuscators[obfuscation])
    obfuscation1 = lambda self, n: (n + self.ints[0]) + (self.ints[2] % self.ints[1])
    obfuscation2 = lambda self, n: (n * self.ints[1]) ^ self.ints[0]
    obfuscation3 = lambda self, n: n + sum(self.ints)

    def _escape(self, s):
        return s.replace('"', r'\"').replace("'", r"\'")

    def obfuscate(self, obfuscation=1):
        obfuscators = {1: self.obfuscation1, 2: self.obfuscation2, 3: self.obfuscation3}
        obfuscator = obfuscators[obfuscation]

        tokens = list()
        variables = self.tokenizer.get_variables()
        for index, _vars in enumerate(variables):
            for _var in variables[index]:
                _id = ([token[0] for token in self.tokens_all if token[2] == _var])[0]
                tokens.append((index, _id))

        for token in tokens:
            if self.obf_types[token[0]] == "string":
                string = self.tokenizer.find_by_id(int(token[1]))[2]
                obfuscated_string = self._escape(''.join(chr(obfuscator(ord(c))) for c in string))
                print(obfuscated_string)


    