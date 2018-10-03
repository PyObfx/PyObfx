#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import random
from scripts.tokenizer import Tokenizer
from scripts.strgen import generate_rand_str as StringGenerator
from pygments.token import Token
from scripts.io import read_file, write_file


class Obfuscator:
    def __init__(self, file_name):
        # Header for obfuscated file
        self.obfx_header = "# Obfuscated with PyObfx #"
        # File name and content
        self.file_name = file_name
        self.file_content = read_file(file_name)
        # Tokenize the source and retrieve tokenizer object
        self.tokenizer = Tokenizer(self.file_content)
        # Random integers for obfuscation
        self.ints = [random.randint(1, 5) for _ in range(3)]
        # Deobfuscator declarations
        self.deobfuscators = {
            1: "lambda n: (n - ({} % {})) - {}".format(*self.ints[::-1]),
            2: "lambda n: int((n ^ {}) / {})".format(*self.ints[:2]),
            3: "lambda n: n - sum({})".format(str(self.ints))
        }
        # Length constant for random string
        self.obf_len_constant = 2
        # Quote character distance from string (max)
        self.quote_dist_constant = 5
        # String generator
        self.strgen_for_variable = StringGenerator(1)
        # New file extension for obfuscated file
        self.obfx_ext = "_obfx.py"
        # Randomized deobfuscator function names
        self.deobfuscator_name = self.strgen_for_variable.generateRandStr(
            2, 10)
        self.str_deobfuscator_name = self.strgen_for_variable.generateRandStr(
            2, 10)

    # str.format with int deobfuscator name
    string_deobfuscator = "lambda s: ''.join(chr({}(ord(c))) for c in s)"

    # Obfuscator methods
    def obfuscation1(self, n):
        return (n + self.ints[0]) + (self.ints[2] % self.ints[1])
    def obfuscation2(self, n): return (n * self.ints[1]) ^ self.ints[0]
    def obfuscation3(self, n): return n + sum(self.ints)

    # Escape string
    def _escape(self, s):
        return s.replace('"', r'\"').replace("'", r"\'")

    def _obfuscate_names(self, token_type):
        # Iterate through the tokens and check if
        # token type is Token.Name
        for token in self.tokenizer.TOKENS:
            if token[1][0] == token_type:
                # Get the name value
                name_value = token[2]
                # Obfuscate the name string
                obf_var_name = self.strgen_for_variable.generateRandStr(len(name_value), len(name_value) * self.obf_len_constant)
                # Find usages for current name with find_index_by_id method
                token_index = self.tokenizer.find_index_by_id(token[0])
                # Iterate through the indexes and change current value with
                # new obfuscated value
                for index in token_index:
                    current_token = self.tokenizer.TOKENS[index]
                    # Change list element
                    self.tokenizer.TOKENS[index] = (current_token[0], (Token.Name, obf_var_name), obf_var_name)
                    
    def _obfuscate_var_values(self, obfuscator):
        # Get parsed variables from tokenizer
        variables = self.tokenizer.get_variables()

        # Integer and Float Obfuscation
        for index, value in variables['integers'] + variables['floats']:
            # Get token
            current_token = self.tokenizer.TOKENS[index]
            # Obfuscate variable value
            obf_val = obfuscator(value)
            # Update token list
            self.tokenizer.TOKENS[index] = (
                current_token[0], current_token[1],
                f'{self.deobfuscator_name}({obf_val})')

        # Boolean Obfuscation
        for index, value in variables['booleans']:
            # Get token
            current_token = self.tokenizer.TOKENS[index]
             # Obfuscate variable value
            obf_val = obfuscator(value)
            # Update token list
            self.tokenizer.TOKENS[index] = (
                current_token[0], current_token[1],
                f'bool({self.deobfuscator_name}({obf_val}))')

        # String Obfuscation
        for indexes, string in variables['strings']:
            # Get first quote
            start = self.tokenizer.TOKENS[indexes[0]]
            # Change quote with obfuscator method
            self.tokenizer.TOKENS[indexes[0]] = (
                *start[:2], f'{self.str_deobfuscator_name}({start[2]}')
            # Obfuscate string value
            obf_string = self._escape(
                ''.join(chr(obfuscator(ord(c))) for c in string))
            # Change last quote with parentheses and update token list
            self.tokenizer.TOKENS[indexes[1]] = (
                *self.tokenizer.TOKENS[indexes[1]][:2], obf_string)
            end = self.tokenizer.TOKENS[indexes[2]]
            self.tokenizer.TOKENS[indexes[2]] = (*end[:2], f'{end[2]})')

        # Function Strings Obfuscation
        for index, string in variables['strings_func']:
            # Get token
            current_token = self.tokenizer.find_by_id(index)
            # Check if string is changed before.
            # Some function strings and normal strings have
            # same types. So, if condition is necessary. 
            # If value of current token changed before,
            # it is not the string we are looking for.
            if string == current_token[2]:
                # Obfuscate the string
                # (eg.: <deobfuscator_name>('<obfuscated_string>'))
                obf_string = self.str_deobfuscator_name + "(\"" + self._escape(
                ''.join(chr(obfuscator(ord(c))) for c in string)) + "\")"
                # Find usages for current token with find_index_by_id method
                token_index = self.tokenizer.find_index_by_id(current_token[0])
                # Iterate through the indexes and change current value with
                # new obfuscated value
                for index in token_index:
                    token = self.tokenizer.TOKENS[index]
                    self.tokenizer.TOKENS[index] = (token[0], (Token.Name, obf_string), obf_string)
                    # Pop unnecessary escape characters
                    # (eg.: print("deobf("test")") -> Quote is unnecessary)
                    for n_index in range(self.quote_dist_constant):
                        if self.tokenizer.TOKENS[index-n_index][2] in self.tokenizer.QUOTES:
                            self.tokenizer.TOKENS.pop(index-n_index)
                            self.tokenizer.TOKENS.pop(index)

    def obfuscate(self, obfuscation=1):
        # Declare obfuscator
        obfuscators = {1: self.obfuscation1, 2: self.obfuscation2, 3: self.obfuscation3}
        # Select obfuscator
        obfuscator = obfuscators[obfuscation]
        self.deobfuscator = self.deobfuscators[obfuscation]
        # Variable Name Obfuscation
        self._obfuscate_names(Token.Name)
        # Function Name Obfuscation
        self._obfuscate_names(Token.Name.Function)
        # Variable Value Obfuscation
        self._obfuscate_var_values(obfuscator)
        # Save file
        self.save_obfuscated_file()


    def save_obfuscated_file(self):
        new_file_content = ''
        # Shebang check & fix
        for index, token in enumerate(self.tokenizer.TOKENS[:4]):
            if token[2].startswith('#') or token[2] == '\n':
                new_file_content += token[2]
                self.tokenizer.TOKENS.pop(0)
        # New file name
        new_file_name = self.file_name.replace(
            "." + self.file_name.split('.')[len(self.file_name.split('.'))-1],
            self.obfx_ext)
        # Add header
        new_file_content += self.obfx_header + '\n'
        # Write deobfuscator functions
        new_file_content += f'{self.deobfuscator_name} = {self.deobfuscator}\n{self.str_deobfuscator_name} = {self.string_deobfuscator.format(self.deobfuscator_name)}\n'
        # Write new file 
        for token in self.tokenizer.TOKENS:
            new_file_content += token[2]
        write_file(new_file_name, new_file_content)
        print("Successfully obfuscated.\nSaved to: " + new_file_name)
        print(new_file_content)  # testing
