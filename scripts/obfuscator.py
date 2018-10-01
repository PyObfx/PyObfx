#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import random
from scripts.tokenizer import Tokenizer
from scripts.strgen import StringGenerator
from pygments.token import Token
from scripts.io import read_file, write_file


class Obfuscator:
    def __init__(self, file_name):
        self.obfx_header = "# Obfuscated with PyObfx #"
        self.file_name = file_name
        self.file_content = read_file(file_name)
        self.tokenizer = Tokenizer(self.file_content)
        self.ints = [random.randint(1, 5) for _ in range(3)]
        self.deobfuscators = {
            1: "lambda n: (n - ({} % {})) - {}".format(*self.ints[::-1]),
            2: "lambda n: int((n ^ {}) / {})".format(*self.ints[:2]),
            3: "lambda n: n - sum({})".format(str(self.ints))
        }
        self.obf_len_constant = 2
        self.obf_types = {0: "name", 1: "val", 2: "func"}
        self.obf_types_rev = {"name": 0, "val": 1, "func": 2}
        self.strgen_for_variable = StringGenerator(1)
        self.obfx_ext = "_obfx.py"
        self.deobfuscator_name = self.strgen_for_variable.generateRandStr(
            2, 10)
        self.str_deobfuscator_name = self.strgen_for_variable.generateRandStr(
            2, 10)

    # str.format with int deobfuscator name
    string_deobfuscator = "lambda s: ''.join(chr({}(ord(c))) for c in s)"

    def string_deobfuscator2(self, obfuscation):
        return "lambda s: ''.join(chr(({})(ord(c))) for c in s)".format(
            self.deobfuscators[obfuscation])

    def obfuscation1(self, n):
        return (n + self.ints[0]) + (self.ints[2] % self.ints[1])

    def obfuscation2(self, n): return (n * self.ints[1]) ^ self.ints[0]

    def obfuscation3(self, n): return n + sum(self.ints)

    def _escape(self, s):
        return s.replace('"', r'\"').replace("'", r"\'")

    def obfuscate(self, obfuscation=1):
        obfuscators = {1: self.obfuscation1,
                       2: self.obfuscation2,
                       3: self.obfuscation3}
        obfuscator = obfuscators[obfuscation]
        self.deobfuscator = self.deobfuscators[obfuscation]
        # Variable Name Obfuscation
        name_tokens = list()
        for token in self.tokenizer.get_tokens():
            if str(Token.Name)+"," in token[1]:
                name_tokens.append((self.obf_types_rev['name'], token[0]))
        for token in name_tokens:
            if self.obf_types[token[0]] == 'name':
                string = self.tokenizer.find_by_id(int(token[1]))[2]
                obf_var_name = self.strgen_for_variable.generateRandStr(
                    len(string), len(string) * self.obf_len_constant)
                token_index = self.tokenizer.find_index_by_id(token[1])
                for index in token_index:
                    current_token = self.tokenizer.TOKENS[index]
                    self.tokenizer.TOKENS[index] = (
                        current_token[0], current_token[1]
                        .replace(string, obf_var_name), obf_var_name)

        variables = self.tokenizer.get_variables()

        # Integer and Float Obfuscation
        for index, value in variables['integers'] + variables['floats']:
            current_token = self.tokenizer.TOKENS[index]
            obf_val = obfuscator(value)
            self.tokenizer.TOKENS[index] = (
                current_token[0], current_token[1],
                f'{self.deobfuscator_name}({obf_val})')

        # Boolean Obfuscation
        for index, value in variables['booleans']:
            current_token = self.tokenizer.TOKENS[index]
            obf_val = obfuscator(value)
            self.tokenizer.TOKENS[index] = (
                current_token[0], current_token[1],
                f'bool({self.deobfuscator_name}({obf_val}))')

        # String Obfuscation
        for indexes, string in variables['strings']:
            start = self.tokenizer.TOKENS[indexes[0]]
            self.tokenizer.TOKENS[indexes[0]] = (
                *start[:2], f'{self.str_deobfuscator_name}({start[2]}')
            obf_string = self._escape(
                ''.join(chr(obfuscator(ord(c))) for c in string))
            self.tokenizer.TOKENS[indexes[1]] = (
                *self.tokenizer.TOKENS[indexes[1]][:2], obf_string)
            end = self.tokenizer.TOKENS[indexes[2]]
            self.tokenizer.TOKENS[indexes[2]] = (*end[:2], f'{end[2]})')

        self.save_obfuscated_file()

    def save_obfuscated_file(self):
        new_file_content = ''
        for index, token in enumerate(self.tokenizer.TOKENS[:4]):
            if token[2].startswith('#') or token[2] == '\n':
                new_file_content += token[2]
                self.tokenizer.TOKENS.pop(0)

        new_file_name = self.file_name.replace(
            "." + self.file_name.split('.')[len(self.file_name.split('.'))-1],
            self.obfx_ext)
        new_file_content += self.obfx_header + '\n'
        # Write deobfuscator functions
        new_file_content += f'{self.deobfuscator_name} = {self.deobfuscator}\n{self.str_deobfuscator_name} = {self.string_deobfuscator.format(self.deobfuscator_name)}\n'
        tokens = self.tokenizer.TOKENS
        for token in tokens:
            new_file_content += token[2]
        print(new_file_content)  # testing
        write_file(new_file_name, new_file_content)
