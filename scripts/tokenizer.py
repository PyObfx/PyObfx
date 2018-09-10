#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from pygments.lexers import Python3Lexer
from pygments.token import Token


class Tokenizer:
    """ 
        Tokenizer class: 
            @param data: source code

        Usage:
            tokenizer = Tokenizer(source_code)
            tokenizer.tokenize()

            # also
            tokenizer.get_next_token()  #---> get one token
    """

    def __init__(self, data):
        self.tokens = Python3Lexer().get_tokens(data)

    def get_next_token(self):
        return next(self.tokens)

    def tokenize(self):
        return_dic = {}

        variables = []
        strings = []
        operators = []
        punctuation = []
        docs_str = []
        comments = []
        namespaces = []
        keywords = []
        integers = []
        exceptions = []

        for toktype, tokvalue in self.tokens:
            if toktype is Token.Name.Namespace:
                namespaces.append(tokvalue)
                continue

            elif toktype is Token.Name.Exception:
                exceptions.append(tokvalue)
                continue

            elif toktype is Token.Literal.Number.Integer:
                integers.append(tokvalue)

            elif toktype is Token.Keyword:
                keywords.append(tokvalue)

            elif toktype is Token.Name:
                variables.append(tokvalue)

            elif toktype is Token.Literal.String.Double or toktype is Token.Literal.String.Single:
                strings.append(tokvalue)

            elif toktype is Token.Operator.Word or toktype is Token.Operator:
                operators.append(tokvalue)

            elif toktype is Token.Punctuation:
                punctuation.append(tokvalue)

            elif toktype is Token.Literal.String.Doc:
                docs_str.append(tokvalue)

            elif toktype is Token.Comment.Single:
                comments.append(tokvalue)

            #print(f" {toktype} --> {repr(tokvalue)}  ")

        return_dic = {
            'variables': variables,
            'strings': strings,
            'operators': operators,
            'punctuation': punctuation,
            'docs_str': docs_str,
            'commnets': comments,
            'namespaces': namespaces,
            'keywords': keywords,
            'integers': integers,
            'exceptions': exceptions,
        }
        return return_dic
