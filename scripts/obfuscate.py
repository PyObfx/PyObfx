#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import hashlib

class Obfuscate:
    def __init__(self, file_content):
        self.file_content = file_content
        #obfuscation will be done here

    MD5 = lambda s: hashlib.md5(s.encode('utf-8')).hexdigest()

    def obfuscate_string1(self, s):
        out = [0]
        for c in s:
            out.extend([(ord(c) / 3) + (out[-1] % 2), 0])
        return out

    def deobfuscate_string1(self, s):
        out = ''
        for i in range(1, len(s), 2):
            out += chr(int((s[i] - (s[i-1] % 2)) * 3))

        return out

    def obfuscate_string2(self, s):
        rot13 = str.maketrans(
            'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
            'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm'
        )
        return s.translate(rot13)


    def deobfuscate_string2(self, s):
        rot13 = str.maketrans(
            'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm',
            'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz'
        )
        return s.translate(rot13)