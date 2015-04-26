import requests
from bs4 import BeautifulSoup
import re
import json
import logging

logger = logging.getLogger('scorer.fetch_scores')

def getJsonURL(matchId):
    logger.info("Entry Point for getJsonURL")
    jsonurl = "http://www.espncricinfo.com/ci/engine/match/" + matchId + ".json"
    logger.debug("Url to get the latest json is: {}".format(jsonurl))
    return jsonurl

def getLastestScore(scoreParser):
    logger.info("Entry Point for getLastestScore")
    scoreParser.refresh()
    matchStatus = scoreParser.getMatchStatus()
    logger.info("matchStatus: {}".format(matchStatus))
    titleToDisplay = matchStatus
    scoreToDisplay = ""
    #Check if match Started
    if scoreParser.isMatchNotStarted() :
        logger.info("Match not started")
        return (titleToDisplay,scoreToDisplay)
    #Check if match over
    if scoreParser.isMatchOver():
        logger.info("Match over")
        return (titleToDisplay,scoreToDisplay)
    battingTeamName = scoreParser.getBattingTeamName()
    bowlingTeamName = scoreParser.getBowlingTeamName()
    overs = scoreParser.getOvers()
    logger.debug("Found Overs: {}".format(overs))
    runs = scoreParser.getRuns()
    logger.debug("Found Runs: {}".format(runs))
    wickets = scoreParser.getWickets()
    logger.debug("Found wickets: {}".format(wickets))
    requiredRuns = scoreParser.getRequiredRuns()
    logger.debug("The requiredRuns string is: {}".format(requiredRuns))
    titleToDisplay = battingTeamName + " vs " + bowlingTeamName
    scoreToDisplay = "score: " + runs + "/" + wickets + "\n" + "overs: " + overs + "\n" + requiredRuns
    logger.debug("The display string is: {} {} ".format(titleToDisplay,scoreToDisplay))
    return (titleToDisplay,scoreToDisplay)

def getMatchID(matchChoice, xml):
    logger.info("Entry point for getMatchID")
    guid = xml[matchChoice].guid.text
    logger.debug("strriped url from xml: {}".format(guid))
    matchId = re.search(r'\d+',guid).group()
    logger.debug("Found matchId: {}".format(matchId))
    return matchId

def findMatchesAvailable(url="http://static.cricinfo.com/rss/livescores.xml"):
    logger.info("Entry point for findMatchesAvailable")
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    xml = soup.find_all("item")
    matches = map( lambda item : re.sub(r'\s+'," ",re.sub('[^A-Za-z ]+', '', item.title.text)), xml)
    return (xml, matches)
