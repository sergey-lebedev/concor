from ..algorithms import *
import copy
DEBUG = False
inf = float("infinity")

def branch_generator(game_state, adjacency_list, owner, storage, alpha, beta, is_final):
    pruning = False
    # branch init
    branch = {}
    branch['nodes'] = []
    # data gathering from game state
    player = game_state['player']
    player_list = game_state['player_list']
    wall_list = game_state['wall_list']
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
    #movement
    distances = []
    for opponent in opponent_list:
        opponent_id = player['id']
        #print opponent
        opponent_available_positions =\
            available_positions_generator(opponent['location'], 
                                          wall_list, 
                                          player_list, 
                                          adjacency_list)
        step = bfs_light(opponent['location'], 
                            opponent_available_positions, 
                            opponent['target_loc'])
        #print step
        distances.append(step)
    distance = min(distances)

    step = bfs_light(loc, available_positions, target_loc)

    #trace = list(subtrace)
    #print distance
    for neighbor in neighbors:
        # leafs don't need game state copy
        if is_final:
            current_game_state = {}
        else:
            current_game_state = copy.deepcopy(game_state)
        gamestate = str(game_state)
        #print gamestate
        if storage.has_key(gamestate):
            step = storage[gamestate]
            #print 'found!'
        else:   
            step = bfs_light(neighbor, available_positions, target_loc)
            storage[gamestate] = step   
        #print step
        if (step != None) and (distance != None):
            value = distance - step
        else:
            value = 0
        #print 'cost: ', value
        #print 'estimate: ', estimate
        action = {'action_type': 'movement', 'location': neighbor, 'cost': value}
        ##print action        
        (x, y) = neighbor
        if not is_final:
            current_game_state['player_list'][current_player]['location'] = neighbor 
            current_game_state['player'] = player_list[next_player]
        branch['nodes'].append({'action': action, 'game_state': current_game_state})
        if is_final:
            pruning = alpha_beta_pruning(alpha, beta, value, owner)
        if pruning:
            break
         
    # cost evaluation
    # win move
    intersection = set(neighbors).intersection(set(target_loc)) 
    if intersection != set([]):
        # leafs don't need game state copy
        if is_final:
            current_game_state = {}
        else:
            current_game_state = copy.deepcopy(game_state)

        location = list(intersection)[0]
        value = inf
        action = {'action_type': 'movement', 'location': location, 'cost': value}
        action_list.append(action)
        (x, y) = location
        if not is_final:
            current_game_state['players'][x][y] = 1 
            current_game_state['player_list'][current_player]['location'] = location 
            current_game_state['player'] = player_list[next_player]
        branch['nodes'].append({'action': action, 'game_state': current_game_state})
        # node pruning
        if is_final:
            pruning = alpha_beta_pruning(alpha, beta, value, owner)

    # building
    if (player['amount_of_walls'] > 0) and not pruning:
        for location in p:
            if (p[location] != set([])) and not pruning:
                for wall_type in p[location]:
                    # leafs don't need game state copy
                    if is_final:
                        current_game_state = {}
                    else:
                        current_game_state = copy.deepcopy(game_state)

                    projected_wall_list = list(wall_list)
                    wall = {'type': wall_type, 
                            'location': location, 
                            'player_id': player['id']
                    }
                    projected_wall_list.append(wall)
                    distances = []
                    for opponent in opponent_list:
                        opponent_id = opponent['id']
                        projected_available_positions =\
                            available_positions_generator(opponent['location'],                                                     projected_wall_list,
                                                          player_list,
                                                          adjacency_list)
                        step = bfs_light(opponent['location'], 
                                            projected_available_positions, 
                                            opponent['target_loc'])
                        distances.append(step)
                    distance = min(distances)
                    projected_available_positions =\
                        available_positions_generator(loc, 
                                                      projected_wall_list,
                                                      player_list,
                                                      adjacency_list)
                    step = bfs_light(loc, 
                                        projected_available_positions, 
                                        target_loc)
                    if (step != None) and (distance != None):
                        value = distance - step
                        #print 'cost: ', value
                        #print 'estimate: ', estimate
                        action = {'action_type': 'building', 'wall': wall, 'cost': value}
                        #print action 
                        if not is_final:
                            current_game_state['wall_list'].append(wall)
                            current_game_state['player_list'][current_player]['amount_of_walls'] -= 1  
                            current_game_state['player'] = player_list[next_player]
                        branch['nodes'].append({'action': action, 'game_state': current_game_state})           
                        action_list.append(action)
                    # node pruning
                    if is_final:
                        pruning = alpha_beta_pruning(alpha, beta, value, owner)
                    if pruning:
                        break    
    return branch
