### Project Status
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI version sentry-kavenegar](https://img.shields.io/badge/Pypi%20Version-0.1.1-green.svg)](https://pypi.org/project/sentry-kavenegar/)
[![Pypi](https://img.shields.io/badge/Pypi-yes-green.svg)](https://pypi.org/project/sentry-kavenegar/)

# sentry-kavenegar
A plugin for [Sentry](https://www.getsentry.com/) that sends SMS notifications via [Kavenegar](https://kavenegar.com/)

**Note**: Only works with IR numbers, mostly because I'm too lazy to think about international phone numbers and what to do with them. Feel free to submit a pull request.

## Installation
`$ pip install sentry-kavenegar`

Sentry will automagically detect that it has been installed.

## Configuration
`sentry-kavenegar` needs 2 pieces of information to set this up correctly.

### Account SID & Auth Token
The Account API KEY can both be found on your [Kavenegar account dashboard](https://panel.kavenegar.com/client/setting/account).
![](http://i.imgur.com/XfrTV2R.png)

### SMS From # 
This is the number that was purchased through Kaveneger. [Kavenegar documentation for more information](https://kavenegar.com/rest.html).

Examples:
```
+98935XXXXXXX
// or
0912XXXXXXXX
```

### SMS To #'s
A list of phone numbers to send to separated by commas.

Example:
```
+98935XXXXXXX, 0912XXXXXXXX
```
