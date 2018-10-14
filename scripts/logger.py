#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from colorama import Fore, Style
import platform
import time

class Log:
    states = {
            'error':('[ERROR]', Fore.RED),
            'critical':('[CRITICAL]',Fore.YELLOW),
            'info': ('[INFO]', Fore.GREEN)
            }
    _RESET = Fore.RESET
    def __init__(self, path=None):
        self.path = path
        self.os = platform.system()

    def _write(self, msg, state):
        content = f"[{time.strftime('%X')}] {self.states[state][0]} {msg}"
        with open(self.path, 'a') as f:
            f.write(content)

    def _clear(self):
        try:
            open(self.path, 'w').close()
        except:
            pass

    def log(self, msg, state='info'):
        content = f"{Style.BRIGHT}{self.states[state][1] if self.os == 'Linux' else ''}[{time.strftime('%X')}] {self.states[state][0]} {msg}{self._RESET}{Style.RESET_ALL}"
        print(content)
        if self.path:
            self._write(msg=msg, state=state)

