<p align="center">
  <img width="600" height="197" src="https://user-images.githubusercontent.com/24392180/60277578-86af4e00-9906-11e9-8c60-fed3de02b449.png"><br/>
  <a href="https://github.com/PyObfx/PyObfx/releases"><img src="https://img.shields.io/github/release/PyObfx/PyObfx.svg"/></a>
  <a href="https://github.com/PyObfx/PyObfx/issues"><img src="https://img.shields.io/github/issues/PyObfx/PyObfx.svg"/></a>
  <a href="https://github.com/PyObfx/PyObfx/pulls"><img src="https://img.shields.io/github/issues-pr/PyObfx/PyObfx.svg"/></a>
  <a href="https://github.com/PyObfx/PyObfx/stargazers"><img src="https://img.shields.io/github/stars/PyObfx/PyObfx.svg"/></a>
  <a href="https://github.com/PyObfx/PyObfx/network"><img src="https://img.shields.io/github/forks/PyObfx/PyObfx.svg"/></a>
  <a href="https://github.com/PyObfx/PyObfx/blob/master/LICENSE"><img src="https://img.shields.io/github/license/PyObfx/PyObfx.svg"/></a>
</p>

# PyObfx
Python Obfuscation tool

## Features
* String, Integer, Float and Boolean Obfuscation
* Variable Name Obfuscation
* Import Name Obfuscation
* Packing

## Installation

```
git clone https://github.com/PyObfx/PyObfx.git && cd PyObfx/
pip install -r requirements.txt
```

## Usage

<p align="center">
  <a href="https://asciinema.org/a/207739" target="_blank"><img src="https://asciinema.org/a/207739.png" /></a>
</p>

In order to obfuscate a single file:
```
python3 PyObfx.py <file_name>
```

To pack the file after obfuscation: (Available packers are bz2, gz and lzma)
```
python3 PyObfx.py <file_name> -p <packer>
```

For other options, see:
```
python3 PyObfx.py -h
```
## Results
Before Obfuscating:
```python
import os as oss
import random as rnd
import time as wow_time
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

test_str = "<- Test ->"
real_test_str   =   "x"
test_float = 9.9
test_int = 0
test_bool = True
hi = "Hi! \n"

def main():
    print(test_float)
    print(test_int)
    print(test_bool)
    print(hi + " " + test_str)
    print(rnd.randint(5, 15))
    wow_time.sleep(1)
    """docstring"""
    def awesome():
    	print("awesome") # Awesome
    	print("\t+\'is this really working?\'\n" + "\t-\"oh, it is\"")
    awesome()
    print(""" multiline string """)

if __name__ == "__main__":
    main()
```
After Obfuscating:
```python
import os as HzIufY
import random as bsSOod
import time as xydWSaztIpRmlqvr
import socket as SsKHeNIacbCE

HfRtJhXqkg = lambda n: (n - (5 % 5)) - 2
RboljamGsh = lambda s: ''.join(chr(int(HfRtJhXqkg(ord(c)))) for c in s)

CY = SsKHeNIacbCE.socket(SsKHeNIacbCE.AF_INET,SsKHeNIacbCE.SOCK_STREAM)

ZJgMixQLFvIOVkWATrhdDPjaHNsfKqBn = RboljamGsh(">/\"Vguv\"/@")
sCIhJLAvexrBHnMtZYjRzgwqGu   =   RboljamGsh("z")
dgsHVSxQucJwrLWbYoflXFzZyAUTmjOkqtBnvpGK = HfRtJhXqkg(11.9)
KzcOpAuoPlXrTEvZSYLgByidFDaUwetM = int(HfRtJhXqkg(2))
QiKPneOHJCIFEWxyYvXcshTquMAULdSBZrpw = bool(int(HfRtJhXqkg(3)))
HEUcxPKD = RboljamGsh("Jk#\"\f")

def fiZdbpzr():
    print(dgsHVSxQucJwrLWbYoflXFzZyAUTmjOkqtBnvpGK)
    print(KzcOpAuoPlXrTEvZSYLgByidFDaUwetM)
    print(QiKPneOHJCIFEWxyYvXcshTquMAULdSBZrpw)
    print(HEUcxPKD + RboljamGsh("\"") + ZJgMixQLFvIOVkWATrhdDPjaHNsfKqBn)
    print(bsSOod.randint(int(HfRtJhXqkg(7)), int(HfRtJhXqkg(17))))
    xydWSaztIpRmlqvr.sleep(int(HfRtJhXqkg(3)))
    """docstring"""
    def CNgSHDbrXecMZi():
    	print(RboljamGsh("cyguqog")) # Awesome
    	print(RboljamGsh("\v-)ku\"vjku\"tgcnn{\"yqtmkpiA)\f") + RboljamGsh("\v/$qj.\"kv\"ku$"))
    CNgSHDbrXecMZi()
    print(""" multiline string """)

if __name__ == RboljamGsh("aaockpaa"):
    fiZdbpzr()

```
## License
This project is licensed under the GPL v3 License - see the [LICENSE](https://github.com/PyObfx/PyObfx/blob/master/LICENSE) file for details.
