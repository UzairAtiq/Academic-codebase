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
    print("==========================")

def getNeighbors(r, c):
    result = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < 8 and 0 <= nc < 8 and maze[nr][nc] == 0:
            result.append((nr, nc))
    return result

def ids():
    total_explored = []

    for limit in range(100):
        print(f"  Trying depth limit: {limit}")
        stack    = [(start, 0)]
        visited  = set()
        parent   = {start: None}
        explored = []

        while stack:
            cell, depth = stack.pop()
            if cell in visited:
                continue
            visited.add(cell)
            explored.append(cell)
            if cell == goal:
                path = []
                while cell is not None:
                    path.append(cell)
                    cell = parent[cell]
                path.reverse()
                total_explored += explored
                return path, total_explored, limit
            if depth < limit:
                for neighbor in getNeighbors(cell[0], cell[1]):
                    if neighbor not in visited:
                        parent[neighbor] = cell
                        stack.append((neighbor, depth + 1))
        total_explored += explored

    return None, total_explored, -1

displayMaze()
path, explored, depth_used = ids()

print("\n========== IDS RESULTS ==========")
print(f"  Path Found    : YES")
print(f"  Found at Depth: {depth_used}")
print(f"  Path Length   : {len(path)}")
print(f"  Nodes Explored: {len(explored)}")
print(f"\n--- Path ---")
print(" -> ".join(str(c) for c in path))
print(f"\n--- Traversal Order ---")
for i, cell in enumerate(explored):
    print(f"  {i+1}. {cell}")
print("\n========== IDS TABLE ==========")
print(f"  Algorithm      : IDS")
print(f"  Path Found     : Yes")
print(f"  Depth Used     : {depth_used}")
print(f"  Path Length    : {len(path)}")
print(f"  Nodes Explored : {len(explored)}")
print("================================")
