from algorithms import *
import random

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
                (place_row > 0) and (place_row < height):
                if place not in places:
                   places.append(place)
    return places

def turn(player, player_list, wall_list, available_positions, adjacency_list):
    loc = player['location']
    target_loc = player['target_loc']
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
    if intersection:
        location = list(intersection)[0]
        value = width * height
        action = {'action_type': 'movement', 'location': location, 'cost': value}
        action_list.append(action)            
    # building
    if player['amount_of_walls'] > 0:
        places = trace2places(trace)
        for location in places:
            if p[location]:
                for wall_type in p[location]:
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
                        action_list.append(action)            
        #print action_list

    action = action_choice(action_list)

    if action['action_type'] == 'movement':
        (x, y) = action['location']
        player['location'] = (x, y)
    elif action['action_type'] == 'building':
        wall_list.append(action['wall'])
        player['amount_of_walls'] -= 1   
    else:
        pass
