# -*- coding: utf-8 -*-
from user_input import *
from settings import *
from draw import *   

def adjacency_list_generator():
    #adjacency_list
    adjacency_list = {}
    for i in range(width):
        for j in range(height):
            link_list = set([])
            for direction in DIRECTIONS:
                (dx, dy) = DIRECTIONS[direction]
                if ((dy + j) >= 0) & ((dy + j) < height) &\
                   ((dx + i) >= 0) & ((dx + i) < width): 
                    link_list.add((dx + i, dy + j))
            adjacency_list.update({(i, j): link_list})    

    return adjacency_list

def available_positions_generator(loc, wall_list, player_list):
    adjacency_list = adjacency_list_generator()   
    #calculate available positions
    available_positions = {}
    for positions in adjacency_list:
        #print positions
        available_positions.update({positions: adjacency_list[positions].copy()})
    #available_positions = adjacency_list.copy()
    #print available_positions

    for wall in wall_list:
        (col, row) = wall['location']
        left_top = (col - 1, row - 1)  
        right_top = (col, row - 1) 
        left_bottom = (col - 1, row) 
        right_bottom = (col, row) 

        #print left_top, right_top,left_bottom, right_bottom
        if (wall['type'] == 'horizontal'):
            available_positions[left_top].difference_update(set([left_bottom]))
            available_positions[left_bottom].difference_update(set([left_top])) 
            available_positions[right_top].difference_update(set([right_bottom]))    
            available_positions[right_bottom].difference_update(set([right_top]))         
        elif (wall['type'] == 'vertical'):        
            available_positions[left_top].difference_update(set([right_top]))
            available_positions[left_bottom].difference_update(set([right_bottom])) 
            available_positions[right_top].difference_update(set([left_top]))    
            available_positions[right_bottom].difference_update(set([left_bottom]))

    #occupied cells
    (col, row) = loc        
    #print available_positions[loc]

    player_locations = []
    for player in player_list:
        player_locations.append(player['location'])

    for direction in DIRECTIONS:
        (dx, dy) = DIRECTIONS[direction]                    
        for a_loc in player_locations:
            if (a_loc == (col + dx, row + dy)) and\
               (a_loc in available_positions[loc]):
                #print a_loc
                (a_col, a_row) = a_loc
                for neighbors in available_positions[a_loc]:
                    available_positions[neighbors].difference_update(set([a_loc]))
                
                b_loc = (a_col + dx, a_row + dy) 
                if (b_loc in available_positions[a_loc]) and\
                   (b_loc not in player_locations):                            
                    available_positions[b_loc].update(set([loc]))
                    available_positions[loc].update(set([b_loc]))
                else:
                    #sideway jump
                    (ldx, ldy) = DIRECTIONS[LEFT[direction]]
                    c_loc = (a_col + ldx, a_row + ldy)
                    if (c_loc in available_positions[a_loc]) and\
                       (c_loc not in player_locations):
                        available_positions[c_loc].update(set([loc]))
                        available_positions[loc].update(set([c_loc]))
                    (rdx, rdy) = DIRECTIONS[RIGHT[direction]]
                    d_loc = (a_col + rdx, a_row + rdy)
                    if (d_loc in available_positions[a_loc]) and\
                       (d_loc not in player_locations):
                        available_positions[d_loc].update(set([loc]))
                        available_positions[loc].update(set([d_loc]))        
                available_positions.update({a_loc: set([])})
    #print available_positions[loc]    
    return available_positions 

def bfs(loc, available_positions, target_loc):
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
    step = 0
    while node != loc:
        step += 1
        neighbor = node
        node = path[neighbor]

    return step, neighbor 

def minimax(wall_list, player_list):
    pass

def bot_turn(PLAYER, player, wall_list, available_positions, players):
    bot_type = PLAYER['owner']
    target_loc = PLAYER['target_loc']
    #print target_loc
    if bot_type == 'bot':
        pass
    elif bot_type == 'straight_bot':
        loc = player['location']
        [step, neighbor] = bfs(loc, available_positions, target_loc)
        print step
        (x, y) = neighbor
        players[x][y] = 0    
        player['location'] = (x, y)
        players[x][y] = 1
    else:
        pass
