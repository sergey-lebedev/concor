import copy
import random

DEBUG = False
inf = float("infinity")

def adjacency_list_generator():
    #adjacency_list
    adjacency_list = {}
    ij_list = [(i, j) for i in range(width) for j in range(height)]
    for (i, j) in ij_list:
        link_list = []
        #link_list = {}
        for direction in DIRECTIONS:
            (dx, dy) = DIRECTIONS[direction]
            dyj = dy + j
            dxi = dx + i
            if (0 <= dyj < height) and (0 <= dxi < width): 
                link_list.append((dxi, dyj))
                #link_list[(dxi, dyj)] = True
        adjacency_list[(i, j)] = set(link_list)
        #adjacency_list[(i, j)] = link_list

    return adjacency_list

def available_positions_generator(loc, wall_list, player_list, adjacency_list):
    # calculate available positions   
    available_positions = {}
    for position in adjacency_list:
        #print positions
        available_positions[position] = adjacency_list[position].copy()
    #available_positions = adjacency_list.copy()

    for wall in wall_list:
        (col, row) = wall['location']
        left_top = (col - 1, row - 1)  
        right_top = (col, row - 1) 
        left_bottom = (col - 1, row) 
        right_bottom = (col, row)

        #print left_top, right_top,left_bottom, right_bottom
        if wall['type'] == 'horizontal':
            available_positions[left_top].difference_update(set([left_bottom]))
            available_positions[left_bottom].difference_update(set([left_top])) 
            available_positions[right_top].difference_update(set([right_bottom]))    
            available_positions[right_bottom].difference_update(set([right_top]))         
        elif wall['type'] == 'vertical':        
            available_positions[left_top].difference_update(set([right_top]))
            available_positions[left_bottom].difference_update(set([right_bottom])) 
            available_positions[right_top].difference_update(set([left_top]))    
            available_positions[right_bottom].difference_update(set([left_bottom]))

    #occupied cells
    (col, row) = loc
    set_loc = set([loc])

    player_locations = []
    for player in player_list:
        player_locations.append(player['location'])

    for direction in DIRECTIONS:
        (dx, dy) = DIRECTIONS[direction]
        for a_loc in player_locations:
            if (a_loc == (col + dx, row + dy) and
                a_loc in available_positions[loc]):
                #print a_loc
                (a_col, a_row) = a_loc
                for neighbors in available_positions[a_loc]:
                    available_positions[neighbors].difference_update(set([a_loc]))

                b_loc = (a_col + dx, a_row + dy) 
                if (b_loc in available_positions[a_loc] and
                    b_loc not in player_locations):                            
                    available_positions[b_loc].update(set_loc)
                    available_positions[loc].update(set([b_loc]))
                else:
                    #sideway jump
                    (ldx, ldy) = DIRECTIONS[LEFT[direction]]
                    c_loc = (a_col + ldx, a_row + ldy)
                    if (c_loc in available_positions[a_loc] and
                        c_loc not in player_locations):
                        available_positions[c_loc].update(set_loc)
                        available_positions[loc].update(set([c_loc]))
                    (rdx, rdy) = DIRECTIONS[RIGHT[direction]]
                    d_loc = (a_col + rdx, a_row + rdy)
                    if (d_loc in available_positions[a_loc] and
                        d_loc not in player_locations):
                        available_positions[d_loc].update(set_loc)
                        available_positions[loc].update(set([d_loc]))        
                available_positions[a_loc] = set([])
    #print available_positions[loc]
    return available_positions

def iapg(player, wall_list, player_list, adjacency_list):
    # calculate available positions   
    available_positions = {}
    for position in adjacency_list:
        #print positions
        available_positions[position] = adjacency_list[position].copy()
    #available_positions = adjacency_list.copy()

    for wall in wall_list:
        (col, row) = wall['location']
        left_top = (col - 1, row - 1)  
        right_top = (col, row - 1) 
        left_bottom = (col - 1, row) 
        right_bottom = (col, row)

        #print left_top, right_top,left_bottom, right_bottom
        if wall['type'] == 'horizontal':
            available_positions[left_top].difference_update(set([left_bottom]))
            available_positions[left_bottom].difference_update(set([left_top])) 
            available_positions[right_top].difference_update(set([right_bottom]))    
            available_positions[right_bottom].difference_update(set([right_top]))         
        elif wall['type'] == 'vertical':        
            available_positions[left_top].difference_update(set([right_top]))
            available_positions[left_bottom].difference_update(set([right_bottom])) 
            available_positions[right_top].difference_update(set([left_top]))    
            available_positions[right_bottom].difference_update(set([left_bottom]))

    if player:
        # occupied cells
        loc = player['location']
        (col, row) = loc
        set_loc = set([loc])

        # opponent's locations
        opponent_locations = [item['location'] for item in player_list if item != player]

        for direction in DIRECTIONS:
            (dx, dy) = DIRECTIONS[direction]
            for a_loc in opponent_locations:
                if (a_loc == (col + dx, row + dy) and
                    a_loc in available_positions[loc]):
                    #print a_loc
                    (a_col, a_row) = a_loc
                    for neighbors in available_positions[a_loc]:
                        available_positions[neighbors].difference_update(set([a_loc]))

                    b_loc = (a_col + dx, a_row + dy) 
                    if (b_loc in available_positions[a_loc] and
                        b_loc not in opponent_locations):                            
                        available_positions[b_loc].update(set_loc)
                        available_positions[loc].update(set([b_loc]))
                    else:
                        #sideway jump
                        (ldx, ldy) = DIRECTIONS[LEFT[direction]]
                        c_loc = (a_col + ldx, a_row + ldy)
                        if (c_loc in available_positions[a_loc] and
                            c_loc not in opponent_locations):
                            available_positions[c_loc].update(set_loc)
                            available_positions[loc].update(set([c_loc]))
                        (rdx, rdy) = DIRECTIONS[RIGHT[direction]]
                        d_loc = (a_col + rdx, a_row + rdy)
                        if (d_loc in available_positions[a_loc] and
                            d_loc not in opponent_locations):
                            available_positions[d_loc].update(set_loc)
                            available_positions[loc].update(set([d_loc]))       
                    available_positions[a_loc] = set([])
    #print available_positions[loc]
    return available_positions

