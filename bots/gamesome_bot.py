from algorithms import *
import random
import copy
DEBUG = True

def trace2places(trace):
    places = []
    offsets = ((0, 0), (1, 0), (0, 1), (1, 1))
    for location in trace:
        (col, row) = location
        for offset in offsets:
            (offset_col, offset_row) = offset
            (place_col, place_row) = (col + offset_col, row + offset_row)
            place = (place_col, place_row)
            if (place_col > 0) and (place_col < width) and\
                (place_row > 0) and (place_row < height) and\
                place not in places:
                places.append(place)
    return places

def branch_generator(game_state, adjacency_list):
    # branch init
    branch = {}
    branch.update({'nodes': []})
    # data gathering from game state
    player = game_state['player']
    players = game_state['players']
    player_list = game_state['player_list']
    wall_list = game_state['wall_list']
    # player detection
    current_player = player_list.index(player)
    #print 'player_number: ', current_player
    next_player = (current_player + 1) % len(player_list)
    # old
    loc = player['location']
    target_loc = player['target_loc']
    #opponent_list
    opponent_list = []
    for item in player_list:
        if item != player:
            opponent_list.append(item)
    #neigbors
    neighbors = []
    available_positions = available_positions_generator(loc, wall_list, player_list, adjacency_list)
    for location in available_positions[loc]:
        neighbors.append(location)
    #possibility matrix
    p = w2p(wall_list)
    #actions
    action_list = []
    #movement
    distances = []
    subtrace = set([])
    for opponent in opponent_list:
        #print opponent
        opponent_available_positions =\
            available_positions_generator(opponent['location'], 
                                          wall_list, 
                                          player_list, 
                                          adjacency_list)
        [step, trace] = bfs(opponent['location'], 
                            opponent_available_positions, 
                            opponent['target_loc'])
        subtrace |= set(trace)
        #print step
        distances.append(step)
    distance = min(distances)
    trace = list(subtrace)
    #print distance
    for neighbor in neighbors:
        current_game_state = copy.deepcopy(game_state)
        [step, dummy] = bfs(neighbor, available_positions, target_loc)
        #print step
        if (step != None) and (distance != None):
            value = distance - step
            action = {'action_type': 'movement', 'location': neighbor, 'cost': value}
            # print action        
            (x, y) = neighbor
            current_game_state['players'][x][y] = 1 
            current_game_state['player_list'][current_player].update({'location': neighbor}) 
            current_game_state.update({'player': player_list[next_player]})
            branch['nodes'].append({'action': action, 'game_state': current_game_state})           
    # cost evaluation
    # win move
    intersection = set(neighbors).intersection(set(target_loc)) 
    if intersection != set([]):
        current_game_state = copy.deepcopy(game_state)
        location = list(intersection)[0]
        value = width * height
        action = {'action_type': 'movement', 'location': location, 'cost': value}
        action_list.append(action)
        (x, y) = location
        current_game_state['players'][x][y] = 1 
        current_game_state['player_list'][current_player].update({'location': location}) 
        current_game_state.update({'player': player_list[next_player]})
        branch['nodes'].append({'action': action, 'game_state': current_game_state})   
    # building
    if player['amount_of_walls'] > 0:
        places = trace2places(trace)
        for location in places:
            if p[location] != set([]):
                for wall_type in p[location]:
                    current_game_state = copy.deepcopy(game_state)
                    projected_wall_list = list(wall_list)
                    wall = {'type': wall_type, 
                            'location': location, 
                            'player_id': player['id']
                    }
                    projected_wall_list.append(wall)
                    distances = []
                    for opponent in opponent_list:
                        projected_available_positions =\
                            available_positions_generator(opponent['location'],                                                     projected_wall_list,
                                                          player_list,
                                                          adjacency_list)
                        [step, dummy] = bfs(opponent['location'], 
                                            projected_available_positions, 
                                            opponent['target_loc'])
                        distances.append(step)
                    distance = min(distances)
                    projected_available_positions =\
                        available_positions_generator(loc, 
                                                      projected_wall_list,
                                                      player_list,
                                                      adjacency_list)
                    [step, dummy] = bfs(loc, 
                                        projected_available_positions, 
                                        target_loc)
                    if (step != None) and (distance != None):
                        value = distance - step
                        action = {'action_type': 'building', 'wall': wall, 'cost': value}
                        #print action          
                        current_game_state['wall_list'].append(wall)
                        current_game_state['player_list'][current_player]['amount_of_walls'] -= 1  
                        current_game_state.update({'player': player_list[next_player]})
                        branch['nodes'].append({'action': action, 'game_state': current_game_state})           
                        action_list.append(action)            
        #print action_list
    return branch

