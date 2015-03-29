from __future__ import print_function
import fetch_scores as fs
import notification as notify
import logging
from time import sleep

matchChoice = 0
didInterrupt = False

logging.basicConfig(level=logging.DEBUG)

while True:
    try:
        logging.debug("Getting the xml and matches list")
        xmlAndMatches = fs.findMatchesAvailable()
        matches = xmlAndMatches[1]
        xml = xmlAndMatches[0]
        print("The following matches are available now:")
        for index,game in enumerate(matches, 1):
            print (index, ".", game)
        matchChoice = int(input("Enter your choice: "))
        logging.info("User's choice: {} {}".format(matchChoice, matches[matchChoice-1]))
        while True:
            logging.debug("User's choice was invalid")
            if matchChoice in range(1, index+1):
                break
            matchChoice = int(input("Invalid Choid. Enter your choice: "))
        didInterrupt = False
        notify.popUpMessage("Score", matches[matchChoice-1])
        # logging.info("Getting the latest score for the selected match")
        # score = fs.getLastestScore(fs.getMatchID(int(matchChoice-1), xml))
        # logging.debug("Sending notification for: title:{} score:{}".format(matches[matchChoice-1], score))
        # notify.popUpMessage(matches[matchChoice-1], score)
        sleep(15)
    except KeyboardInterrupt:
        if didInterrupt:
            print ("Thank you for using the scorer app")
            break
        else:
            print ("Press Ctrl+D again to quit")
            matchChoice, didInterrupt = 0, True
