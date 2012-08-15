DEBUG = False

def adjacency_list_generator():
    #adjacency_list
    adjacency_list = {}
    ij_list = [(i, j) for i in range(width) for j in range(height)]
    for (i, j) in ij_list:
        link_list = []
        for direction in DIRECTIONS:
            (dx, dy) = DIRECTIONS[direction]
            dyj = dy + j
            dxi = dx + i
            if (dyj >= 0) & (dyj < height) & (dxi >= 0) & (dxi < width): 
                link_list.append((dxi, dyj))
        adjacency_list[(i, j)] = set(link_list)    

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
                available_positions[a_loc] = set([])
    #print available_positions[loc]
    return available_positions

def w2p(wall_list):
    #print wall_list
    ij_list = ((i, j) for i in range(1, width) for j in range(1, height))
    p = dict([(ij, set(['horizontal', 'vertical'])) for ij in ij_list])

    for wall in wall_list:
        (x, y) = wall['location']
        p[(x, y)] = set([])
        if wall['type'] == 'horizontal':
            for direction in ('w', 'e'):
                (dx, dy) = DIRECTIONS[direction]
                location = (x + dx, y + dy)
                if p.has_key(location):
                    p[location].difference_update(set(['horizontal']))
        elif wall['type'] == 'vertical':
            for direction in ('n', 's'):
                (dx, dy) = DIRECTIONS[direction]
                location = (x + dx, y + dy)
                if p.has_key(location):
                    p[location].difference_update(set(['vertical']))
        else:
            pass
    #print p
    return p

def bfs(loc, available_positions, target_loc):
    # breadth-first search
    neighbor = loc
    queue = [loc]   
    visited = {loc: True}
    is_break = False
    path = {}
    while (queue != []) and not is_break:
        node = queue.pop(0)
        for neighbor in available_positions[node]:
            if not visited.has_key(neighbor):
                path[neighbor] = node
                visited[neighbor] = True
                if neighbor in target_loc:
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
    #backtrace.reverse()

    return step, backtrace

def bfs_light(loc, available_positions, target_loc):
    # breadth-first search
    neighbor = loc
    queue = [loc]   
    visited = {loc: True}
    is_break = False
    path = {}
    while (queue != []) and not is_break:
        node = queue.pop(0)
        for neighbor in available_positions[node]:
            if not visited.has_key(neighbor):
                path[neighbor] = node
                visited[neighbor] = True
                if neighbor in target_loc:
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
    while (node != loc) and is_break:
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
    while (queue != []) and (not is_break):
        (dummy, node) = queue.pop(0)
        for neighbor in available_positions[node]:
            if not (visited.has_key(neighbor)):
                if distances.has_key(neighbor):
                    distance = min(distances[neighbor], distances[node] + 1)
                else:
                    distance = distances[node] + 1
                distances[neighbor] = distance
                estimation = (distance, neighbor)
                if estimation not in queue:
                    queue.append(estimation)               
        visited[node] = True
        if node in target_loc:
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
            if (place_col > 0) and (place_col < width) and\
                (place_row > 0) and (place_row < height) and\
                place not in places:
                places.append(place)
    return places

def alpha_beta_pruning(alpha, beta, value, owner):
    pruning = False
    if DEBUG:
        print "alpha-beta pruning"
        print "alpha:", alpha
        print "beta:", beta
        print "value:", value   
    if (owner == 'max' and alpha != None):
        if (value >= alpha):
            if DEBUG: 
                print "alpha pruning node"
                print "alpha:", alpha
                print "value:", value
            pruning = True
    if (owner == 'min' and beta != None):
        if (- value < beta):
            if DEBUG: 
                print "beta pruning node"
                print "beta:", beta
                print "value:", value
            pruning = True        
    return pruning
