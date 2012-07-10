# -*- coding: utf-8 -*-
from user_input import *
from bots import *

def bot_turn(PLAYER, player, player_list, wall_list, available_positions, 
             players, adjacency_list):
    bot_type = player['owner']
    if bot_type == 'bot':
        pass
    elif bot_type == 'straight_bot':
        straight_bot.turn(player, players, available_positions)
    elif bot_type == 'simple_bot':
        simple_bot.turn(player, players, player_list, wall_list, available_positions, adjacency_list)
    elif bot_type == 'complicated_bot':
        complicated_bot.turn(player, players, player_list, wall_list, available_positions, adjacency_list)
    elif bot_type == 'optimized_bot':
        optimized_bot.turn(player, players, player_list, wall_list, available_positions, adjacency_list)
    elif bot_type == 'gamesome_bot':
        gamesome_bot.turn(player, players, player_list, wall_list, available_positions, adjacency_list)
    elif bot_type == 'playful_bot':
        playful_bot.turn(player, players, player_list, wall_list, available_positions, adjacency_list)
    elif bot_type == 'medium_bot':
        medium_bot.turn(player, players, player_list, wall_list, available_positions, adjacency_list)
    else:
        pass
