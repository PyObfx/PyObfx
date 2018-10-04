import platform
import time


class Log:
    states = {
            'error':('ERROR', '\033[91m'),
            'critical':('CRITICAL','\033[93m'),
            'info': ('INFO', '\033[92m')
            }
    _RESET = '\033[39m'
    def __init__(self, path=None):
        self.path = path
        self.os =  platform.system()


    def _write(self, msg, state):
        content = f"[{time.strftime('%X')}] {self.states[state][0]} {msg}"
        with open(self.path, 'a') as f:
            f.write(content)

    def _clear(self):  #only debugi
        try:
            open(self.path, 'w').close()
        except:
            pass

    def log(self, msg, state='info'):
        content = f"{self.states[state][1] if self.os == 'Linux' else ''}[{time.strftime('%X')}] {self.states[state][0]} {msg}{self._RESET}"
        print(content)
        if self.path:
            self._write(msg=msg, state=state)


if __name__ == '__main__':
    logger = Log('log.txt')
    logger._clear()
    logger.log('Obfuscating strings')
    time.sleep(1)
    logger.log('Replacing bad chars', state='critical')
    time.sleep(1)
    logger.log('Obfuscate fail', state='error')

