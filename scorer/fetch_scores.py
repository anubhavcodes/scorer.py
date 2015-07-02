import requests
from bs4 import BeautifulSoup
import re
import json
import logging
from scorer.customlog import log

@log()
def getJsonURL(matchId):
    jsonurl = "http://www.espncricinfo.com/ci/engine/match/" + matchId + ".json"
    return jsonurl

@log()
def getLastestScore(scoreParser):
    scoreParser.refresh()
    matchStatus = scoreParser.getMatchStatus()
    titleToDisplay = matchStatus
    scoreToDisplay = ""
    #Check if match Started
    if scoreParser.isMatchNotStarted() :
        return (titleToDisplay,scoreToDisplay)
    #Check if match over
    if scoreParser.isMatchOver():
        return (titleToDisplay,scoreToDisplay)
    battingTeamName = scoreParser.getBattingTeamName()
    bowlingTeamName = scoreParser.getBowlingTeamName()
    overs = scoreParser.getOvers()
    runs = scoreParser.getRuns()
    wickets = scoreParser.getWickets()
    requiredRuns = scoreParser.getRequiredRuns()
    titleToDisplay = battingTeamName + " vs " + bowlingTeamName
    scoreToDisplay = "score: " + runs + "/" + wickets + "\n" + "overs: " + overs + "\n" + requiredRuns
    return (titleToDisplay,scoreToDisplay)

@log()
def getMatchID(matchChoice, xml):
    guid = xml[matchChoice].guid.text
    matchId = re.search(r'\d+',guid).group()
    return matchId

def findMatchesAvailable():
    url="http://static.cricinfo.com/rss/livescores.xml"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    xml = soup.find_all("item")
    matches = map( lambda item : re.sub(r'\s+'," ",re.sub('[^A-Za-z ]+', '', item.title.text)), xml)
    return (xml, matches)
