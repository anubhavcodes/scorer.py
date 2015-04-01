import requests
from bs4 import BeautifulSoup
import re
import json
import logging

def getJsonURL(matchId):
    logging.debug("Entry Point for getJsonURL")
    jsonurl = "http://www.espncricinfo.com/ci/engine/match/" + matchId + ".json"
    logging.debug("Url to get the latest json is: {}".format(jsonurl))
    return jsonurl

def getPlayingTeamNames(jsonurl):
    #Get the playing team names and store it in teamId:teamName dict format
    r = requests.get(jsonurl)
    jsonData = r.json()
    playingTeams={ team.get("team_id"):team.get("team_name") for team in jsonData.get("team") }
    return playingTeams

def getLastestScore(jsonurl,playingTeams):
    logging.debug("Entry Point for getLastestScore")
    logging.debug("Url to get the latest json is: {}".format(jsonurl))
    r = requests.get(jsonurl)
    jsonData = r.json()
    innings = jsonData.get("live").get("innings")
    batting_team_id=innings.get("batting_team_id")
    battingTeamName = playingTeams[batting_team_id]
    bowling_team_id=innings.get("bowling_team_id")
    bowlingTeamName = playingTeams.get(bowling_team_id)
    overs = innings.get("overs")
    logging.info("Found Overs: {}".format(overs))
    runs=innings.get("runs")
    logging.info("Found Runs: {}".format(runs))
    wickets = innings.get("wickets")
    logging.info("Found wickets: {}".format(wickets))
    titleToDisplay = battingTeamName + " vs " + bowlingTeamName
    scoreToDisplay = "score: " + runs + "/" + wickets + "\n" + "overs: " + overs 
    logging.debug("The display string is: {} {} ".format(titleToDisplay,scoreToDisplay))
    return (titleToDisplay,scoreToDisplay)

def getMatchID(matchChoice, xml):
    logging.debug("Entry point for getMatchID")
    guid = xml[matchChoice].guid.text
    logging.debug("strriped url from xml: {}".format(guid))
    matchId = re.search(r'\d+',guid).group()
    logging.info("Found matchId: {}".format(matchId))
    return matchId

def findMatchesAvailable(url="http://static.cricinfo.com/rss/livescores.xml"):
    logging.debug("Entry point for findMatchesAvailable")
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    xml = soup.find_all("item")
    matches = map( lambda item : re.sub(r'\s+'," ",re.sub('[^A-Za-z ]+', '', item.title.text)), xml)
    return (xml, matches)
