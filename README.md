# scorer.py
A simple python script to fetch cricket scores and send notifications.

## NOTE ##
* This project is going massive changes.
Much of the code in the master branch is broken because of a lot of hardcoding.
The code is being fixed in the structureCode branch.
* If you want to run the code, checkout the structureCode branch and the do the
following 
cd scorer.py/scorer/
python app.py

![alt tag](http://i.imgur.com/LiMUo5V.png)

## Features ##
* Allows you to choose from concurrent matches
* Change choice by Ctrl+C
* Quit by Ctrl+C twice
* Shows notification only if there's a change in the score (run or wicket)
* Should work with python2 or python3

## Requirements ##
* Install python dependencies using `pip install -r requirements.txt`
* libnotify, BeautifulSoup
* Internet connection

## Usage ##
python scorer.py (If you checked out the master branch)

## Todo ##
* Use argparse to add some command line arguments like debug etc.
* Use the pushbullet api and allow users to get notifications on their devices using pushbullet.
* Use telegram api to make something similar to Natasha on hike.
* Use the matchid from current url and use the cricinfo api to get other notification like overs, batsmen playing, and other such stats when there is no change in the score.
* create a command line option to run this notification system as a GUI.
* Use twitter api to get the latest tweets based on match hastags and use it to feed the notifications when there is no score change.
* Use a configuration file
* Use arrows to navigate the command line interface. 
* Add documentation
* Add an option for proxy server host and port
* Add unit tests
That's all I could think for now.

**NOTE:** Works on Linux only. For OS X version, check this [project](https://github.com/avinassh/score-notify).
