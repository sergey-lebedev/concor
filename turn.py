# -*- coding: utf-8 -*-
from user_input import *
from settings import *
from draw import *   
import random

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
    while (queue != []) and (not is_break):
        node = queue.pop(0)
        for neighbor in available_positions[node]:
            if (neighbor not in visited) and (not is_break):
                path.update({neighbor: node})
                visited.append(neighbor)
                if neighbor in target_loc:
                    is_break = True
                    #print neighbor
                queue.append(neighbor)
            if is_break: 
                break    
        #queue.remove(node)

    if not is_break:
        step = None  
    else:

        step = 0

    node = neighbor
    while (node != loc) and is_break:
        step += 1
        neighbor = node
        node = path[neighbor]      
  
    return step, neighbor 

def minimax(loc, wall_list, player_list):
    pass

def bot_turn(PLAYER, player, player_list, wall_list, available_positions, players):
    bot_type = player['owner']
    target_loc = player['target_loc']
    #print target_loc
    if bot_type == 'bot':
        pass
    elif bot_type == 'straight_bot':
        loc = player['location']
        [step, neighbor] = bfs(loc, available_positions, target_loc)
        #print step
        (x, y) = neighbor
        players[x][y] = 0    
        player['location'] = (x, y)
        players[x][y] = 1
    elif bot_type == 'simple_bot':
        loc = player['location']
        #opponent_list
        opponent_list = []
        for item in player_list:
            if item != player:
                opponent_list.append(item)
        #neigbors
        neighbors = []
        for location in available_positions[loc]:
            neighbors.append(location)
        #possibility matrix
        p = w2p(wall_list)
        #actions
        action_list = []
        #movement
        distances = []
        for opponent in opponent_list:
            #print opponent
            opponent_available_positions = available_positions_generator(opponent['location'], wall_list, player_list)
            [step, dummy] = bfs(opponent['location'], opponent_available_positions, opponent['target_loc'])
            #print step
            distances.append(step)
        distance = min(distances)
        #print distance
        for neighbor in neighbors:
            [step, dummy] = bfs(neighbor, available_positions, target_loc)
            #print step
            if (step != None) and (distance != None):
                value = distance - step
            else:
                value = None
            action = {'action_type': 'movement', 'location': neighbor, 'cost': value}
            # print action
            action_list.append(action)
        # win move
        intersection = set(neighbors).intersection(set(target_loc))
        if intersection != set([]):
            location = list(intersection)[0]
            value = width*height
            action = {'action_type': 'movement', 'location': location, 'cost': value}
            action_list.append(action)            
        # building
        if player['amount_of_walls'] > 0:
            for i in range(1, width):
                for j in range(1, height):
                    location = (i, j)
                    if p[location] != set([]):           
                        for wall_type in p[location]:
                            projected_wall_list = list(wall_list)
                            wall = {'type': wall_type, 'location': location, 'player_id': player['id']}
                            projected_wall_list.append(wall)
                            distances = []
                            for opponent in opponent_list:
                                projected_available_positions = available_positions_generator(opponent['location'], projected_wall_list, player_list)
                                [step, dummy] = bfs(opponent['location'], projected_available_positions, opponent['target_loc'])
                                distances.append(step)
                            distance = min(distances)
                            projected_available_positions = available_positions_generator(loc, projected_wall_list, player_list)
                            [step, dummy] = bfs(loc, projected_available_positions, target_loc)
                            if (step != None) and (distance != None):
                                value = distance - step
                                action = {'action_type': 'building', 'wall': wall, 'cost': value}
                                #print action  
                                action_list.append(action)            
            #print action_list
        # action select
        maximal_cost = None
        equal_actions_list = []
        for actions in action_list:
            if actions['cost'] > maximal_cost:
                equal_actions_list = []
                maximal_cost = actions['cost']
                action = actions
                equal_actions_list.append(action)
            elif actions['cost'] == maximal_cost:
                action = actions
                equal_actions_list.append(action)
        variants = len(equal_actions_list)
        if variants != 0:
            action = equal_actions_list[random.randint(0, variants - 1)]
        else:
            action = {'action_type': None}      
        # print action
        if action['action_type'] == 'movement':
            (x, y) = action['location']
            player['location'] = (x, y)
            players[x][y] = 1 
        elif action['action_type'] == 'building':
            wall_list.append(action['wall'])
            player['amount_of_walls'] -= 1   
        else:
            pass   
    else:
        pass
