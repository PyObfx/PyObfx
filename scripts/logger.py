#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
import platform
import time

class Log:
    states = {
            'error':('[ERROR]', '\033[91m'),
            'critical':('[CRITICAL]','\033[93m'),
            'info': ('[INFO]', '\033[92m')
            }
    _RESET = '\033[39m'
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
        content = f"{self.states[state][1] if self.os == 'Linux' else ''}[{time.strftime('%X')}] {self.states[state][0]} {msg}{self._RESET}"
        print(content)
        if self.path:
            self._write(msg=msg, state=state)


