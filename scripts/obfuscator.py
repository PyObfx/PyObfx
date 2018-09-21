#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import random
from scripts.tokenizer import Tokenizer
from scripts.strgen import StringGenerator
from scripts.io import read_file

class Obfuscator:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_content = read_file(file_name)
        self.tokenizer = Tokenizer(self.file_content)
        self.tokens_all = self.tokenizer.get_tokens()
        self.ints = [random.randint(1, 5) for _ in range(3)]
        self.deobfuscators = {
            1: "lambda n: (n - ({} % {})) - {}".format(*self.ints[::-1]),
            2: "lambda n: int((n ^ {}) / {})".format(*self.ints[:2]),
            3: "lambda n: n - sum({})".format(str(self.ints))
        }
        self.obf_types = {0:"string", 1:"int", 2:"float", 3:"bool"}
        self.strgen_for_variable = StringGenerator(1)
        self.obfx_ext = "_obfx.py"
        self.obfx_header = "# Obfuscated with PyObfx #"

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
            # String Name Obfuscation
                string = self.tokenizer.find_by_id(int(token[1]))[2]
                obf_string_name = self.strgen_for_variable.generate(len(string))
                token_index = self.tokenizer.find_index_by_id(token[1])
                current_token = self.tokens_all[token_index]
                self.tokenizer.TOKENS[token_index] = (current_token[0], current_token[1]. \
                    replace(string, obf_string_name), obf_string_name)
            # String Value Obfuscation
                # obf_string_ = self._escape(''.join(chr(obfuscator(ord(c))) for c in string)) # Example code

        self.save_obfuscated_file()

    def save_obfuscated_file(self):
        new_file_name = self.file_name.replace("."+self.file_name.split('.')[len(self.file_name.split('.'))-1], self.obfx_ext)
        new_file_content = self.obfx_header + '\n';
        tokens = self.tokenizer.TOKENS
        for token in tokens:
            new_file_content += token[2]
        print(new_file_content)

    
    