#general method of getting the path
def get_path(parent, start, end):
    child = end 
    path = [end]
    if start in parent:
        del parent[start]
    if child in parent:
        while parent[child]:
            if parent[child] in path:
                break
            path.append(parent[child])
            child = parent[child]
            if child not in parent: 
                break
            # avoid the case 'K': 'I', 'I':'K', while loop will be infinite 
            child_parent = parent[child]
            if child_parent in parent:
                if parent[child_parent] == child:
                    if child_parent not in path:
                        path.append(child_parent)
                    break
    if start != path[-1]:
        path.append(start)
    path.reverse()
    return path

def get_distance(start, end):
    distance = ((start[0]-start[1])**2)+((end[0]-end[1])**2)
    return distance

# in this method, could optimal the child list, like put them in order and check the security
def createChild(position, goal, board_width, board_height): 
    childList = {}
    # all these check should be covered by method isSafe(), we don't need the board_width and board_height
    # right now just write like this for testing

    if position[0] - 1 < board_width and position[0] - 1 >= 0: 
        left = (position[0] - 1, position[1])
        childList[left] = get_distance(left, goal) # add left direction

    if position[1] - 1 < board_height and position[1] - 1 >= 0: 
        down = (position[0], position[1] - 1)   
        childList[down] = get_distance(down, goal) # add down direction

    if position[0] + 1 < board_width and position[0] + 1 >= 0:
        right = (position[0] + 1, position[1])
        childList[right] = get_distance(right, goal) # add right direction

    if position[1] + 1 < board_height and position[1] + 1 >= 0:  
        up = (position[0], position[1] + 1)     
        childList[up] = get_distance(up, goal) # add up direction

    #sorted_by_value = sorted(childList.items(), key=lambda kv: kv[1])
    #print 'position', position, 'childList', childList.keys()
    return childList.keys()  # [(12, 15), (12, 14), (11, 13), (13, 13)]


def dfs(start_state, goal_state):
    frontier = createChild(start_state, goal_state, 20, 20)
    frontier_size = len(frontier)
    explored = []
    explored.append(start_state)
    parent = {}
    for child in frontier:
        parent[child] = start_state
    path = []
    while frontier:
        node = frontier.pop()
        # frontier_size = frontier_size - 1
        explored.append(node)
        if node == goal_state:
            path = get_path(parent, start_state, goal_state)
            return ("path", path)
        child_list = createChild(node, goal_state, 20, 20)  #the neighbors of the current position          
        # for child in child_list:
        #     if child not in explored and child not in frontier:
        #         parent[child] = node
        frontier.extend(child for child in child_list if child not in explored and child not in frontier)
        # frontier_size = frontier_size + 1
        #print 'explored', explored
        #print 'frontier', frontier
    return None

print(dfs((12, 7), (16, 5))) # notice here we are using tuples, as dictionary cannot hash list

DFS(current_pos, goal_state):
    x = current_pos[0]
    y = current_pos[1]
    childrenStates = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]
    for child in childrenStates: 
        if dfs_solution(child, goal_state):
            return child
    return null

dfs_solution(current_pos, goal_state):
    frontier = createChild(start_state, goal_state, 20, 20)
    explored = []
    explored.append(start_state)
    while frontier:
        node = frontier.pop()
        explored.append(node)
        if node == goal_state:
            return true
        child_list = createChild(node, goal_state, 20, 20)
        frontier.extend(child for child in child_list if child not in explored and child not in frontier)
    return false


