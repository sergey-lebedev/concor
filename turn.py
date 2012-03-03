# -*- coding: utf-8 -*-
from settings import *

def user_turn(player, wall_list, available_positions, players, walls):
    (x, y) = player['location']
    loc = (x, y)
    print available_positions[loc]
    for a_loc in available_positions[loc]:
        (a_col, a_row) = a_loc
        if (a_col - x) > 0:
            increment_x = a_col - x
        if (a_col - x) < 0:
            decrement_x = x - a_col
        if (a_row - y) > 0:
            increment_y = a_row - y
        if (a_row - y) < 0:
            decrement_y = y - a_row

    command = raw_input()
    #(X, Y) = wall_list[0]['location']        
    if (command == 'i'):
        if (x, y - decrement_y) in available_positions[loc]:
            players[x][y] = 0
            y -= decrement_y
            y = max(0, y)
            player['location'] = (x, y)
            players[x][y] = 1  
    elif (command == 'j'):
        if (x - decrement_x, y) in available_positions[loc]:
            players[x][y] = 0    
            x -= decrement_x
            x = max(0, x)
            player['location'] = (x, y)
            players[x][y] = 1 
    elif (command == 'k'):
        if (x, y + increment_y) in available_positions[loc]:
            players[x][y] = 0    
            y += increment_y
            y = min(height-1, y)
            player['location'] = (x, y)
            players[x][y] = 1 
    elif (command == 'l'):
        if (x + increment_x, y) in available_positions[loc]:
            players[x][y] = 0    
            x += increment_x
            x = min(width-1, x)
            player['location'] = (x, y)
            players[x][y] = 1
    elif (command == 'I'):
        pass
        #walls[X][Y] = 0    
        #Y -= 1
        #Y = max(1, Y)
        #if (wall_list[0]['type'] == 'vertical') & (Y <= 1):
        #    wall_list[0]['type'] = 'horizontal'
        #wall_list[0]['location'] = (X, Y)
        #walls[X][Y] = 1 
    elif (command == 'J'):
        pass
        #walls[X][Y] = 0    
        #X -= 1
        #X = max(1, X)
        #if (wall_list[0]['type'] == 'horizontal') & (X <= 1):
        #    wall_list[0]['type'] = 'vertical'
        #wall_list[0]['location'] = (X, Y)
        #walls[X][Y] = 1 
    elif (command == 'K'):
        pass
        #walls[X][Y] = 0    
        #Y += 1
        #Y = min(height - wall_length + 1, Y)
        #if (wall_list[0]['type'] == 'vertical') & (Y > height - wall_length):
        #    wall_list[0]['type'] = 'horizontal'
        #wall_list[0]['location'] = (X, Y)
        #walls[X][Y] = 1 
    elif (command == 'L'):
        pass
        #walls[X][Y] = 0    
        #X += 1
        #X = min(width - wall_length + 1, X)
        #if (wall_list[0]['type'] == 'horizontal') & (X > width - wall_length):
        #    wall_list[0]['type'] = 'vertical'
        #wall_list[0]['location'] = (X, Y)
        #walls[X][Y] = 1
    elif (command == 'R'):
        pass
        #if (wall_list[0]['type'] == 'horizontal'):
        #    wall_list[0]['type'] = 'vertical'   
        #elif (wall_list[0]['type'] == 'vertical'):
        #    wall_list[0]['type'] = 'horizontal'       
    elif (command == 'N'):
        pass
        #wall_list.insert(0, {'type': 'horizontal', 'location': (1, 1)})                
    elif (command == 'q'):
        end = True
    elif (command == 'q!'):
        end = True
        win = True
    else:
        pass

def bot_turn(PLAYER, player, wall_list, available_positions, players):
    bot_type = PLAYER['owner']
    target_loc = PLAYER['target_loc']
    #print target_loc
    if bot_type == 'bot':
        pass
    elif bot_type == 'straight_bot':
        loc = player['location']
        #neighbor = loc
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
