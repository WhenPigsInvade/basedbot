# BasedBot -- written in Python
Discord Bot which keeps track of frequently said words and displays leaderboard.

## Table of Contents
* [Introduction](#introduction)
* [Installation](#installation)
* [Configurations](#configurations)
* [Change Log](#change-log)

## Introduction
BasedBot's main feature is keeping track of how many times a user says a certain phrase in a leaderboard. 
BasedBot can also reply to certain phrases or keywords with unique responses.

Our team plans to include a database overhaul soon, as well as including time stamps for leaderboard reset.


## Installation
If you want to run BasedBot on your own server you will have to install the following:

* [Python 3.x](https://nodejs.org)
* [Discord.py](https://discord.js.org/#/)
* [asyncio](https://docs.python.org/3/library/asyncio.html)

or use `pip install requirements.txt` to install all required libraries

## Configurations

BasedBot has the following commands

* `keywords`
  * `add`
  * `delete`
  * `reset` --TODO
  
* `top` [keyword]
* `help`
* `log`

As well as custom responses to the follow phrases:

* brb
* f
* @everyone
* (or when mentioned)
* (common mispellings of the word "Elliott") -- TODO

## Change log
2.0.1 - 4/22/2023
* Added most missing cosmetic features from 1.x.x
* Now has randomized quotes after embed blocks
* Now utilizes asyncio for its delayed response to prevent back logging

2.0.0 - 9/6/2022
* Bot was rewritten in Python. Now also implements SQLlite for database efficiency.

1.1.2 - 1/3/2022
* Only updates userdata and serverdata every 30 mins provided there is change to improve efficiency.

1.1.1 - 8/29/2021
* Now prompts user if they want to delete keyword for real.
* Adjusted ~keywords spacing
* ~keywords reset added
* keyword logging per server now increased to 10

1.1.0 - 8/24/2021
* Now has a proper response for ~log when bot does not have MANAGE_MESSAGES permission.
* Can now add and delete keywords to word logging, needs MANAGE_MESSAGES permission.
* Moved ~top back onto the leaderboard folder for clarity.

1.0.6 - 8/17/2021
* New ~log command
* Restructured code for organization

1.0.5 - 8/8/2021
* Now properly checks for word, ie. hello != ehellos
* Searching for a word no longer counts it, ie. ~top hello will not increase your word count for hello (as long as a message begins with prefix it will not count it)
* New responses when pinged

1.0.4 - 7.18.2021
* Removed username property from userdata.json
* Reformated leaderboard to show username first
* Elliot now searches properly

1.0.3 - 7.17.2021
* Elliot reply added
* Leaderboard now uses embeds
* New reply for ~help

1.0.2 - 7.3.2021
* Leaderboard now sorts
* Leaderboard now displays updated username
* No longer keeps track of user username when initiating new user file

1.0.1 - 6.24.2021
* Editted leaderboard formating on mobile
* Now ignores other bots
* Editted reply for 'f'
* Added replies when mentioned
* Moved ~top to its own module
* Added custom status

1.0.0 - 6.20.2021
* First "public" release of BasedBot. Keeps track of keyword counts per user. 2 custom response. (brb, F)

