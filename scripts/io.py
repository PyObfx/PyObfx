import os

from pygments.lexers import Python3Lexer
from pygments.token import Token

#BASEDIR  = os.path.dirname(os.path.realpath(__file__))


def read_file(filename):
    with open(filename) as file:
        data = file.read()

    return data

def tokenize(data):
    lex = Python3Lexer()
    return_dic = {}

    veriables = []
    strings = []
    operators = []
    punctuation = []
    docs_str = []
    commnets = []

    for toktype, tokvalue in lex.get_tokens(data):
        if toktype is Token.Name:
            veriables.append(tokvalue)
        elif toktype is Token.Literal.String.Double or toktype is Token.Literal.String.Single:
            strings.append(tokvalue)
        elif toktype is Token.Operator.Word:
            operators.append(tokvalue)
        elif toktype is Token.Punctuation:
            punctuation.append(tokvalue)
        elif toktype is Token.Literal.String.Doc:
            docs_str.append(tokvalue)
        elif toktype is Token.Comment.Single:
            commnets.append(tokvalue)

        #print(f" {toktype} --> {tokvalue}  ")

    return_dic = {
        'veriables': veriables,
        'strings': strings,
        'operators': operators,
        'punctuation': punctuation,
        'docs_str': docs_str,
        'commnets': commnets,
    }
    return return_dic


if __name__ == '__main__':
    pass
