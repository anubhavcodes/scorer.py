import requests
from bs4 import BeautifulSoup
import re
import json
import logging

def getLastestScore(matchId):
    logging.debug("Entry Point for getLastestScore")
    url = "http://www.espncricinfo.com/ci/engine/match/" + matchId + ".json"
    logging.debug("Url to get the latest json is: {}".format(url))
    r = requests.get(url)
    jsonData = json.loads(r.text)
    overs = jsonData['comms'][0]['over_number']
    logging.info("Found Overs: {}".format(overs))
    runs = jsonData['comms'][1]['runs']
    logging.info("Found Runs: {}".format(runs))
    wickets = jsonData['comms'][0]['wickets']
    logging.info("Found wickets: {}".format(wickets))

    toDisplay = "score: " + runs + "/" + wickets + "\n" + "overs: " + overs 
    logging.debug("The display string is: {}".format(toDisplay))
    return toDisplay

def getMatchID(matchId, xml):
    logging.debug("Entry point for getMatchID")
    url = xml[matchId].guid.text
    logging.debug("strriped url from xml: {}".format(url))
    isDigit = re.search("\d", url)
    matchId = url[isDigit.start():url.find(".html")]
    logging.info("Found matchId: {}".format(matchId))
    return matchId

def findMatchesAvailable(url="http://static.cricinfo.com/rss/livescores.xml"):
    logging.debug("Entry point for findMatchesAvailable")
    matches = list()
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    xml = soup.find_all("item")
    for i in range(0, len(xml)):
        matches.append(xml[i].title.text)
    return (xml, matches)
