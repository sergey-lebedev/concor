from ..algorithms import *
from branch_generator import *
#import shelve
import __builtin__
import copy
DEBUG = False
inf = float("infinity")

def turn(player, player_list, wall_list, available_positions, adjacency_list):
    # opening storage
    #filename = str(player['id']) + '.mem'
    #storage = shelve.open(filename)

    # restructing storage
    #key = cache.keygen(player_list, wall_list)
    #cache.restruct(key)
    cache.init()

    #print storage_struct

    # current game state
    game_state = {}
    game_state['player'] = player
    game_state['wall_list'] = wall_list
    game_state['player_list'] = player_list

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
            key = cache.keygen(current_game_state['player_list'], current_game_state['wall_list'])
            branch = branch_generator(current_game_state, adjacency_list, game_tree[parent]['owner'], game_tree[parent]['alpha'], game_tree[parent]['beta'], is_final, level)
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
            if DEBUG:
                print 'subbranches: '
                print weighted_subbranches

            # ordering subbranches by preliminary evaluation
            weighted_subbranches = sorted(weighted_subbranches, key=lambda subbranch: subbranch[1], reverse=True)

            if DEBUG: print weighted_subbranches

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
                if DEBUG:
                    print game_tree[parent]['owner']
                    print game_tree[grandparent]['owner']
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
                        if value > alpha:
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

    # closing storage
    #storage.close()

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
