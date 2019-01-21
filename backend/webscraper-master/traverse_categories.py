
def traverse(data):
    if 'children' not in data.keys():
        return 1
    
    total_nodes = 0
    for child in data['children']:
        total_nodes += traverse(child)

    return total_nodes