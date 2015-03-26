from __future__ import print_function
from sys import version_info
import requests
from bs4 import BeautifulSoup
if version_info.major is 2:
    import pynotify
    notifyModule = "pynotify"
if version_info.major is 3:
    try:
        from gi.Repository import Notify
        notifyModule = "Notify"
    except ImportError:
        import notify2
        notifyModule = "notify2"
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG)

def popUpMessage(title, message):
    if notifyModule is "pynotify":
        logging.debug("Initializing pynotify")
        pynotify.init("Scorer")
        logging.debug("Sending notification: title:{}, message:{}".format(title,message))
        pynotify.Notification(title, message, "dialog-information").show()
    elif notifyModule is "Notify":
        logging.debug("Initializing Notify")
        Notify.init("Scorer")
        logging.debug("Sending notification: title:{}, message:{}".format(title,message))
        Notify.Notification.new(title, message, "dialog-information").show()
    else:
        logging.debug("Initializing notify2")
        notify2.init("Scorer")
        logging.debug("Sending notification: title:{}, message:{}".format(title,message))
        notify2.Notification(title, message, "dialog-information").show()



liveUrl = "http://static.cricinfo.com/rss/livescores.xml"
matchChoice = 0
score = ""
didInterrupt = False
proxies = {
  "http": "http://username:password@proxy.host:port",
}


print("Fetching matches..")
while True:
    try:
        logging.info("Sending requests")
        dataFromUrl = requests.get(liveUrl)
        while dataFromUrl.status_code is not 200:
            logging.debug("Request failed: trying again")
            sleep(2)
            if dataFromUrl.status_code == 407:
                dataFromUrl = requests.get(liveUrl, proxies=proxies)
            else:    
                dataFromUrl = requests.get(liveUrl)
        data = BeautifulSoup(dataFromUrl.text).find_all("description")
        if not matchChoice:
            print("Matches available:")
            for index, game in enumerate(data[1:], 1):
                print(index, ".", str(game.text))
            matchChoice = int(input("Enter your choice: "))
            while True:
                if matchChoice in range(1, index):
                    break
                matchChoice = int(input("Invalid Choice. Enter your choice: "))
            didInterrupt=False
        newscore = data[matchChoice].text
        logging.info("Score found is {}".format(newscore))
        if newscore != score:
            logging.info("This is the most recent score, send me a notification")
            score = newscore
            popUpMessage("Score", score)
        sleep(15)

    except KeyboardInterrupt:
        if didInterrupt:
            logging.info("keyboard interrupted, once")
            print("Bye bye")
            break
        else:
            print("Press Ctrl+C again to quit")
            matchChoice, didInterrupt = 0, True

