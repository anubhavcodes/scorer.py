import logging
import re

import requests
from bs4 import BeautifulSoup
from scorer.system import exitApp

logger = logging.getLogger('scorer.fetch_scores')

WON_STATUS = "won by"


def getJsonURL(matchId):
    """
    Return the json url for the particular match.
    :param matchId: The uid of the match.
    :type matchId: `str`.
    :return: The url of the particular match.
    """
    logger.info("Entry Point for getJsonURL")
    jsonurl = "http://www.espncricinfo.com/ci/engine/match/" + matchId + ".json"
    logger.debug("Url to get the latest json is: {}".format(jsonurl))
    return jsonurl


def getPlayingTeamNames(jsonurl):
    """
    Get the names of the teams playing the matches.
    :param jsonurl: url for the json.
    :type jsonurl: `str`
    :return: teams playing
    """
    logger.info("Url to get the json from {}".format(jsonurl))
    try:
        r = requests.get(jsonurl)
    except:
        logger.error("not able to reach the site to get the match info!!")
        exitApp()

    jsonData = r.json()
    playingTeams = {team.get("team_id"): team.get("team_name") for team in jsonData.get("team")}
    logger.debug("playingTeams: {}".format(playingTeams))
    return playingTeams


def getLastestScore(jsonurl, playingTeams):
    logger.info("Entry Point for getLastestScore")
    logger.debug("Url to get the latest json is: {}".format(jsonurl))
    try:
        r = requests.get(jsonurl)
    except:
        logger.error("not able to reach the site to get the match info!!")
        exitApp()

    jsonData = r.json()
    matchStatus = jsonData.get("live").get("status")
    logger.info("matchStatus: {}".format(matchStatus))
    titleToDisplay = matchStatus
    scoreToDisplay = ""
    # Check if match Started
    if (not jsonData.get("live").get("innings")):
        logger.info("Match not started")
        return (titleToDisplay, scoreToDisplay)

    # Check if match over
    if (WON_STATUS in matchStatus):
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
    """
    Get the id of the match.
    :param matchChoice: the choice of the match
    :type matchChoice: `int`.
    :param xml: xml data.
    :type xml: `str`.
    :return: the match id of the match
    """
    logger.info("Entry point for getMatchID")
    guid = xml[matchChoice].guid.text
    logger.debug("striped url from xml: {}".format(guid))
    matchId = re.search(r'\d+', guid).group()
    logger.debug("Found matchId: {}".format(matchId))
    return matchId


def findMatchesAvailable(url="http://static.cricinfo.com/rss/livescores.xml"):
    """
    Find all the matches available for the day.
    :param url: url for the matches for the day.
    :param url: `str`
    :return: a tuple of xml and matches.
    """
    logger.info("Entry point for findMatchesAvailable")
    try:
        r = requests.get(url)
    except:
        logger.error("not able to reach the site to get the match info!!")
        exitApp()

    soup = BeautifulSoup(r.text)
    xml = soup.find_all("item")
    matches = map(lambda item: re.sub(r'\s+', " ", re.sub('\
        [^A-Za-z ]+', '', item.title.text)), xml)
    return (xml, matches)
