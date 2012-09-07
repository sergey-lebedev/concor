# -*- coding: utf-8 -*-
from user_input import *
from bots import *

def bot_turn(PLAYER, player, player_list, wall_list, available_positions, 
             players, adjacency_list):
    bot_type = player['owner']
    turn_call = '.turn(player, players, player_list, wall_list, available_positions, adjacency_list)'
    try:
        eval(bot_type + turn_call)
    except:
        pass
