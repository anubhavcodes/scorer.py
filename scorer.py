#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from gi.repository import Notify
from time import sleep


def sendmessage(title, message):
    Notify.init("Scorer")
    Notify.Notification.new(title, message, "dialog-information").show()


url, match, score, interrupted = "http://static.cricinfo.com/rss/livescores.xml", 0, "", False

print("Fetching matches..")
while True:
    try:
        # Sleep for two seconds and keep on trying to get the url, if failed with `HTTPError`
        while True:
            r = requests.get(url)
            try:
                r.raise_for_status()
                break
            except requests.exceptions.HTTPError as err:
                print("Request failed with", err)
                sleep(2)

        # Fetch all the match information from cricinfo
        data = BeautifulSoup(r.text).find_all("description")
        if not match:
            print("Matches available:")
            for counter, game in enumerate(data[1:], 1):
                print(counter, game.text)
            match = int(input("Enter your choice: "))
            interrupted = False

        newscore = data[match].text
        if newscore != score:
            score = newscore
            sendmessage("Score", score)

        # Be a good citizen and wait 15 seconds before getting the next score update
        sleep(15)

    except KeyboardInterrupt:
        if interrupted:
            print("Bye bye")
            break
        else:
            print("Press Ctrl+C again to quit")
            match, interrupted = 0, True
