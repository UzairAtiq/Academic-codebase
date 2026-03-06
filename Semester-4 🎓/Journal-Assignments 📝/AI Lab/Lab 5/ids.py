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

def dls(limit):
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
            return path, explored
        if depth < limit:
            for neighbor in getNeighbors(cell[0], cell[1]):
                if neighbor not in visited:
                    parent[neighbor] = cell
                    stack.append((neighbor, depth + 1))
    return None, explored

displayMaze()

# --- DLS with limit too small ---
print("\n===== DLS (limit = 5) =====")
path, explored = dls(limit=5)
print(f"  Path Found    : {'YES' if path else 'NO'}")
print(f"  Path Length   : {len(path) if path else 'N/A'}")
print(f"  Nodes Explored: {len(explored)}")
if path:
    print(f"\n--- Path ---")
    print(" -> ".join(str(c) for c in path))
print(f"\n--- Traversal Order ---")
for i, cell in enumerate(explored):
    print(f"  {i+1}. {cell}")

# --- DLS with enough limit ---
print("\n===== DLS (limit = 20) =====")
path, explored = dls(limit=20)
print(f"  Path Found    : {'YES' if path else 'NO'}")
print(f"  Path Length   : {len(path) if path else 'N/A'}")
print(f"  Nodes Explored: {len(explored)}")
print(f"\n--- Path ---")
print(" -> ".join(str(c) for c in path))
print(f"\n--- Traversal Order ---")
for i, cell in enumerate(explored):
    print(f"  {i+1}. {cell}")

print("\n========== DLS TABLE ==========")
print(f"  Algorithm      : DLS")
print(f"  Limit = 5      : No Path Found")
print(f"  Limit = 20     : Path Found - Length {len(path)}")
print(f"  Nodes Explored : {len(explored)}")
print("================================")