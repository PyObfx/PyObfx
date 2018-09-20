#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from pygments.lexers import Python3Lexer
from pygments.token import Token
from random import randint


class Tokenizer:
    TOKENS = list()

    def __init__(self, data):
        self._tokens = Python3Lexer().get_tokens(data)
        self.tokenize()

    def genenate_id(self):
        while True:
            tok_id = randint(0, 1000)
            if tok_id in [i[0] for i in self.TOKENS]:
                continue
            return tok_id

    def find_by_id(self, _id):
        for token in self.TOKENS:
            if token[0] == _id:
                return token
        return (None, None, None)

    def get_next_token(self):
        return next(self._tokens)

    def tokenize(self):
        check_dict = dict()
        for toktype, tokvalue in self._tokens:
            tok_id = self.genenate_id()
            if not str(tokvalue) in list(check_dict.keys()):
                check_dict[str(tokvalue)] = (tok_id, str(toktype))
                self.TOKENS.append((tok_id, str(toktype), str(tokvalue)) )
            else:
                self.TOKENS.append((check_dict[tokvalue][0], check_dict[tokvalue][1], str(tokvalue)))       
        del check_dict
            #print(f"{toktype} --> {repr(tokvalue)}  ")
