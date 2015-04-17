# scorer.py
A simple python script to fetch cricket scores and send notifications.

![alt tag](http://i.imgur.com/LiMUo5V.png)

## Features ##
* Allows you to choose from concurrent matches
* Change choice by arrow keys

## Requirements ##
* beautifulSoup4
* requests
* python2 only

## Installation ##
``sudo python setup.py install``
[Make sure you are using python2]

## Usage ##
``scorer``

## Todo ##
* Use argparse to add some command line arguments like debug etc.
* Use the pushbullet api and allow users to get notifications on their devices using pushbullet.
* Use telegram api to make something similar to Natasha on hike.
* Use the matchid from current url and use the cricinfo api to get other notification like overs, batsmen playing, and other such stats when there is no change in the score.
* create a command line option to run this notification system as a GUI.
* Use twitter api to get the latest tweets based on match hastags and use it to feed the notifications when there is no score change.
* Use a configuration file
* Add documentation
* Add an option for proxy server host and port
That's all I could think for now.

**NOTE:** Works on Linux only. For OS X version, check this [project](https://github.com/avinassh/score-notify).
