from algorithms import *
import random
import copy
DEBUG = False
inf = float("infinity")

def trace2places(trace):
    places = []
    offsets = [(0, 0), (1, 0), (0, 1), (1, 1)]
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

def branch_generator(game_state, adjacency_list, is_final):
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

    # self trace | defend mode
    [step, trace] = bfs(loc, available_positions, target_loc)
    subtrace |= set(trace)

    trace = list(subtrace)
    #print distance
    for neighbor in neighbors:
        # leafs don't need game state copy
        if is_final:
            current_game_state = {}
        else:
            current_game_state = copy.deepcopy(game_state)

        [step, dummy] = bfs(neighbor, available_positions, target_loc)
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
        value = inf
        action = {'action_type': 'movement', 'location': location, 'cost': value}
        action_list.append(action)
        (x, y) = location
        current_game_state['players'][x][y] = 1 
        current_game_state['player_list'][current_player].update({'location': location}) 
        current_game_state.update({'player': player_list[next_player]})
        branch['nodes'].append({'action': action, 'game_state': current_game_state})
    # building
    if (player['amount_of_walls'] > 0):
        places = trace2places(trace)
        for location in places:
            if p[location] != set([]):
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
                        #print 'cost: ', value
                        #print 'estimate: ', estimate
                        action = {'action_type': 'building', 'wall': wall, 'cost': value}
                        #print action 
                        if not is_final:
                            current_game_state['wall_list'].append(wall)
                            current_game_state['player_list'][current_player]['amount_of_walls'] -= 1  
                            current_game_state.update({'player': player_list[next_player]})
                        branch['nodes'].append({'action': action, 'game_state': current_game_state})           
                        action_list.append(action)            
    return branch

def turn(player, players, player_list, wall_list, available_positions, adjacency_list):
    # current game state 
    game_state = {}
    game_state.update({'player': player})
    game_state.update({'players': players})
    game_state.update({'wall_list': wall_list})
    game_state.update({'player_list': player_list})
    # game tree
    depth = 2
    index = 0
    game_tree = {}
    root = {index: {'parent': None, 'child': [], 'game_state': game_state, 'expanded': False, 'initial': -inf, 'final': -inf, 'owner': 'max', 'action': None, 'is_node': False}}
    game_tree.update(root)

    # game tree dfs
    level = 0
    stack = [index]
    while (stack != []):
        # get ancestor
        parent = stack[-1]
        #print 'parent: '
        #print parent
        if game_tree[parent]['expanded']:
            stack.pop(-1)
            level -= 1
        else:
            level += 1
        #print 'stack:'
        #print stack
        current_game_state = game_tree[parent]['game_state']
        #print current_game_state
        # owner detector
        if (level % len(player_list) == 0):
            owner = 'max'
        else:
            owner = 'min'

        # final branches detection 
        if (level < depth):
            is_final = False
        else:
            is_final = True

        if not game_tree[parent]['expanded']:
            # brach generator
            if owner == 'max':
                if game_tree[parent]['owner'] == 'min':
                    initial = final = -inf
            elif owner == 'min':
                if game_tree[parent]['owner'] == 'max':
                    initial = final = inf
            branch = branch_generator(current_game_state, adjacency_list, is_final)
            #print branch['nodes']
            child_list = []
            subbranches = []
            for state in branch['nodes']:
                index += 1
                action = state['action']
                value = action['cost']      
                #print action
                node_game_state = state['game_state']
                node = {index: {'parent': parent, 'child': [], 'game_state': node_game_state, 'action': action, 'expanded': False, 'initial': initial, 'final': final, 'owner': owner, 'is_node': False}}
                game_tree.update(node)
                #print node
                child_list.append(index)         
                if (level < depth) and (abs(value) != inf):
                    subbranches.append(index)
                else:
                    game_tree[index]['is_node'] = True
                    if DEBUG: 
                        print 'node:', index, ' termination'
                    if owner == 'max':
                        initial = final = - value
                        #print initial
                        game_tree[index]['initial'] = initial
                        game_tree[index]['final'] = final
                        if game_tree[parent]['owner'] == 'min':
                            if game_tree[parent]['initial'] > final:
                                game_tree[parent]['initial'] = final
                    elif owner == 'min':
                        initial = final = value
                        #print initial
                        game_tree[index]['initial'] = initial 
                        game_tree[index]['final'] = final
                        if game_tree[parent]['owner'] == 'max':
                            if game_tree[parent]['initial'] < final:
                                game_tree[parent]['initial'] = final
                       
            # stack forming
           #print 'child list: '
           #print child_list
           #print 'subbranches: '
           #print subbranches   
            game_tree[parent]['child'].extend(child_list)
            subbranches.reverse()
            stack.extend(subbranches)
           #print stack
            #print 'level: '
            #print level
            game_tree[parent]['expanded'] = True
        else:
            initial = game_tree[parent]['initial']
            final = initial
            #print 'final: ', final
            game_tree[parent]['final'] = final
            grandparent = game_tree[parent]['parent']
            if parent != 0:
                game_tree[parent]['action'].update({'cost': final}) 
                grandparent = game_tree[parent]['parent']
                initial = game_tree[grandparent]['initial']        
                if owner == 'max':
                    #print game_tree[parent]['final']
                    if game_tree[grandparent]['owner'] == 'min':
                        if (initial > final):
                            game_tree[grandparent]['initial'] = final
                elif owner == 'min':
                    #print game_tree[parent]['final']
                    if game_tree[grandparent]['owner'] == 'max':
                        if (initial < final):
                            game_tree[grandparent]['initial'] = final

        if DEBUG:
            print "debug output. game tree structure."
            sequence = []
            sequence.append(0)
            while (sequence != []):
                node = sequence.pop(0)
                parent = game_tree[node]['parent']
                child_list = game_tree[node]['child']
                initial = game_tree[node]['initial']
                final = game_tree[node]['final']
                owner = game_tree[node]['owner']
                is_node = game_tree[node]['is_node']
                print "node: %s; is_node: %s; parent: %s; child: %s; initial: %s; final: %s; owner: %s;"\
                        %(node, is_node, parent, child_list, initial, final, owner)
                #print 'action: ', game_tree[node]['action']
                sequence.extend(child_list)

    level = 0
    # action select
    action_list = []
    #print 'actions: '
    #print 'level: ', level
    #print game_tree[level]['child']
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
        action = equal_actions_list[random.randint(0, variants - 1)]
    else:
        action = {'action_type': None}
    #print action

    if action['action_type'] == 'movement':
        (x, y) = action['location']
        player['location'] = (x, y)
        players[x][y] = 1 
    elif action['action_type'] == 'building':
        wall_list.append(action['wall'])
        player['amount_of_walls'] -= 1   
    else:
        pass
