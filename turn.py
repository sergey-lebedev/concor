# -*- coding: utf-8 -*-
from user_input import *
from bots import *

def bot_turn(PLAYER, player, player_list, wall_list, available_positions,
             adjacency_list):
    bot_type = player['owner']
    turn_call = '.turn(player, player_list, wall_list, available_positions, adjacency_list)'
    eval(bot_type + turn_call)

