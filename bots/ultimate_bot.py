from algorithms import *
import random
import copy
DEBUG = False
inf = float("infinity")

def branch_generator(game_state, adjacency_list, owner, alpha, beta, is_final):
    pruning = False
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
        # node pruning
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
            current_game_state['player_list'][current_player].update({'location': location}) 
            current_game_state.update({'player': player_list[next_player]})
        branch['nodes'].append({'action': action, 'game_state': current_game_state})
        # node pruning
        if is_final:
            pruning = alpha_beta_pruning(alpha, beta, value, owner)

    # building
    if (player['amount_of_walls'] > 0) and not pruning:
        places = trace2places(trace)
        for location in places:
            if pruning:
                break
            if p[location] != set([]) and not pruning:
                for wall_type in p[location]:
                    if pruning:
                        break
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
                    # node pruning
                    if is_final:
                        pruning = alpha_beta_pruning(alpha, beta, value, owner)
                    if pruning:
                        break        
    return branch

def turn(player, players, player_list, wall_list, available_positions, adjacency_list):
    # current game state 
    game_state = {}
    game_state.update({'player': player})
    game_state.update({'players': players})
    game_state.update({'wall_list': wall_list})
    game_state.update({'player_list': player_list})
    # game tree
    depth = 3
    index = 0
    game_tree = {}
    root = {index: {'parent': None, 'child': [], 'game_state': game_state, 'expanded': False, 'initial': -inf, 'final': -inf, 'alpha': None, 'beta': None, 'owner': 'max', 'action': None, 'is_node': False}}
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
            if DEBUG:
                print owner
                print game_tree[parent]['owner']

            # in depth params transition
            if parent != 0:
                grandparent = game_tree[parent]['parent']
                alpha = game_tree[grandparent]['alpha']
                beta = game_tree[grandparent]['beta']
                game_tree[parent]['alpha'] = alpha
                game_tree[parent]['beta'] = beta
                if DEBUG:
                    print "in depth params transition"
                    print "from", grandparent, "to", parent
                    print game_tree[grandparent]['owner']               
                    print game_tree[parent]['owner']
                    print "alpha:", alpha, "beta:", beta
            else:
                if owner == 'max':
                    if game_tree[parent]['owner'] == 'min':
                        alpha = None
                        beta = game_tree[parent]['initial']
                elif owner == 'min':
                    if game_tree[parent]['owner'] == 'max':
                        alpha = game_tree[parent]['initial']
                        beta = None

            branch = branch_generator(current_game_state, adjacency_list, game_tree[parent]['owner'], game_tree[parent]['alpha'], game_tree[parent]['beta'], is_final)
            #print branch['nodes']
            child_list = []
            weighted_subbranches = []
            for state in branch['nodes']:
                index += 1
                action = state['action']
                value = action['cost']      
                #print action
                node_game_state = state['game_state']
                node = {index: {'parent': parent, 'child': [], 'game_state': node_game_state, 'action': action, 'expanded': False, 'initial': initial, 'final': final, 'alpha': alpha, 'beta': beta, 'owner': owner, 'is_node': False}}
                game_tree.update(node)
                #print node
                child_list.append(index)         
                if (level < depth) and (abs(value) != inf):
                    weighted_subbranches.append((index, value))
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
                                if (final == -inf):
                                    game_tree[parent]['alpha'] = -inf

                    elif owner == 'min':
                        initial = final = value
                        #print initial
                        game_tree[index]['initial'] = initial 
                        game_tree[index]['final'] = final
                        if game_tree[parent]['owner'] == 'max':
                            if game_tree[parent]['initial'] < final:
                                game_tree[parent]['initial'] = final
                                if (final == inf):
                                    game_tree[parent]['beta'] = final

            game_tree[parent]['child'].extend(child_list)
            game_tree[parent]['expanded'] = True
            if DEBUG:
                print 'subbranches: '
                print weighted_subbranches

            # ordering subbranches by preliminary evaluation
            weighted_subbranches = sorted(weighted_subbranches, key=lambda subbranch: subbranch[1], reverse=True)
            
            if DEBUG: print weighted_subbranches

            subbranches = []
            for (subbranch, weight) in weighted_subbranches:
                subbranches.append(subbranch)
    
            # stack forming
            subbranches.reverse()
            stack.extend(subbranches)

        else:
            initial = game_tree[parent]['initial']
            final = initial
            #print 'final: ', final
            game_tree[parent]['final'] = final
            grandparent = game_tree[parent]['parent']
            if parent != 0:
                if DEBUG:
                    print game_tree[parent]['owner']
                    print game_tree[grandparent]['owner']
                game_tree[parent]['action'].update({'cost': final}) 
                grandparent = game_tree[parent]['parent']
                initial = game_tree[grandparent]['initial']   
                # from depth params transition     
                if owner == 'max':
                    #print game_tree[parent]['final']
                    if game_tree[grandparent]['owner'] == 'min':
                        if (initial >= final):
                            game_tree[grandparent]['initial'] = final
                            if final != inf:
                                game_tree[grandparent]['alpha'] = final
                            else:
                                game_tree[grandparent]['alpha'] = None
                elif owner == 'min':
                    #print game_tree[parent]['final']
                    if game_tree[grandparent]['owner'] == 'max':
                        if (initial < final):
                            game_tree[grandparent]['initial'] = final
                            if final != -inf:
                                game_tree[grandparent]['beta'] = final
                            else:
                                game_tree[grandparent]['beta'] = None

        # branch pruning
        if parent != 0:
            grandparent = game_tree[parent]['parent']
            value = game_tree[parent]['initial']
            alpha = game_tree[parent]['alpha']
            beta = game_tree[parent]['beta']
            if DEBUG:
                print 'owner:', owner
                print 'grandparent owner:', game_tree[grandparent]['owner']
                print 'parent owner:', game_tree[parent]['owner']
                print 'value:', value
                print 'alpha:', alpha
                print 'beta:', beta

            if game_tree[grandparent]['owner'] == 'max':
                #print game_tree[parent]['final']
                if game_tree[parent]['owner'] == 'min':
                    # branch pruning
                    if alpha != None: 
                        if (value > alpha) or (alpha == -inf):
                            if DEBUG:
                                print "alpha pruning"
                                print parent
                                print game_tree[parent]['child']
                                print game_tree[grandparent]['child']
                                print stack
                            for child in game_tree[grandparent]['child']:
                                if DEBUG:
                                    print child, game_tree[child]['expanded']
                                if not game_tree[child]['expanded'] and child in stack:
                                    if DEBUG:
                                        print "pruning node", child  
                                    stack.remove(child)
                                    game_tree[grandparent]['child'].remove(child)

            if game_tree[grandparent]['owner'] == 'min':
                #print game_tree[parent]['final']
                if game_tree[parent]['owner'] == 'max':
                    if beta != None: 
                        if (value < beta) or (beta == inf):
                            if DEBUG:
                                print "beta pruning"
                                print parent
                                print game_tree[parent]['child']
                                print game_tree[grandparent]['child']
                                print stack
                            for child in game_tree[grandparent]['child']:
                                if DEBUG:
                                    print child, game_tree[child]['expanded']
                                if not game_tree[child]['expanded'] and child in stack:
                                    if DEBUG:
                                        print "pruning node", child  
                                    stack.remove(child)
                                    game_tree[grandparent]['child'].remove(child)

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
                alpha = game_tree[node]['alpha']
                beta = game_tree[node]['beta']
                owner = game_tree[node]['owner']
                is_node = game_tree[node]['is_node']
                expanded = game_tree[node]['expanded']
                print "node: %s; expanded: %s, is_node: %s; parent: %s; child: %s; initial: %s; final: %s; alpha: %s; beta: %s; owner: %s;"\
                        %(node, expanded, is_node, parent, child_list, initial, final, alpha, beta, owner)
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
