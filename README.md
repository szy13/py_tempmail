# tempmail
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

The tempmail.net interaction module based on web scraping.

![license](https://img.shields.io/github/license/szy13/py_tempmail)
[![telegram](https://img.shields.io/badge/telegram-szyxiii-blue)](https://t.me/szyxiii)

## Requirements
* [requests](https://pypi.org/project/requests/) - http(s) library
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) - web scraping library


## Installation
Legacy setup
```
$ python3 setup.py install
```
Pip
```
No pip installation for now
```

## Usage
Get random email address
```python
from tempmail import TempMail

tm = TempMail()

email = tm.get_address()
print('Email address is', email.address)
```

Get email address inbox messages
```python
from tempmail import TempMail

tm = TempMail()

email = tm.get_address()
print('Email address is', email.address)

messages = email.get_messages()
if not messages:
    print("[No inbox messages]")
else:
    for message in messages:
        print('Message:\n', str(message))
        print('Content:\n', message.content)
        print()
```