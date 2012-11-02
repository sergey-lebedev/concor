import __builtin__

def keygen(player_list, wall_list):
    first_key = []
    for player in player_list:
        first_key.append((player['id'], player['location']))
    first_key.sort()

    second_key = []
    for wall in wall_list:
        second_key.append((wall['type'], wall['location']))
    second_key.sort()

    key = str((first_key, second_key))
    return key

def init():
    del __builtin__.storage
    __builtin__.storage = {}
    del __builtin__.storage_struct
    __builtin__.storage_struct = {}

def restruct(key):
    # dfs
    #print len(storage)
    #print len(storage_struct)
    new_storage = {}
    new_storage_struct = {}
    stack = []
    stack.append(key)
    while stack != []:
        parent_key = stack.pop()
        if storage_struct.has_key(parent_key):
            new_storage[parent_key] = storage[parent_key]
            new_storage_struct[parent_key] = storage_struct[parent_key]
            for child_key in storage_struct[parent_key]:
                stack.append(child_key)
        elif storage.has_key(parent_key):
            new_storage[parent_key] = storage[parent_key]

    del __builtin__.storage
    __builtin__.storage = new_storage
    del __builtin__.storage_struct
    __builtin__.storage_struct = new_storage_struct
    #print len(storage)
    #print len(storage_struct)
