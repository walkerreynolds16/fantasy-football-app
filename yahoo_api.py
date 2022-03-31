import json
from yahoo_oauth import OAuth2
import xmltodict

import logging
from fantasy_logger import Fantasy_Logger

logging.setLoggerClass(Fantasy_Logger)
logger = logging.getLogger(__name__)
logging.getLogger('yahoo_oauth').setLevel(logging.INFO)

class Yahoo_Api():
    def __init__(self, credentials_file):
        self.oauth = OAuth2(None, None, from_file=credentials_file)
        self.validate_oauth()
        self.league_info = None
        self.league_standings = None
        self.team_info_map = {}
        self.team_matchup_map = {}

    def validate_oauth(self):
        if not self.oauth.token_is_valid():
            self.oauth.refresh_access_token()

    def get_league_info(self, league_id):
        if not self.league_info:
            logger.info("Did not have league info, retrieving info...")

            self.validate_oauth()
            url = "https://fantasysports.yahooapis.com/fantasy/v2/league/nfl.l.{}".format(league_id)
            response = xmltodict.parse(self.oauth.session.get(url, params={'format': 'xml'}).content)
            self.league_info = response

        return self.league_info

    def get_league_standings(self, league_id):
        if not self.league_standings:
            logger.info("Did not have league standings, retrieving info...")

            self.validate_oauth()
            url = "https://fantasysports.yahooapis.com/fantasy/v2/league/nfl.l.{}/standings".format(league_id)
            response = xmltodict.parse(self.oauth.session.get(url, params={'format': 'xml'}).content)
            self.league_standings = response

        return self.league_standings

    def get_team_info(self, league_id, team_id):
        try:
            return self.team_info_map[team_id]
        except KeyError as e:
            logger.info("Did not have team info for team_id={}, retrieving info...".format(team_id))

            self.validate_oauth()
            url = "https://fantasysports.yahooapis.com/fantasy/v2/team/nfl.l.{}.t.{}".format(league_id, team_id)
            response = xmltodict.parse(self.oauth.session.get(url, params={'format': 'xml'}).content)

            self.team_info_map[team_id] = response
            return self.team_info_map[team_id]
      
    def get_num_of_teams_in_league(self, league_id):
        league_info = self.get_league_info(league_id)
        try:
            return int(league_info["fantasy_content"]["league"]["num_teams"])
        except Exception as e:
            raise Exception("Could not retrieve num of teams")
    
    def get_current_week_of_league(self, league_id):
        league_info = self.get_league_info(league_id)
        try:
            return int(league_info['fantasy_content']['league']['current_week'])
        except Exception as e:
            raise Exception("Could not retrieve current week")

    def get_team_matchups(self, league_id, team_id):
        try:
            return self.team_matchup_map[team_id]
        except KeyError as e:
            logger.info("Did not have team matchups for team_id={}, retrieving info...".format(team_id))

            current_week = self.get_current_week_of_league(league_id)
            weeks_string = ""
            for i in range(1, current_week + 1):
                weeks_string += "{},".format(i)

            self.validate_oauth()
            url = "https://fantasysports.yahooapis.com/fantasy/v2/team/nfl.l.{}.t.{}/matchups;weeks={}".format(league_id, team_id, weeks_string)
            response = xmltodict.parse(self.oauth.session.get(url, params={'format': 'xml'}).content)

            self.team_matchup_map[team_id] = response
            return self.team_matchup_map[team_id]

    def get_team_id_to_manager_map(self, league_id):
        num_teams = self.get_num_of_teams_in_league(league_id)
        team_map = {}

        for team_id in range(1, num_teams + 1):
            res = self.get_team_info(league_id, team_id)
            manager_name = res["fantasy_content"]["team"]["managers"]["manager"]["nickname"]
            team_name = res["fantasy_content"]["team"]["name"]
            team_map[team_id] = {"manager_name": manager_name, "team_name": team_name}

        return team_map

    def get_all_matchups(self, league_id):
        num_teams = self.get_num_of_teams_in_league(league_id)
        
        for team_id in range(1, num_teams + 1):
            self.get_team_matchups(league_id, team_id)
        
        return self.team_matchup_map

    def get_team_scores(self, league_id, team_id):
        team_matchups = self.get_team_matchups(league_id, team_id)
        scores = []
        for matchup in team_matchups['fantasy_content']['team']['matchups']['matchup']:
            winner_team_id = -1
            if "winner_team_key" in matchup:
                winner_team_id = int(str(matchup["winner_team_key"]).split('.')[-1])
            
            opponent_id = [t for t in matchup['teams']['team'] if int(t['team_id']) != team_id][0]["team_id"]
            team_obj = [t for t in matchup['teams']['team'] if int(t['team_id']) == team_id][0]
            week_score = {"week": matchup['week'], "did_win": team_id == winner_team_id, "opponent_id": opponent_id}
            
            week_score["actual_points"] = team_obj["team_points"]["total"]
            week_score["projected_points"] = team_obj["team_projected_points"]["total"]

            scores.append(week_score)

        return scores