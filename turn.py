# -*- coding: utf-8 -*-
from user_input import *
from settings import *
from draw import *                  

def bot_turn(PLAYER, player, wall_list, available_positions, players):
    bot_type = PLAYER['owner']
    target_loc = PLAYER['target_loc']
    #print target_loc
    if bot_type == 'bot':
        pass
    elif bot_type == 'straight_bot':
        loc = player['location']
        neighbor = loc
        #breadth-first search
        queue = []
        queue.append(loc)   
        visited = []
        visited.append(loc)
        is_break = False
        path = {}
        while (queue != []) and not is_break:
            node = queue[0]
            for neighbor in available_positions[node]:
                if neighbor not in visited and not is_break:
                    path.update({neighbor: node})
                    visited.append(neighbor)
                    if neighbor in target_loc:
                        is_break = True
                        #print neighbor
                    queue.append(neighbor)
                if is_break: 
                    break    
            queue.remove(node)

        node = neighbor
        while node != loc:
            neighbor = node
            node = path[neighbor]

        (x, y) = neighbor
        players[x][y] = 0    
        player['location'] = (x, y)
        players[x][y] = 1
    else:
        pass
