from collections import deque

maze = [
    [0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 1, 0]
]

startNode = (0, 0)
goalNode = (7, 7)
rows = 8
cols = 8

def displayMaze():
    print("\n=== MAZE REPRESENTATION ===")
    print("\nMaze Grid (0 = Free, 1 = Wall, S = Start, G = Goal):\n")
    print("    ", end="")
    for c in range(cols):
        print(f"C{c}  ", end="")
    print()
    
    for r in range(rows):
        print(f"R{r}  ", end="")
        for c in range(cols):
            if (r, c) == startNode:
                print("S   ", end="")
            elif (r, c) == goalNode:
                print("G   ", end="")
            else:
                print(f"{maze[r][c]}   ", end="")
        print()
    
    print(f"\nStart Node: {startNode}")
    print(f"Goal Node: {goalNode}")

def getNeighbors(row, col):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        newRow = row + dr
        newCol = col + dc
        
        if 0 <= newRow < rows and 0 <= newCol < cols and maze[newRow][newCol] == 0:
            neighbors.append((newRow, newCol))
    
    return neighbors

def bfs():
    queue = deque([startNode])
    visited = {startNode}
    parent = {startNode: None}
    nodesExplored = []
    
    while queue:
        currentNode = queue.popleft()
        nodesExplored.append(currentNode)
        
        if currentNode == goalNode:
            path = []
            node = goalNode
            while node is not None:
                path.append(node)
                node = parent[node]
            path.reverse()
            
            return {
                'pathFound': True,
                'path': path,
                'nodesExplored': nodesExplored,
                'pathLength': len(path),
                'totalNodesExplored': len(nodesExplored)
            }
        
        row, col = currentNode
        neighbors = getNeighbors(row, col)
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = currentNode
                queue.append(neighbor)
    
    return {
        'pathFound': False,
        'path': [],
        'nodesExplored': nodesExplored,
        'pathLength': 0,
        'totalNodesExplored': len(nodesExplored)
    }

def displayResults(result):
    print("\n\n=== BFS RESULTS ===\n")
    
    if result['pathFound']:
        print(f"Path Found: YES")
        print(f"Path Length: {result['pathLength']}")
        print(f"Total Nodes Explored: {result['totalNodesExplored']}")
        
        print(f"\nPath: ", end="")
        for i, node in enumerate(result['path']):
            if i < len(result['path']) - 1:
                print(f"{node} -> ", end="")
            else:
                print(f"{node}")
        
        print(f"\nNodes Explored (in order):")
        for i, node in enumerate(result['nodesExplored']):
            print(f"{i+1}. {node}")
        
        print("\n\n=== BFS TABLE ENTRIES ===")
        print(f"Algorithm: Breadth-First Search (BFS)")
        print(f"Path Found: Yes")
        print(f"Path Length: {result['pathLength']}")
        print(f"Nodes Explored: {result['totalNodesExplored']}")
        print(f"Solution Path: {' -> '.join([str(node) for node in result['path']])}")
        
    else:
        print("Path Found: NO")
        print(f"Total Nodes Explored: {result['totalNodesExplored']}")

def main():
    displayMaze()
    result = bfs()
    displayResults(result)

if __name__ == "__main__":
    main()
