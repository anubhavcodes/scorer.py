from __future__ import print_function
from scorer.system import exitApp
import scorer.fetch_scores as fs
import scorer.notification as notify
import logging
from time import sleep


logging.basicConfig(level=logging.DEBUG)
NO_LIVE_MATCHES = "No Match in progress"
SLEEP_INTERVAL = 15 

def main():
    while True:
        logging.debug("Getting the xml and matches list")
        xml, matches = fs.findMatchesAvailable()
        if(matches[0]==NO_LIVE_MATCHES):
            print("No Live matches are available now:")
            exitApp()
        print("The following matches are available now:")
        for index,game in enumerate(matches, 1):
            print (index, ".", game)
        print (index+1, ". Quit ")
        try:
            matchChoice = str(input("Enter your choice: ")).strip()
        except KeyboardInterrupt:
                exitApp()   
        while True:
            if (matchChoice.isdigit()):
                matchChoice = int(matchChoice)
                if (matchChoice==index+1):
                    logging.info("User selected Quit")
                    exitApp()
                if matchChoice in range(1, index+1):
                    break
            logging.debug("User's choice was invalid")
            try:
                matchChoice = raw_input("Enter your choice: ").strip()
            except KeyboardInterrupt:
                exitApp()  
        #logging moved down after validation since matches[matchChoice-1] could lead to exception 
        #for unvalidated match choices.
        logging.info("User's choice: {} {}".format(matchChoice, matches[matchChoice-1]))
        logging.info("Getting the latest score for the selected match")
        matchID = fs.getMatchID(matchChoice-1, xml)
        jsonurl = fs.getJsonURL(matchID)
        playingTeams = fs.getPlayingTeamNames(jsonurl)
        while True:
            try:
                title,score = fs.getLastestScore(jsonurl,playingTeams)
                logging.debug("Sending notification for: title:{} score:{}".format(title, score))
                notify.popUpMessage(title, score)
                sleep(SLEEP_INTERVAL)
            except KeyboardInterrupt:
                break

if __name__ == '__main__':
    main()
