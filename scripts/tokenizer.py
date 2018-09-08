#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from pygments.lexers import Python3Lexer
from pygments.token import Token


def tokenize(data):
    lex = Python3Lexer()
    return_dic = {}

    variables = []
    strings = []
    operators = []
    punctuation = []
    docs_str = []
    comments = []

    for toktype, tokvalue in lex.get_tokens(data):
        if toktype is Token.Name:
            variables.append(tokvalue)
        elif toktype is Token.Literal.String.Double or toktype is Token.Literal.String.Single:
            strings.append(tokvalue)
        elif toktype is Token.Operator.Word:
            operators.append(tokvalue)
        elif toktype is Token.Punctuation:
            punctuation.append(tokvalue)
        elif toktype is Token.Literal.String.Doc:
            docs_str.append(tokvalue)
        elif toktype is Token.Comment.Single:
            comments.append(tokvalue)

        #print(f" {toktype} --> {tokvalue}  ")

    return_dic = {
        'variables': variables,
        'strings': strings,
        'operators': operators,
        'punctuation': punctuation,
        'docs_str': docs_str,
        'comments': comments,
    }
    return return_dic
