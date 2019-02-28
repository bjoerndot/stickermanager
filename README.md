# Sticker Manager Bot (0.1.0)
Telegram Bot to handle Sticker-Management in a streamlined way

## Installation

In order to run, this script needs the following packages:
- Python3.7
- Python Telegram Bot
```
pip install python-telegram-bot
```

- pyArango
```
pip install pyarango
```

It uses requires following Python-packages:
- random
- logging
- datetime
- re

## Organization
_The script is split by use into different part:_

`stickermanager.py` - holds the functionality for handling stickers

_It uses a couple of other scripts included in this repository, like:_

`datetime_util.py` - contains a couple of functions for converting strings and datetime-objects to a desired output

`arango_utils` - contains a couple of functions, to easily access the arango-database

## Future development
Any future features will be setup as issues containing one of the following tags:

- *new command*: Idea for new command for BOTler
- *enhancement*: Existing command can be enhanced
- *wording*: Wording/given information needs to be adjusted

## Versioning
x.y.z

x = Major update, which involves a completely new functionality

y = Minor update, which involves new commands added to existing functionality

z = Bugfixes and others
