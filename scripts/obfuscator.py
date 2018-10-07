#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import random
from scripts.tokenizer import Tokenizer
from scripts.strgen import generate_rand_str
from pygments.token import Token
from scripts.io import read_file, write_file
from scripts.logger import Log
from scripts.packer import *

class Obfuscator:
    def __init__(self, args):
        # Logger
        self.logger = Log()
        # Header for obfuscated file
        self.obfx_header = "# Obfuscated with PyObfx #"
        # Escape placeholder
        self.escape_placeholder = "#escaped_char#"
        # Obfx arguments
        self.args = args
        # File name and content
        self.file_name = self.args['file']
        self.file_content = read_file(self.file_name)
        # Escape chars in file
        self.escaped_file = self._escape_file(self.file_content)
        # Tokenize the source and retrieve tokenizer object
        self.tokenizer = Tokenizer(self.escaped_file)
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
        # New file extension for obfuscated file
        self.obfx_ext = "_obfx.py"
        # Randomized deobfuscator function names
        self.deobfuscator_name = generate_rand_str(1, 10)
        self.str_deobfuscator_name = generate_rand_str(1, 10)
        # Quote list
        self.quotes = ["'", '"', '"""', "'''"]
        # Boolean value list
        self.boolean_val = ['True', 'False']
        # Escape Sequences
        self.escapes = [('\a', '\\a'), ('\b', '\\b'), \
        ('\f', '\\f'), ('\n', '\\n'), ('\r', '\\r'), \
         ('\t', '\\t'), ('\v', '\\v')]

    # str.format with int deobfuscator name
    string_deobfuscator = "lambda s: ''.join(chr({}(ord(c))) for c in s)"

    # Obfuscator methods
    def obfuscation1(self, n):
        return (n + self.ints[0]) + (self.ints[2] % self.ints[1])
    def obfuscation2(self, n): return (n * self.ints[1]) ^ self.ints[0]
    def obfuscation3(self, n): return n + sum(self.ints)

    # Escape string
    def _escape(self, s):
        s = s.replace('"', r'\"').replace("'", r"\'")
        for escape in self.escapes:
            s = s.replace(escape[0], escape[1])
        return s

    # Escape file
    # (eg.: Replace '\' with placeholder)
    def _escape_file(self, file_content):
        # Double quote
        file_content = file_content.replace("\\\"", "\\d")
        # Single quote
        file_content = file_content.replace("\\\'", "\\s")
        return file_content.replace("\\", self.escape_placeholder)

    # Unescape string using placeholder
    def _unescape_str(self, s):
        for escape in self.escapes:
            s = s.replace(self.escape_placeholder+escape[1].replace("\\", ""), escape[0])
        s = s.replace(self.escape_placeholder, '\\')
        # Single quote
        s = s.replace('\\s', '\'')
        # Double quote
        s = s.replace('\\d', '\"')
        return s

    def _obfuscate_names(self, token_type):
        # Iterate through the tokens and check if
        # token type is Token.Name
        for token in self.tokenizer.TOKENS:
            if token[1][0] == token_type:
                # Get the name value
                name_value = token[2]
                # Obfuscate the name string
                obf_var_name = generate_rand_str(1, len(name_value) * self.obf_len_constant)
                # Find usages for current name with find_index_by_id method
                token_index = self.tokenizer.find_index_by_id(token[0])
                # Iterate through the indexes and change current value with
                # new obfuscated value
                for index in token_index:
                    current_token = self.tokenizer.TOKENS[index]
                    # Change list element
                    self.tokenizer.TOKENS[index] = (current_token[0], 
                        (Token.Name, obf_var_name), obf_var_name)

    def _obfuscate_vars(self, obfuscator, token_type):
        # Inner function for type casting
        # [can be simplified]
        def cast(token):
            if token_type == Token.Literal.Number.Integer:
                return int(token)
            elif token_type == Token.Literal.Number.Float:
                return float(token)
            elif token_type == Token.Keyword.Constant:
                return bool(token)
        # Iterate through the tokens and check if
        # token type equals token_type
        for token in self.tokenizer.TOKENS:
            if token[1][0] == token_type:
                # Cast and obfuscate the value
                obf_val = obfuscator(cast(token[2]))
                # Find usages for current token
                token_index = self.tokenizer.find_index_by_id(token[0])
                # Update old values with new obfuscated values
                # If obfuscation type is a boolean obfuscation
                # don't forget to add casting to new string
                for index in token_index:
                    # Get token
                    current_token = self.tokenizer.TOKENS[index]
                    # Check boolean obfuscation
                    if token_type == Token.Keyword.Constant and \
                    current_token[2] in self.boolean_val:
                        # Add boolean casting [bool(...)]
                        # Update TOKENS
                        self.tokenizer.TOKENS[index] = (
                        current_token[0], current_token[1],
                        f'bool({self.deobfuscator_name}({obf_val}))')
                    else:
                        # Update TOKENS
                        self.tokenizer.TOKENS[index] = (
                        current_token[0], current_token[1],
                        f'{self.deobfuscator_name}({obf_val})')

    def _obfuscate_strings(self, obfuscator):
        # Iterate through the tokens and make sure
        # current token is string and not an unnecessary
        # char (quote)
        for token in self.tokenizer.TOKENS:
            if token[1][0] == Token.Literal.String.Double and not token[2] in self.quotes or \
            token[1][0] == Token.Literal.String.Single and not token[2] in self.quotes: 
                string_value = self._unescape_str(token[2])
                # String obfuscation procedure
                obfuscated = ''
                # Obfuscate chars in string
                for c in string_value:
                    obfuscated += ''.join(chr(obfuscator(ord(c))))
                # Create obfuscated string
                # (eg.: <deobfuscator_name>('<obfuscated_string>'))
                obf_string = self.str_deobfuscator_name + "(\"" + self._escape(obfuscated) + "\")"
                # Find usages for current token
                token_index = self.tokenizer.find_index_by_id(token[0])
                # Iterate through the indexes and change current value with
                # new obfuscated value
                for index in token_index:
                    current_token = self.tokenizer.TOKENS[index]
                    self.tokenizer.TOKENS[index] = (current_token[0], 
                        (Token.Name, obf_string), obf_string)
                    # Pop unnecessary escape characters
                    # (eg.: print("deobf("test")") -> Quote is unnecessary)
                    for n_index in range(self.quote_dist_constant):
                        if self.tokenizer.TOKENS[index-n_index][2] in self.quotes:
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
        # Integer Obfuscation
        self._obfuscate_vars(obfuscator, 
            Token.Literal.Number.Integer)
        # Float Obfuscation
        self._obfuscate_vars(obfuscator, 
            Token.Literal.Number.Float)
        # Boolean Obfuscation
        self._obfuscate_vars(obfuscator, 
            Token.Keyword.Constant)
        # String Obfuscation
        self._obfuscate_strings(obfuscator)
        # Save file
        self._save_obfuscated_file()

    def _save_obfuscated_file(self):
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
        # Create new file content from tokens 
        for token in self.tokenizer.TOKENS:
            new_file_content += token[2]
        # Pack
        new_file_content = self._pack(new_file_content)
        # Write file
        write_file(new_file_name, new_file_content)
        print("Successfully obfuscated.\nSaved to: " + new_file_name)
        print(new_file_content)  # testing

    def _pack(self, file_content):
        # Packer functions
        packer_dispatcher = {
            'bz2': bz2_pack(file_content),
            'gz': gz_pack(file_content),
            'lzma': lzma_pack(file_content)
        }
        # Pack file if -p argument is provided and packer type is valid
        try:
            file_content = packer_dispatcher[self.args['pack']]
        except KeyError:
            pass
        return file_content