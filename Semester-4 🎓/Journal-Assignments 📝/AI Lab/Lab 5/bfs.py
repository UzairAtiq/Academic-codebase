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

start = (0, 0)
goal  = (7, 7)

def displayMaze():
    print("\n========== MAZE ==========")
    for r in range(8):
        for c in range(8):
            if   (r,c) == start: print("S", end=" ")
            elif (r,c) == goal:  print("G", end=" ")
            else:                print(maze[r][c], end=" ")
        print()
    print(f"Start: {start}  |  Goal: {goal}")
    print("==========================")

def getNeighbors(r, c):
    result = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < 8 and 0 <= nc < 8 and maze[nr][nc] == 0:
            result.append((nr, nc))
    return result

def bfs():
    queue    = deque([start])
    visited  = {start}
    parent   = {start: None}
    explored = []

    while queue:
        cell = queue.popleft()
        explored.append(cell)

        if cell == goal:
            path = []
            while cell is not None:
                path.append(cell)
                cell = parent[cell]
            path.reverse()
            return path, explored

        for neighbor in getNeighbors(cell[0], cell[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = cell
                queue.append(neighbor)

    return None, explored

# ---- run ----
displayMaze()
path, explored = bfs()

print("\n========== BFS RESULTS ==========")
if path:
    print(f"Path Found    : YES")
    print(f"Path Length   : {len(path)}")
    print(f"Nodes Explored: {len(explored)}")
    print(f"\n--- Path ---")
    print(" -> ".join(str(c) for c in path))
    print(f"\n--- Traversal Order ---")
    for i, cell in enumerate(explored):
        print(f"  {i+1}. {cell}")
else:
    print("Path Found    : NO")
    print(f"Nodes Explored: {len(explored)}")

print("\n========== BFS TABLE ==========")
print(f"  Algorithm      : BFS")
print(f"  Path Found     : {'Yes' if path else 'No'}")
print(f"  Path Length    : {len(path) if path else 'N/A'}")
print(f"  Nodes Explored : {len(explored)}")
print("================================")