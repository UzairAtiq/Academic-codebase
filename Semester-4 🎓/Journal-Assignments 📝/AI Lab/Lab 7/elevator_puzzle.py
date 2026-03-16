from heapq import heappush, heappop

def isSafe(state):
    p, s, v, c = state
    
    if s == v and s != p:
        return False
    
    if c == s and c != p:
        return False
    
    return True

def getSuccessors(state):
    p, s, v, c = state
    successors = []
    target = 15 if p == 0 else 0
    
    nextState = (target, s, v, c)
    if isSafe(nextState):
        successors.append((nextState, "Policeman goes " + ("up" if target == 15 else "down")))
    
    if s == p:
        nextState = (target, target, v, c)
        if isSafe(nextState):
            successors.append((nextState, "Policeman takes Suspect " + ("up" if target == 15 else "down")))
    
    if v == p:
        nextState = (target, s, target, c)
        if isSafe(nextState):
            successors.append((nextState, "Policeman takes Victim " + ("up" if target == 15 else "down")))
    
    if c == p:
        nextState = (target, s, v, target)
        if isSafe(nextState):
            successors.append((nextState, "Policeman takes Case File " + ("up" if target == 15 else "down")))
    
    return successors

def heuristic(state):
    return sum(1 for x in state if x == 0)

def astarSearch():
    start = (0, 0, 0, 0)
    goal = (15, 15, 15, 15)
    
    frontier = [(heuristic(start), 0, start, [])]
    visited = set()
    
    while frontier:
        _, cost, state, path = heappop(frontier)
        
        if state in visited:
            continue
        
        visited.add(state)
        
        if state == goal:
            return path
        
        for nextState, action in getSuccessors(state):
            if nextState not in visited:
                newCost = cost + 1
                priority = newCost + heuristic(nextState)
                heappush(frontier, (priority, newCost, nextState, path + [action]))
    
    return None

def printSolution():
    solution = astarSearch()
    
    if solution:
        print("Solution found in", len(solution), "steps:\n")
        for i, action in enumerate(solution, 1):
            print(f"{i}. {action}")
    else:
        print("No solution found")

printSolution()
