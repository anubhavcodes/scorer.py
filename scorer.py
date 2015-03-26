from __future__ import print_function
from sys import version_info
import requests
import json
import re
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

def getLastestScore(parsingJson):
    firstTeamName = parsingJson['other_scores']['international'][0]['team1_name'].strip()
    firstTeamScore = parsingJson['other_scores']['international'][0]['team1_desc'].replace('&nbsp;ov',' overs').strip()
    secondTeamName = parsingJson['other_scores']['international'][0]['team2_name'].strip()
    secondTeamScore = parsingJson['other_scores']['international'][0]['team2_desc'].replace('&nbsp;ov',' overs').strip()
    matchSummary = parsingJson['match']['current_summary'].strip()
        
    latestScore = str(firstTeamName) + ' - ' + str(firstTeamScore) +  '\n' + str(secondTeamName) + ' - ' + str(secondTeamScore)

    onCrease = re.sub(r'.*ov,','', str(matchSummary))

    toDisplay = latestScore + '\n'+ 'On the crease -> '+ onCrease

    logging.info("Score found is {}".format(toDisplay))
    return toDisplay
    



liveXMLUrl = "http://static.cricinfo.com/rss/livescores.xml"
liveJSONUrl = "http://www.espncricinfo.com/netstorage/656493.json"
matchChoice = 0
score = ""
didInterrupt = False


print("Fetching matches..")
while True:
    try:
        logging.info("Sending requests")
        dataFromXMLUrl = requests.get(liveXMLUrl)
        dataFromJSONUrl = requests.get(liveJSONUrl)
        while dataFromXMLUrl.status_code is not 200:
            logging.debug("Request failed: trying again")
            sleep(2)
            dataFromXMLUrl = requests.get(liveXMLUrl)

        data = BeautifulSoup(dataFromXMLUrl.text).find_all("description")
        parsingJson = json.loads(dataFromJSONUrl.text)
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
        updatedScore = getLastestScore(parsingJson)
        popUpMessage("Score", updatedScore)
        sleep(15)



    except KeyboardInterrupt:
        if didInterrupt:
            logging.info("keyboard interrupted, once")
            print("Bye bye")
            break
        else:
            print("Press Ctrl+C again to quit")
            matchChoice, didInterrupt = 0, True

