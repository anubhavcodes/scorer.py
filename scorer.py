#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from gi.repository import Notify
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG)

def sendmessage(title, message):
    logging.debug("Initializing the Notification system")
    Notify.init("Scorer")
    logging.debug("Calling the notifiction system with the parameters: title: {}, score:{}".format(title, message))
    scorer = Notify.Notification.new(title, message, "dialog-information")
    logging.info("showing score")
    scorer.show()
    return


url = "http://static.cricinfo.com/rss/livescores.xml"
match = 0
score = ""
interrupted=False

print("Fetching matches..")
while True:
    try:
        logging.info("Sending requests")
        r = requests.get(url)
        while r.status_code is not 200:
            logging.debug("Request failed: trying again")
            sleep(2)
            r = requests.get(url)
        soup = BeautifulSoup(r.text)
        data = soup.find_all("description")
        logging.debug("Found the following from scrapping: {}".format(data))
        if match == 0:
            print("Matches available:")
            counter = 1
            for game in data[1:]:
                print(counter, game.text)
                counter += 1
            match = int(input("Enter your choice: "))
            interrupted=False
        newscore = data[match].text
        logging.info("Score found is {}".format(newscore))
        if newscore != score:
            logging.info("This is the most recent score, send me a notification")
            score = newscore
            sendmessage("Score", score)
        sleep(15)

    except KeyboardInterrupt:
        if interrupted:
            logging.info("keyboard interrupted, once")
            print("Bye bye")
            break
        else:
            print("Press Ctrl+C again to quit")
            match = 0
            interrupted=True
