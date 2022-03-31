import numpy as np 
from matplotlib import pyplot as plt 

import logging
from fantasy_logger import Fantasy_Logger

logging.setLoggerClass(Fantasy_Logger)
logger = logging.getLogger(__name__)

def create_score_graph(team_id, team_scores, team_id_map):
    focused_team_name = team_id_map[team_id]

    week_arr = np.array([int(week["week"]) for week in team_scores])
    actual_score_arr = np.array([float(week["actual_points"]) for week in team_scores])
    did_win_colors_arr = np.array([get_win_color(week["did_win"]) for week in team_scores])
    opponent_team_name_arr = np.array([team_id_map[int(week["opponent_id"])]["team_name"] for week in team_scores])
    
    plt.title("Score Graph") 
    plt.xlabel("Week") 
    plt.ylabel("Score") 
    
    plt.xticks(week_arr)
    plt.scatter(week_arr,actual_score_arr, c=did_win_colors_arr, s=50) 

    for x,y,z in zip(week_arr, actual_score_arr, opponent_team_name_arr):
        label = "v.s. {}".format(z)

        plt.annotate(label, # this is the text
                    (x,y), # these are the coordinates to position the label
                    textcoords="offset points", # how to position the text
                    xytext=(0,7), # distance from text to points (x,y)
                    ha='center',
                    fontsize=8) # horizontal alignment can be left, right or center
    # fig, ax = plt.subplot()
    # legend = ax.legend(*scatter.legend_elements(),
    #                     loc="lower left", title="Classes")
    # plt.legend(legend)
    plt.grid(True)
    plt.show()

def get_win_color(did_win):
    return 'g' if did_win else 'r'