from algorithms import *

def turn(player, players, available_positions):
    loc = player['location']
    target_loc = player['target_loc']
    [step, neighbor] = bfs(loc, available_positions, target_loc)
    #print step
    (x, y) = neighbor
    players[x][y] = 0    
    player['location'] = (x, y)
    players[x][y] = 1
