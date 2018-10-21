<p align="center">
  <img width="256" height="125" src="https://i.resimyukle.xyz/7b7xyb.png"><br/>
  <a href="https://github.com/PyObfx/PyObfx/issues"><img src="https://img.shields.io/github/issues/PyObfx/PyObfx.svg"/></a>
  <a href="https://github.com/PyObfx/PyObfx/blob/master/LICENSE"><img src="https://img.shields.io/github/license/PyObfx/PyObfx.svg"/></a>
  <a href="https://github.com/PyObfx/PyObfx/stargazers"><img src="https://img.shields.io/github/stars/PyObfx/PyObfx.svg"/></a>
  <a href="https://github.com/PyObfx/PyObfx/network"><img src="https://img.shields.io/github/forks/PyObfx/PyObfx.svg"/></a>
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
python3 PyObfx.py -f <file_name>
```

To pack the file after obfuscation: (Available packers are bz2, gz and lzma)
```
python3 PyObfx.py -f <file_name> -p <packer>
```

For other options, see:
```
python3 PyObfx.py -h
```

## License
This project is licensed under the GPL v3 License - see the [LICENSE.md](https://github.com/PyObfx/PyObfx/blob/master/LICENSE) file for details
