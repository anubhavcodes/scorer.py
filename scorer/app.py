from scorer.system import exitApp
import scorer.fetch_scores as fs
import scorer.notification as notify
from scorer.ui import getUserInput
from scorer.scoreparser import ScoreParser
import logging
from sys import version_info
from time import sleep

logger = logging.getLogger("scorer")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("scorer.log")
fh.setLevel(logging.CRITICAL)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

NO_LIVE_MATCHES = "No Match in progress"
SLEEP_INTERVAL = 60 

def main():
    while True:
        logger.debug("Getting the xml and matches list")
        xml, matches = fs.findMatchesAvailable()
        if(matches[0]==NO_LIVE_MATCHES):
            print "No Live matches are available now:"
            logger.critical('No live matches are available')
            exitApp()
        matches.append("Quit the scorer app")
        try:
            matchChoice= getUserInput(matches)
        except KeyboardInterrupt:
            exitApp()
        if(matchChoice == len(matches) -1 ):
            logger.debug("User chose quit")
            exitApp()
        logger.debug("User's choice: {} {}".format(matchChoice, matches[matchChoice-1]))
        logger.debug("Getting the latest score for the selected match")
        matchID = fs.getMatchID(matchChoice,xml)
        jsonurl = fs.getJsonURL(matchID)
        scoreParser = ScoreParser(jsonurl)
        while True:
            try:
                title,score = fs.getLastestScore(scoreParser)
                logger.debug("Sending notification for: title:{} score:{}".format(title, score))
                notify.popUpMessage(title, score)
                sleep(SLEEP_INTERVAL)
            except KeyboardInterrupt:
                logger.critical('Keyboard interrupted by user')
                break

if __name__ == '__main__':
    main()
