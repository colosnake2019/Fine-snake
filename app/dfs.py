
from collections import OrderedDict


# 0/5: safe 1:danger
def isSafe(x, y, board):
    if y<0 or y>(len(board)-1):
        return False
    if x<0 or x>(len(board[0])-1):
        return False
    return board[y][x] == 0 or board[y][x] == 5;

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

# calculate the distance between two points
def get_distance(start, end):
    distance = ((start[0]-start[1])**2)+((end[0]-end[1])**2)
    return distance

# in this method, could optimal the child list, like put them in order and check the security
def createChild(position, goal, board): 
    childList = {}
    # all these check should be covered by method isSafe(), we don't need the board_width and board_height
    # right now just write like this for testing
    x = position[0]
    y = position[1]

    if isSafe(x-1, y, board):
        next = (x-1,y)
        childList[get_distance(next, goal)] = next
    if isSafe(x+1, y, board):
        next = (x+1,y)
        childList[get_distance(next, goal)] = next
    if isSafe(x, y-1, board):
        next = (x,y-1)
        childList[get_distance(next, goal)] = next
    if isSafe(x, y+1, board):
        next = (x,y+1)
        childList[get_distance(next, goal)] = next

    sorted_children = OrderedDict(sorted(childList.items()))

    # return sorted_children.values()  # [(12, 15), (12, 14), (11, 13), (13, 13)]
    return sorted_children.values()

def DFS(current_pos, goal_state, board):
    x = current_pos[0]
    y = current_pos[1]
    childrenStates = createChild((x,y), goal_state, board)
    print 'in DFS, DFS is ', childrenStates
    for child in childrenStates: 
        if dfs_solution(child, goal_state, board):
            return child
    return childrenStates[0]

def dfs_solution(current_pos, goal_state, board):
    frontier = createChild(current_pos, goal_state, board)
    explored = []
    explored.append(current_pos)
    while frontier:
        node = frontier.pop()
        explored.append(node)
        if node == goal_state:
            return True
        child_list = createChild(node, goal_state, board)
        frontier.extend(child for child in child_list if child not in explored and child not in frontier)
    return False