def w2p(wall_list):
    #print wall_list
    p = dict(((ij, ['horizontal', 'vertical']) for ij in ij_list_for_p))
    p_has_key = p.has_key

    #set_vertical = set(['vertical'])
    #set_horizontal = set(['horizontal'])

    for wall in wall_list:
        (x, y) = wall['location']
        #p[(x, y)] = set([])
        p[(x, y)] = []
        if wall['type'] == 'horizontal':
            for direction in ('w', 'e'):
                (dx, dy) = DIRECTIONS[direction]
                location = (x + dx, y + dy)
                if p_has_key(location):
                    #p[location].difference_update(set_horizontal)
                    if 'horizontal' in p[location]: p[location].remove('horizontal')
                    #if p[location].has_key('horizontal'): del p[location]['horizontal']
        elif wall['type'] == 'vertical':
            for direction in ('n', 's'):
                (dx, dy) = DIRECTIONS[direction]
                location = (x + dx, y + dy)
                if p_has_key(location):
                    #p[location].difference_update(set_vertical)
                    if 'vertical' in p[location]: p[location].remove('vertical')
                    #if p[location].has_key('vertical'): del p[location]['vertical']
    #print p
    return p

def bfs(loc, available_positions, target_loc):
    # breadth-first search
    neighbor = loc
    queue = [loc]   
    visited = {}   
    visited[loc] = True
    is_break = False
    path = {}
    while queue and not is_break:
        node = queue.pop(0)
        for neighbor in available_positions[node]:
            if not visited.has_key(neighbor):
                path[neighbor] = node
                visited[neighbor] = True
                if target_loc.has_key(neighbor):
                    is_break = True
                    #print neighbor
                queue.append(neighbor)
            if is_break: 
                break  

    if not is_break:
        step = None
    else:
        step = 0

    node = neighbor
    backtrace = [node]
    while (node != loc) and is_break:
        step += 1
        neighbor = node
        node = path[neighbor]
        backtrace.append(node)
    backtrace.reverse()

    return step, backtrace

def bfs_light(loc, available_positions, target_loc):
    # breadth-first search
    neighbor = loc
    queue = [loc]
    visited = {}   
    visited[loc] = True
    is_break = False
    path = {}
    while queue and not is_break:
        node = queue.pop(0)
        for neighbor in available_positions[node]:
            if not visited.has_key(neighbor):
                path[neighbor] = node
                visited[neighbor] = True
                if target_loc.has_key(neighbor):
                    is_break = True
                    #print neighbor
                queue.append(neighbor)
            if is_break: 
                break    

    if not is_break:
        step = None
    else:
        step = 0
        node = neighbor
        while node != loc:
            step += 1
            neighbor = node
            node = path[neighbor]

    return step

