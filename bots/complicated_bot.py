from algorithms import *
import random

def turn(player, player_list, wall_list, available_positions, adjacency_list):
    loc = player['location']
    target_loc = player['target_loc']
    #opponent_list
    opponent_list = [item for item in player_list if item != player]
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
    for opponent in opponent_list:
        #print opponent
        opponent_available_positions =\
            available_positions_generator(opponent['location'], 
                                          wall_list, 
                                          player_list, 
                                          adjacency_list)
        step = dijkstra(opponent['location'], 
                            opponent_available_positions, 
                            opponent['target_loc'])
        #print step
        distances.append(step)
    distance = min(distances)
    #print distance
    for neighbor in neighbors:
        step = dijkstra(neighbor, available_positions, target_loc)
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
    if intersection != set([]):
        location = list(intersection)[0]
        value = width * height
        action = {'action_type': 'movement', 'location': location, 'cost': value}
        action_list.append(action)            
    # building
    if player['amount_of_walls'] > 0:
        for i in range(1, width):
            for j in range(1, height):
                location = (i, j)
                if p[location] != set([]):           
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
                            step = dijkstra(opponent['location'], 
                                                projected_available_positions, 
                                                opponent['target_loc'])
                            distances.append(step)
                        distance = min(distances)
                        #tic = time.time()
                        projected_available_positions =\
                            available_positions_generator(loc, 
                                                          projected_wall_list,
                                                          player_list,
                                                          adjacency_list)
                        #toc = time.time()
                        #print 'gen', toc - tic
                        #tic = time.time()
                        step = dijkstra(loc, 
                                            projected_available_positions, 
                                            target_loc)
                        #toc = time.time()
                        #print 'bfs', toc - tic
                        if (step != None) and (distance != None):
                            value = distance - step
                            action = {'action_type': 'building', 'wall': wall, 'cost': value}
                            #print action  
                            action_list.append(action)            
        #print action_list
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
    if action['action_type'] == 'movement':
        (x, y) = action['location']
        player['location'] = (x, y)
    elif action['action_type'] == 'building':
        wall_list.append(action['wall'])
        player['amount_of_walls'] -= 1   
    else:
        pass