def negamax(game_tree, depth, amount_of_players):
    action_list = []
    level = 0
    sequence = [0]
    level_list = []
    while level < depth:
        new_sequence = []
        level_list.append([])
        for parent in sequence:
            sublist = []
            for child in game_tree[parent]['child']:
                sublist.append(child)
                new_sequence.append(child)
            level_list[level].append(sublist)
        sequence = new_sequence 
        level += 1
    
    #print level_list
    level -= 1

    while level > 0:
        #print 'level: ', level
        for sublist in level_list[level]:
            if (sublist != []):
                cost_list = [] 
                for child in sublist:
                    cost = game_tree[child]['action']['cost']
                    cost_list.append(cost)
                max_cost = max(cost_list)
                parent = game_tree[child]['parent']
                max_cost = - max_cost
                game_tree[parent]['action'].update({'cost': max_cost})
        level -= 1      

    #print 'actions: '
    #print 'level: ', level
    for child in game_tree[level]['child']:
        action_list.append(game_tree[child]['action'])
        #print game_tree[child]['action']

    maximal_cost = None
    equal_actions_list = []
    for actions in action_list:
        if (actions['cost'] > maximal_cost):
            equal_actions_list = []
            maximal_cost = actions['cost']
            action = actions
            equal_actions_list.append(action)
        elif actions['cost'] == maximal_cost:
            action = actions
            equal_actions_list.append(action)
    variants = len(equal_actions_list)
    if variants != 0:
        action = random.choice(equal_building_actions_list)
    else:
        action = {'action_type': None}
    #print action
    return action

def turn(player, players, player_list, wall_list, available_positions, adjacency_list):
    # current game state 
    game_state = {}
    game_state.update({'player': player})
    game_state.update({'players': players})
    game_state.update({'wall_list': wall_list})
    game_state.update({'player_list': player_list})
    game_state.update({'end': False})
    # game tree
    depth = 2
    index = 0
    game_tree = {}
    root = {index: {'parent': None, 'child': [], 'game_state': game_state}}
    game_tree.update(root)
    # game tree bfs
    level = 0
    sequence = [index]
    while level < depth:
        #print 'level: ', level 
        new_sequence = []
        #print sequence 
        for element in sequence:
            current_game_state = game_tree[element]['game_state']
            #print current_game_state
            is_end = current_game_state['end']
            if is_end:
                index += 1
                node_game_state = game_tree[element]['game_state']
                action = game_tree[element]['action']
                value = action['cost']
                action['cost'] = - value
                node = {index: {'parent': element, 'child': [], 'game_state': node_game_state, 'action': action}}
                game_tree[element]['child'].append(index)
                game_tree.update(node)
                new_sequence.append(index)
            else:
                branch = branch_generator(current_game_state, adjacency_list)
                #print branch['nodes']
                for state in branch['nodes']:
                    index += 1
                    action = state['action']
                    value = action['cost']
                    if abs(value) == width * height:
                        is_end = True
                    state['game_state']['end'] = is_end             
                    #print action
                    node_game_state = state['game_state']
                    node = {index: {'parent': element, 'child': [], 'game_state': node_game_state, 'action': action}}
                    game_tree[element]['child'].append(index)
                    game_tree.update(node)
                    new_sequence.append(index)
        level += 1
        #print level
        sequence = new_sequence
        #print sequence

    # action select
    action = negamax(game_tree, depth, len(player_list))
    if action['action_type'] == 'movement':
        (x, y) = action['location']
        player['location'] = (x, y)
        players[x][y] = 1 
    elif action['action_type'] == 'building':
        wall_list.append(action['wall'])
        player['amount_of_walls'] -= 1   
    else:
        pass
