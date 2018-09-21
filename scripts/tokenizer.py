#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from pygments.lexers import Python3Lexer
from pygments.token import Token
from random import randint
import re


class Tokenizer:
    TOKENS = list()
    VARS = list()
    QUOTES = ["'", '"', '"""', "'''"]
    BOOLS = ['True', 'False']

    def __init__(self, data):
        def token_filter(tokens):
            new_tokens = list()
            for key, token in enumerate(tokens):
                if tokens[key][0] == Token.Text and tokens[key][1] == ' ' and \
                (tokens[key+1][1] == '=' or tokens[key-1][1] == '='): 
                    pass
                else:
                    new_tokens.append((tokens[key][0], \
                        re.sub('\t+', ' ', re.sub(' +', ' ', tokens[key][1]))))  # (?P<variable>.+)\s*=\s*(?P<value>.+)" # Use .strip here
            return new_tokens
        self._tokens = Python3Lexer().get_tokens(data)
        self._tokens = token_filter(token_filter(list(self._tokens))) # Avoid space char bug
        self._tokenize()

    def find_by_id(self, _id):
        for token in self.TOKENS:
            if token[0] == _id:
                return token
        return (None, None, None)

    def find_index_by_id(self, _id):
        index_list = list()
        for index, token in enumerate(self.TOKENS):
            if self.TOKENS[index][0] == _id:
                index_list.append(index)
        return index_list

    def get_next_token(self):
        return next(self._tokens)

    def get_tokens(self):
        return self.TOKENS

    def get_variables(self): # str | int | float | bool
       return self.VARS

    def _generate_id(self): # Generate ID
        while True:
            tok_id = randint(0, 1000)
            if tok_id in [i[0] for i in self.TOKENS]:
                continue
            return tok_id

    def _tokenize(self):
        check_dict = dict()
        str_vars, int_vars, float_vars, bool_vars = {}, {}, {}, {}
        for key, token in enumerate(self._tokens):
            # TOKENS
            toktype = self._tokens[key]
            tok_id = self._generate_id()
            tokvalue = token[1]
            if not str(tokvalue) in list(check_dict.keys()):
                check_dict[str(tokvalue)] = (tok_id, str(toktype))
                self.TOKENS.append((tok_id, str(toktype), str(tokvalue)))
            else:
                self.TOKENS.append((check_dict[tokvalue][0], check_dict[tokvalue][1], str(tokvalue)))
            #######
            # VARS
            if token[0] == Token.Name and self._tokens[key+1] == (Token.Operator, '='):
                name = token[1]
                if (self._tokens[key+2][0] == Token.Literal.String.Double or \
                    self._tokens[key+2][0] == Token.Literal.String.Single) and \
                    (self._tokens[key+2][1] in self.QUOTES):
                    text = ''
                    for tok in self._tokens[key+3:]:
                        if (tok[0] == Token.Literal.String.Double or tok[0] == Token.Literal.String.Single) \
                         and tok[1] in self.QUOTES:
                            str_vars[name] = text
                            break
                        text += tok[1]
                elif self._tokens[key+2][0] == Token.Literal.Number.Integer:
                    int_vars[name] = int(self._tokens[key+2][1])
                elif self._tokens[key+2][0] == Token.Literal.Number.Float: 
                    float_vars[name] = float(self._tokens[key+2][1])
                elif self._tokens[key+2][0] == Token.Keyword.Constant and self._tokens[key+2][1] in self.BOOLS:
                    bool_vars[name] = bool(self._tokens[key+2][1])
            self.VARS = [str_vars, int_vars, float_vars, bool_vars]
            #######
        del check_dict
