import requests
from bs4 import BeautifulSoup
import re
import json
import logging

logger = logging.getLogger('scorer.fetch_scores')

WON_STATUS = "won by"


def getJsonURL(matchId):
    logger.info("Entry Point for getJsonURL")
    jsonurl = "http://www.espncricinfo.com/ci/engine/match/\
    " + matchId + ".json"
    logger.debug("Url to get the latest json is: {}".format(jsonurl))
    return jsonurl


def getPlayingTeamNames(jsonurl):
    # Get the playing team names and store it in teamId:teamName dict format
    logger.info("Url to get the json from {}".format(jsonurl))
    r = requests.get(jsonurl)
    jsonData = r.json()
    playingTeams = {team.get("team_id"): team.get("team_name\
        ") for team in jsonData.get("team")}
    logging.debug("playingTeams: {}".format(playingTeams))
    return playingTeams


def getLastestScore(jsonurl, playingTeams):
    logger.info("Entry Point for getLastestScore")
    logger.debug("Url to get the latest json is: {}" . format(jsonurl))
    r = requests.get(jsonurl)
    jsonData = r.json()
    matchStatus = jsonData.get("live").get("status")
    logger.info("matchStatus: {}".format(matchStatus))
    titleToDisplay = matchStatus
    scoreToDisplay = ""
    # Check if match Started
    if(not jsonData.get("live").get("innings")):
        logger.info("Match not started")
        return (titleToDisplay, scoreToDisplay)

    # Check if match over
    if(WON_STATUS in matchStatus):
        logger.info("Match over")
        return (titleToDisplay, scoreToDisplay)
    innings = jsonData.get("live").get("innings")
    batting_team_id = innings.get("batting_team_id")
    battingTeamName = playingTeams[batting_team_id]
    bowling_team_id = innings.get("bowling_team_id")
    bowlingTeamName = playingTeams.get(bowling_team_id)
    overs = innings.get("overs")
    logger.debug("Found Overs: {}".format(overs))
    runs = innings.get("runs")
    logger.debug("Found Runs: {}".format(runs))
    wickets = innings.get("wickets")
    logger.debug("Found wickets: {}".format(wickets))
    try:
        requiredRuns = jsonData.get("comms")[1].get("required_string")
    except IndexError:
        requiredRuns = ""
    logger.debug("The requiredRuns string is: {}".format(requiredRuns))
    titleToDisplay = battingTeamName + " vs " + bowlingTeamName
    scoreToDisplay = "score: " + runs + "/" + wickets + "\n\
    " + "overs: " + overs + "\n" + requiredRuns
    logger.debug("The display string is: {} {} \
        ".format(titleToDisplay, scoreToDisplay))
    return (titleToDisplay, scoreToDisplay)


def getMatchID(matchChoice, xml):
    logger.info("Entry point for getMatchID")
    guid = xml[matchChoice].guid.text
    logger.debug("strriped url from xml: {}".format(guid))
    matchId = re.search(r'\d+', guid).group()
    logger.debug("Found matchId: {}".format(matchId))
    return matchId


def findMatchesAvailable(url="http://static.cricinfo.com/rss/livescores.xml"):
    logger.info("Entry point for findMatchesAvailable")
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    xml = soup.find_all("item")
    matches = map(lambda item: re.sub(r'\s+', " ", re.sub('\
        [^A-Za-z ]+', '', item.title.text)), xml)
    return (xml, matches)
