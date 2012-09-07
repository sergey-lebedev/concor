from algorithms import *

def turn(player, player_list, wall_list, available_positions, adjacency_list):
    loc = player['location']
    target_loc = player['target_loc']
    [step, backtrace] = bfs(loc, available_positions, target_loc)
    #print step
    neighbor = backtrace[1]
    (x, y) = neighbor
    player['location'] = (x, y)
