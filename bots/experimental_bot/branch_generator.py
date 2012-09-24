from ..algorithms import *
import copy
import math
DEBUG = False
inf = float("infinity")     

def branch_generator(game_state, adjacency_list, owner, alpha, beta, is_final):
    pruning = False
    # branch init
    branch = {}
    branch['nodes'] = []
    # data gathering from game state
    player = game_state['player']
    player_list = game_state['player_list']
    wall_list = game_state['wall_list']
    #print wall_list
    # player detection
    current_player = player_list.index(player)
    player_id = player['id']
    #print 'player_number: ', current_player
    next_player = (current_player + 1) % len(player_list)
    # old
    loc = player['location']
    target_loc = player['target_loc']
    #opponent_list
    opponent_list = [item for item in player_list if item != player]
    #neigbors
    available_positions = available_positions_generator(loc, wall_list, player_list, adjacency_list)
    neighbors = [location for location in available_positions[loc]]
    #possibility matrix
    p = w2p(wall_list)
    #actions
    action_list = []  

    # opponents walls counter
    opponents_walls_counter = 0
    for opponent in opponent_list:
        opponents_walls_counter += opponent['amount_of_walls']

    #movement
    distances = {}
    for opponent in opponent_list:
        #print opponent
        opponent_id = opponent['id']
        opponent_available_positions =\
            available_positions_generator(opponent['location'], 
                                          wall_list, 
                                          player_list, 
                                          adjacency_list)
        step = spwi(opponent['location'], 
                    opponent_available_positions, 
                    opponent['target_loc'])
        #print step
        distances[opponent_id] = step
    distance = min(distances.values())

    #trace = list(subtrace)
    #print distance
    for neighbor in neighbors:
        # leafs don't need game state copy
        if is_final:
            current_game_state = {}
        else:
            current_game_state = copy.deepcopy(game_state)
            current_game_state['player_list'][current_player]['location'] = neighbor 
            current_game_state['player'] = player_list[next_player]

        step = spwi(neighbor, available_positions, target_loc)
        #print step
        value = distance - step
        if value == inf:
            value = width*height
        if value == -inf:
            value = -width*height
        # win move   
        if step == 0:
            value = inf
        if math.isnan(value):
            value = -width*height
        #print 'cost: ', value
        #print 'estimate: ', estimate
        action = {'action_type': 'movement', 'location': neighbor, 'cost': value}
        ##print action
        branch['nodes'].append({'action': action, 'game_state': current_game_state})
        if is_final:
            pruning = alpha_beta_pruning(alpha, beta, value, owner)
        if pruning:
            break

    # building
    if (player['amount_of_walls'] > 0) and not pruning:
        for location in p:
            if (p[location] != set([])) and not pruning:
                for wall_type in p[location]:
                    projected_wall_list = list(wall_list)
                    wall = {'type': wall_type, 
                            'location': location, 
                            'player_id': player_id
                    }
                    projected_wall_list.append(wall)

                    is_reachable = True

                    # leafs don't need game state copy
                    if is_final:
                        current_game_state = {}
                    else:
                        current_game_state = copy.deepcopy(game_state)
                        current_game_state['wall_list'].append(wall)
                        current_game_state['player_list'][current_player]['amount_of_walls'] -= 1  
                        current_game_state['player'] = player_list[next_player]

                    # reachability detection
                    projected_available_positions =\
                        available_positions_generator(loc, 
                                                      projected_wall_list,
                                                      [],
                                                      adjacency_list)
                    step = spwi(loc, 
                                projected_available_positions, 
                                target_loc)

                    player_free_distance = step

                    if player_free_distance == inf:
                        is_reachable = False

                    # step meter
                    if is_reachable:
                        projected_available_positions =\
                            available_positions_generator(loc, 
                                                          projected_wall_list,
                                                          player_list,
                                                          adjacency_list)
                        player_distance = spwi(loc, 
                                                projected_available_positions, 
                                                target_loc)

                    if is_reachable:
                        free_distances = {}
                        distances = {}
                        for opponent in opponent_list:
                            opponent_id = opponent['id']
                            # reachability detection
                            projected_available_positions =\
                                available_positions_generator(opponent['location'],
                                                                projected_wall_list,
                                                                [],
                                                                adjacency_list)
                            step = spwi(opponent['location'], 
                                        projected_available_positions, 
                                        opponent['target_loc'])

                            free_distances[opponent_id] = step
                            if step == inf:
                                is_reachable = False
                                break

                            # step meter
                            if is_reachable:
                                projected_available_positions =\
                                    available_positions_generator(opponent['location'],
                                                                    projected_wall_list,
                                                                    player_list,
                                                                    adjacency_list)
                                step = spwi(opponent['location'], 
                                            projected_available_positions, 
                                            opponent['target_loc'])
                                #print step
                                distances[opponent_id] = step
                        if is_reachable:
                            opponent_distance = min(distances.values())

                    value = None
                    if is_reachable:
                        if opponent_distance == inf:
                            opponent_distance = min(free_distances.values()) + player['amount_of_walls'] - 1
                        if player_distance == inf:
                            player_distance = player_free_distance + opponents_walls_counter

                        value = opponent_distance - player_distance
                        #print 'cost: ', value
                        #print 'estimate: ', estimate
                        action = {'action_type': 'building', 'wall': wall, 'cost': value}
                        #print action 
                        branch['nodes'].append({'action': action, 'game_state': current_game_state})           
                        action_list.append(action)
                    # node pruning
                    if is_final and value != None:
                        pruning = alpha_beta_pruning(alpha, beta, value, owner)
                    if pruning:
                        break    
    return branch
