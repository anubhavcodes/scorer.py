from time import sleep
import scorer.logger as logger
import scorer.fetch_scores as fs
import scorer.notification as notify
from scorer.system import exitApp
from scorer.ui import getUserInput
from scorer import config_reader

logger = logger.get_logger('cricket-scores-api')

NO_LIVE_MATCHES = config_reader.NO_LIVE_MATCHES
SLEEP_INTERVAL = config_reader.SLEEP_INTERVAL


def main():
    while True:
        logger.debug("Getting the xml and matches list")
        xml, matches = fs.findMatchesAvailable()
        if matches[0] == NO_LIVE_MATCHES:
            print "No Live matches are available now:"
            exitApp()
        matches.append("Quit the scorer app")
        try:
            matchChoice = getUserInput(matches)
        except KeyboardInterrupt:
            exitApp()
        if matchChoice == len(matches) - 1:
            logger.debug("User chose quit")
            exitApp()
        logger.debug("User's choice: {} {}".format(matchChoice,
                                                   matches[matchChoice - 1]))
        logger.debug("Getting the latest score for the selected match")
        matchID = fs.getMatchID(matchChoice, xml)
        jsonurl = fs.getJsonURL(matchID)
        playingTeams = fs.getPlayingTeamNames(jsonurl)
        while True:
            try:
                title, score = fs.getLastestScore(jsonurl, playingTeams)
                logger.debug("Sending notification for: title:{} score:\
                    {}".format(title, score))
                notify.popUpMessage(title, score)
                sleep(SLEEP_INTERVAL)
            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    main()
