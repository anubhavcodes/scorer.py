import requests
class ScoreParser(object):
    def __init__(self,jsonurl):
        self._jsonurl = jsonurl
        self.refresh()
        self._getPlayingTeams()
    def refresh(self):
        r = requests.get(self._jsonurl)
        self._jsonData = r.json()
        self._live = self._jsonData.get("live")
        self._innings = self._live.get("innings")
    def getMatchStatus(self):
        return self._live.get("status")
    def getInnings(self):
        return self._innings
    def _getPlayingTeams(self):
        #Get the playing team names and store it in teamId:teamName dict format
        self._playingTeams={ team.get("team_id"):team.get("team_name") for team in self._jsonData.get("team") }
    def getBattingTeamName(self):
        batting_team_id=self._innings.get("batting_team_id")
        return self._playingTeams[batting_team_id]
    def getBowlingTeamName(self):
        bowling_team_id=self._innings.get("bowling_team_id")
        return self._playingTeams[bowling_team_id]
    def getOvers(self):
        return self._innings.get("overs")
    def getRuns(self):
        return self._innings.get("runs")
    def getWickets(self):
        return self._innings.get("wickets")
    def getRequiredRuns(self):
        try:
            requiredRuns = self._jsonData.get("comms")[1].get("required_string")
        except IndexError:
            requiredRuns = ""
        return requiredRuns
    def isMatchNotStarted(self):
        return not self._innings
    def isMatchOver(self):
        WON_STATUS = "won by"
        return WON_STATUS in self.getMatchStatus()