def spwi(loc, available_positions, target_loc):
    # breadth-first search
    target_loc_has_key = target_loc.has_key 
    if target_loc_has_key(loc): return 0

    queue = [loc]
    visited = visited_template.copy()
    visited[loc] = True
    is_break = False

    step = 0
    while queue and not is_break:
        step += 1
        subqueue = []
        subqueue_append = subqueue.append
        for node in queue:
            for neighbor in available_positions[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    subqueue_append(neighbor)
                    if target_loc_has_key(neighbor):
                        is_break = True
                        break
            if is_break: break
        queue = subqueue

    if not is_break: step = inf

    return step

def improved_dijkstra(loc, available_positions, target_loc):
    # dijkstra algorithm
    target_loc_has_key = target_loc.has_key 
    if target_loc_has_key(loc): return 0

    distances = distances_template.copy()
    distances_has_key = distances.has_key
    queue = [(0, loc)]   
    visited = visited_template.copy()
    visited[loc] = True
    is_break = False   
 
    step = 0
    while queue and not is_break:
        step += 1
        subqueue = []
        subqueue_append = subqueue.append
        for (dummy, node) in queue:
            for neighbor in available_positions[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    if distances_has_key(neighbor):
                        distance = min(distances[neighbor], distances[node] + 1)
                    else:
                        distance = distances[node] + 1
                    distances[neighbor] = distance
                    estimation = (distance, neighbor)
                    subqueue.append(estimation)  
                    if target_loc_has_key(neighbor):
                        is_break = True
                        break
            if is_break: break
        queue = subqueue
        queue = sorted(queue)

    if not is_break: step = inf

    return step

def bfs_side(loc, available_positions, player):
    # player-oriented
    axis = player['axis']
    line = player['line']
    # breadth-first search
    neighbor = loc
    queue = [loc]
    visited = {}   
    visited[loc] = True
    is_break = False
    path = {}
    while queue and not is_break:
        node = queue.pop(0)
        for neighbor in available_positions[node]:
            if not visited.has_key(neighbor):
                path[neighbor] = node
                visited[neighbor] = True
                if neighbor[axis] == line:
                    is_break = True
                    #print neighbor
                queue.append(neighbor)
            if is_break: 
                break    

    if not is_break:
        step = None
    else:
        step = 0
        node = neighbor
        while node != loc:
            step += 1
            neighbor = node
            node = path[neighbor]

    return step

def dijkstra(loc, available_positions, target_loc):
    # dijkstra algorithm
    neighbor = loc
    distances = {loc: 0} 
    queue = [(0, loc)]   
    visited = {}
    is_break = False
    while queue and not is_break:
        (dummy, node) = queue.pop(0)
        for neighbor in available_positions[node]:
            if not visited.has_key(neighbor):
                visited[neighbor] = True
                if distances.has_key(neighbor):
                    distance = min(distances[neighbor], distances[node] + 1)
                else:
                    distance = distances[node] + 1
                distances[neighbor] = distance
                estimation = (distance, neighbor)
                queue.append(estimation)               
                if neighbor in target_loc:
                    is_break = True
                    break

        queue = sorted(queue)

    if is_break:
        step = distances[node]
    else:
        step = None

    return step

def trace2places(trace):
    places = []
    offsets = ((0, 0), (1, 0), (0, 1), (1, 1))
    for location in trace:
        (col, row) = location
        for offset in offsets:
            (offset_col, offset_row) = offset
            (place_col, place_row) = (col + offset_col, row + offset_row)
            place = (place_col, place_row)
            if ((0 < place_col < width) and 
                (0 < place_row < height) and
                place not in places):
                places.append(place)
    return places

def alpha_beta_pruning(alpha, beta, value, owner):
    pruning = False
    if DEBUG:
        print "alpha-beta pruning"
        print "alpha:", alpha
        print "beta:", beta
        print "value:", value   
    if owner == 'max' and alpha != None:
        if value >= alpha:
            if DEBUG: 
                print "alpha pruning node"
                print "alpha:", alpha
                print "value:", value
            pruning = True
    if owner == 'min' and beta != None:
        if -value < beta:
            if DEBUG: 
                print "beta pruning node"
                print "beta:", beta
                print "value:", value
            pruning = True        
    return pruning

def action_choice(action_list):
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
        action = random.choice(equal_actions_list)
    else:
        action = {'action_type': None}
    #print action
    return action

def action_choice_greedy(action_list):
    # action select
    maximal_movement_cost = None
    maximal_building_cost = None
    equal_movement_actions_list = []
    equal_building_actions_list = []
    for action in action_list:
        if action['action_type'] == 'movement':
            if action['cost'] > maximal_movement_cost:
                equal_movement_actions_list = []
                maximal_movement_cost = action['cost']
                equal_movement_actions_list.append(action)
            elif action['cost'] == maximal_movement_cost:
                equal_movement_actions_list.append(action)
        elif action['action_type'] == 'building':
            if action['cost'] > maximal_building_cost:
                equal_building_actions_list = []
                maximal_building_cost = action['cost']
                equal_building_actions_list.append(action)
            elif action['cost'] == maximal_building_cost:
                equal_building_actions_list.append(action)
    #print maximal_movement_cost
    #print maximal_building_cost

    if maximal_movement_cost >= maximal_building_cost:
        variants = len(equal_movement_actions_list)
        if variants != 0:
            action = random.choice(equal_movement_actions_list)
        else:
            action = {'action_type': None}
    else:
        variants = len(equal_building_actions_list)
        if variants != 0:
            action = random.choice(equal_building_actions_list)
        else:
            action = {'action_type': None}      
    #print action
    return action
