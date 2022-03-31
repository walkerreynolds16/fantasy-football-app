import json

from pathlib import Path
from yahoo_api import Yahoo_Api
import graph_utils

import logging
from fantasy_logger import Fantasy_Logger

logging.setLoggerClass(Fantasy_Logger)
logger = logging.getLogger(__name__)

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# logger.removeHandler(logger.handlers[0])
# logger.addHandler(stream_handler)


league_id = "838233"


api = Yahoo_Api("credentials.json")


def save_response(function_name, res):
    with open("example_responses/{}.json".format(function_name), "w") as outfile:
        json.dump(res, outfile, ensure_ascii=False)

team_id_map = api.get_team_id_to_manager_map(league_id)

team_id = 5
graph_utils.create_score_graph(team_id, api.get_team_scores(league_id, team_id), team_id_map)

# res = api.get_league_info(league_id)
# save_response("get_league_info", res)

# res = api.get_league_standings(league_id)
# save_response("get_league_standings", res)

# res = api.get_team_info(league_id, 1)
# save_response("get_team_info", res)

# res = api.get_team_matchups(league_id, 2)
# save_response("get_team_matchups", res)

# res = api.get_all_matchups(league_id)
# save_response("get_all_matchups", res)

# res = api.get_team_scores(league_id, 2)
# save_response("get_team_scores", res)

# res = api.get_team_id_to_manager_map(league_id)
# save_response("get_team_id_to_manager_map", res)


# team_id_map = api.get_team_id_to_manager_map(league_id)
# print(team_id_map)

# print(api.get_league_info(league_id))
# print(api.get_league_info(league_id))

# print(api.get_league_standings(league_id))
# print(api.get_league_standings(league_id))

# api.get_team_info(league_id, 1)
# api.get_team_info(league_id, 2)
# print(api.get_team_info(league_id, 1))
# print(api.get_team_info(league_id, 2))
# print(api.get_team_id_to_manager_map(league_id))

