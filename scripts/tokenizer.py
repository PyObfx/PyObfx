#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import re
from pygments.lexers import Python3Lexer
from pygments.token import Token
from random import randint

class Tokenizer:
    TOKENS = list()
    VARS = list()
    QUOTES = ["'", '"', '"""', "'''"]
    BOOLEAN = ['True', 'False']

    def __init__(self, data):
        # Token filter for handling space character
        # Remove spaces because we will parse the
        # variables according to that
        def token_filter(tokens):
            new_tokens = list()
            for key, token in enumerate(tokens):
                if tokens[key][0] == Token.Text and tokens[key][1] == ' ' and \
                        (tokens[key+1][1] == '=' or tokens[key-1][1] == '=') \
                        and not tokens[key][1] == '    ':
                    pass # Space char
                else:
                    # (?P<variable>.+)\s*=\s*(?P<value>.+)" # Use .strip here
                    # Don't change tabs. Remove spaces.
                    new_tokens.append((tokens[key][0], 
                                       re.sub(' +', ' ', 
                                       re.sub('    ', '\t', tokens[key][1]))))  
            return new_tokens
        # Get tokens
        self._tokens = Python3Lexer().get_tokens(data)
        # Filter tokens twice (to avoid space char bug)
        self._tokens = token_filter(
            token_filter(list(self._tokens)))
        # Tokenize
        self._tokenize()

    # Get token by id
    def find_by_id(self, _id):
        for token in self.TOKENS:
            if token[0] == _id:
                return token
        return (None, None, None)

    # Get token index(s) by id
    def find_index_by_id(self, _id):
        index_list = list()
        for index, token in enumerate(self.TOKENS):
            if self.TOKENS[index][0] == _id:
                index_list.append(index)
        return index_list

    # Get next token for testing purposes
    def get_next_token(self):
        return next(self._tokens)

    # Return all tokens
    def get_tokens(self):
        return self.TOKENS

    # Return parsed variable dict
    def get_variables(self):  # str | int | float | bool
        return self.VARS

    # Generate ID for tokens
    def _generate_id(self):
        while True:
            tok_id = randint(0, 1000)
            if tok_id in [i[0] for i in self.TOKENS]:
                continue
            return tok_id

    # Main tokenizer function
    def _tokenize(self):
        # Create a dict for checking token IDs
        # and assigning unique ID for every token
        check_dict = dict()
        # Create lists for every variable type
        str_vars, int_vars, float_vars, bool_vars = [], [], [], []
        # Tokenizer loop
        for key, token in enumerate(self._tokens):

            """ Get tokens and assign ID for every single token """
            current_token = self._tokens[key]
            tok_id = self._generate_id()
            token_value = token[1]
            # Check if function.name token is a string
            # to avoid function name and string type conflicts
            if token[0] == Token.Literal.String.Double or token[0] == Token.Literal.String.Single:
                self.TOKENS.append((tok_id, current_token, str(token_value)))
                continue
            # After checking the ID-token dictionary
            # add token to list
            if not str(token_value) in list(check_dict.keys()):
                check_dict[str(token_value)] = (tok_id, current_token)
                self.TOKENS.append((tok_id, current_token, str(token_value)))
            else:
                self.TOKENS.append(
                    (check_dict[token_value][0], check_dict[token_value][1], str(token_value)))

            """ Parse variables and create a variable dictionary """
            # Determine if current token is a variable declaration
            # with checking the next char (=)
            if token[0] == Token.Name and self._tokens[key+1] == (Token.Operator, '='):
                # Check string
                # Look for next and previous chars ( " | ' )
                if (self._tokens[key+2][0] == Token.Literal.String.Double or
                        self._tokens[key+2][0] == Token.Literal.String.Single) and \
                        (self._tokens[key+2][1] in self.QUOTES):
                    text = ''
                    keys = []
                    keys.append(key+2)
                    # Parse string value and add to list
                    for k, tok in enumerate(self._tokens[key+3:]):
                        keys.append(key+3+k)
                        if (tok[0] == Token.Literal.String.Double or tok[0] == Token.Literal.String.Single) \
                                and tok[1] in self.QUOTES:
                            str_vars.append((keys, text))
                            break
                        text += tok[1]
                # Check integer
                elif self._tokens[key+2][0] == Token.Literal.Number.Integer:
                    int_vars.append((key+2, int(self._tokens[key+2][1])))
                # Check float
                elif self._tokens[key+2][0] == Token.Literal.Number.Float:
                    float_vars.append((key+2, float(self._tokens[key+2][1])))
                # Check boolean
                elif self._tokens[key+2][0] == Token.Keyword.Constant and self._tokens[key+2][1] in self.BOOLEAN:
                    bool_vars.append((key+2, bool(self._tokens[key+2][1])))

            # Create a dict for every variable type and values
            self.VARS = {
                'strings': str_vars,
                'integers': int_vars,
                'floats': float_vars,
                'booleans': bool_vars
            }

        # Delete ID-token dictionary
        del check_dict
