from ..algorithms import *
from branch_generator import *
inf = float("infinity")

def turn(player, player_list, wall_list, available_positions, adjacency_list):
    # current game state 
    game_state = {}
    game_state['player'] = player
    game_state['wall_list'] = wall_list
    game_state['player_list'] = player_list
    game_state['turn'] = 0

    # bot stupefying
    opponents_walls_counter = 0
    for opponent in player_list:
        if opponent != player:
            opponents_walls_counter += opponent['amount_of_walls']
    if player['amount_of_walls'] != 0:
        if opponents_walls_counter != 0:
            depth = 2
        else:
            depth = 2
    else:
        if opponents_walls_counter != 0:
            depth = 0
        else:
            depth = 6
    
    # game tree
    index = 0
    game_tree = {}
    root = {index: {'parent': None, 'child': [], 'game_state': game_state, 'expanded': False, 'initial': -inf, 'final': -inf, 'alpha': None, 'beta': None, 'owner': 'max', 'action': None, 'is_node': False}}
    game_tree.update(root)
    # game tree dfs
    level = 0
    stack = [index]
    while stack:
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
        if level % len(player_list) == 0:
            owner = 'max'
        else:
            owner = 'min'

        # final branches detection 
        if level < depth:
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

            # in depth params transition
            if parent != 0:
                grandparent = game_tree[parent]['parent']
                alpha = game_tree[grandparent]['alpha']
                beta = game_tree[grandparent]['beta']
                game_tree[parent]['alpha'] = alpha
                game_tree[parent]['beta'] = beta

            else:
                if owner == 'max':
                    if game_tree[parent]['owner'] == 'min':
                        alpha = None
                        beta = game_tree[parent]['initial']
                elif owner == 'min':
                    if game_tree[parent]['owner'] == 'max':
                        alpha = game_tree[parent]['initial']
                        beta = None
            branch = branch_generator(current_game_state, adjacency_list, game_tree[parent]['owner'], game_tree[parent]['alpha'], game_tree[parent]['beta'], is_final, depth)
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
                if level < depth and abs(value) != inf:
                    weighted_subbranches.append((index, value))
                else:
                    game_tree[index]['is_node'] = True
                    if owner == 'max':
                        initial = final = - value
                        #print initial
                        game_tree[index]['initial'] = initial
                        game_tree[index]['final'] = final
                        if game_tree[parent]['owner'] == 'min':
                            if game_tree[parent]['initial'] > final:
                                game_tree[parent]['initial'] = final
                                if final == -inf:
                                    game_tree[parent]['alpha'] = -inf

                    elif owner == 'min':
                        initial = final = value
                        #print initial
                        game_tree[index]['initial'] = initial 
                        game_tree[index]['final'] = final
                        if game_tree[parent]['owner'] == 'max':
                            if game_tree[parent]['initial'] < final:
                                game_tree[parent]['initial'] = final
                                if final == inf:
                                    game_tree[parent]['beta'] = final

            game_tree[parent]['child'].extend(child_list)
            game_tree[parent]['expanded'] = True

            # ordering subbranches by preliminary evaluation
            weighted_subbranches = sorted(weighted_subbranches, key=lambda subbranch: subbranch[1], reverse=True)

            subbranches = [subbranch for (subbranch, weight) in weighted_subbranches]
    
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
                game_tree[parent]['action']['cost'] = final 
                grandparent = game_tree[parent]['parent']
                initial = game_tree[grandparent]['initial']   
                # from depth params transition     
                if owner == 'max':
                    #print game_tree[parent]['final']
                    if game_tree[grandparent]['owner'] == 'min':
                        if initial >= final:
                            game_tree[grandparent]['initial'] = final
                            if final != inf:
                                game_tree[grandparent]['alpha'] = final
                            else:
                                game_tree[grandparent]['alpha'] = None
                elif owner == 'min':
                    #print game_tree[parent]['final']
                    if game_tree[grandparent]['owner'] == 'max':
                        if initial < final:
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

            if game_tree[grandparent]['owner'] == 'max':
                #print game_tree[parent]['final']
                if game_tree[parent]['owner'] == 'min':
                    if alpha != None: 
                        if value > alpha:
                            for child in game_tree[grandparent]['child']:
                                if not game_tree[child]['expanded'] and child in stack:
                                    stack.remove(child)
                                    game_tree[grandparent]['child'].remove(child)

            if game_tree[grandparent]['owner'] == 'min':
                #print game_tree[parent]['final']
                if game_tree[parent]['owner'] == 'max':
                    if beta != None: 
                        if (value < beta) or (beta == inf):
                            for child in game_tree[grandparent]['child']:
                                if not game_tree[child]['expanded'] and child in stack:
                                    stack.remove(child)
                                    game_tree[grandparent]['child'].remove(child)

    # action select
    level = 0
    action_list = []
    #print 'actions: '
    #print 'level: ', level
    #print game_tree[level]['child']
    for child in game_tree[level]['child']:
        action_list.append(game_tree[child]['action'])
        #print game_tree[child]['action']

    action = action_choice_greedy(action_list)

    if action['action_type'] == 'movement':
        (x, y) = action['location']
        player['location'] = (x, y)
    elif action['action_type'] == 'building':
        wall_list.append(action['wall'])
        player['amount_of_walls'] -= 1   
    else:
        pass
