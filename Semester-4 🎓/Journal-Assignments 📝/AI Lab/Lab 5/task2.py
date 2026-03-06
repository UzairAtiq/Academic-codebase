from collections import deque

# The maze grid - 0 means you can walk here, 1 means its a wall
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

# Where the robot starts and where it needs to go
startNode = (0, 0)  # top left corner
goalNode = (7, 7)   # bottom right corner
rows = 8
cols = 8


def displayMaze():
    # Just prints the maze so we can see it nicely in the terminal
    print("\n=== MAZE REPRESENTATION ===")
    print("\nMaze Grid (0 = Free, 1 = Wall, S = Start, G = Goal):\n")

    # Print the column numbers across the top (C0, C1, C2...)
    print("    ", end="")
    for c in range(cols):
        print(f"C{c}  ", end="")
    print()

    # Go through each row one by one
    for r in range(rows):
        print(f"R{r}  ", end="")  # print the row number on the left side

        # Go through each cell in this row
        for c in range(cols):
            if (r, c) == startNode:
                print("S   ", end="")   # mark the starting position
            elif (r, c) == goalNode:
                print("G   ", end="")   # mark the goal position
            else:
                print(f"{maze[r][c]}   ", end="")  # print 0 or 1 normally
        print()  # move to next line after finishing a row

    print(f"\nStart Node: {startNode}")
    print(f"Goal Node: {goalNode}")


def getNeighbors(row, col):
    # Given a cell, this finds all the cells you can actually move to from here
    neighbors = []

    # These are the 4 directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        # Calculate where we'd end up if we moved in this direction
        newRow = row + dr
        newCol = col + dc

        # Make sure we're not going outside the maze AND not hitting a wall
        if 0 <= newRow < rows and 0 <= newCol < cols and maze[newRow][newCol] == 0:
            neighbors.append((newRow, newCol))  # this neighbor is valid, add it

    return neighbors


def bfs():
    # This is the main search - finds the shortest path from start to goal

    queue = deque([startNode])      # to-do list, we start by adding the start node
    visited = {startNode}           # keeps track of cells we already checked
    parent = {startNode: None}      # remembers how we got to each cell (for tracing path later)
    nodesExplored = []              # just for recording the order we visited things

    # Keep going as long as there are cells left to explore
    while queue:
        currentNode = queue.popleft()       # grab the next cell from the front of the line
        nodesExplored.append(currentNode)   # record that we visited this one

        # Check if we finally reached the goal
        if currentNode == goalNode:

            # We made it! Now trace back how we got here
            path = []
            node = goalNode

            # Walk backwards from goal to start using the parent map
            while node is not None:
                path.append(node)
                node = parent[node]  # jump to the cell that led us here

            path.reverse()  # flip it so it reads start -> goal instead of goal -> start

            # Return everything the caller might want to know
            return {
                'pathFound': True,
                'path': path,
                'nodesExplored': nodesExplored,
                'pathLength': len(path),
                'totalNodesExplored': len(nodesExplored)
            }

        # Not at goal yet, so look at all cells we can move to from here
        row, col = currentNode
        neighbors = getNeighbors(row, col)

        for neighbor in neighbors:
            # Only add this neighbor if we havent been there before
            if neighbor not in visited:
                visited.add(neighbor)               # mark it as seen right away
                parent[neighbor] = currentNode      # remember we came from currentNode
                queue.append(neighbor)              # add to the back of the to-do list

    # If we get here, the queue ran out and we never found the goal
    return {
        'pathFound': False,
        'path': [],
        'nodesExplored': nodesExplored,
        'pathLength': 0,
        'totalNodesExplored': len(nodesExplored)
    }


def displayResults(result):
    # Prints out everything we found after running BFS
    print("\n\n=== BFS RESULTS ===\n")

    if result['pathFound']:
        print(f"Path Found: YES")
        print(f"Path Length: {result['pathLength']}")
        print(f"Total Nodes Explored: {result['totalNodesExplored']}")

        # Print the path with arrows between each step
        print(f"\nPath: ", end="")
        for i, node in enumerate(result['path']):
            if i < len(result['path']) - 1:
                print(f"{node} -> ", end="")  # arrow after every node except the last
            else:
                print(f"{node}")              # no arrow after the final node

        # Print every single node we visited and in what order
        print(f"\nNodes Explored (in order):")
        for i, node in enumerate(result['nodesExplored']):
            print(f"{i+1}. {node}")

        # Summary table info
        print("\n\n=== BFS TABLE ENTRIES ===")
        print(f"Algorithm: Breadth-First Search (BFS)")
        print(f"Path Found: Yes")
        print(f"Path Length: {result['pathLength']}")
        print(f"Nodes Explored: {result['totalNodesExplored']}")
        print(f"Solution Path: {' -> '.join([str(node) for node in result['path']])}")

    else:
        # No path exists between start and goal
        print("Path Found: NO")
        print(f"Total Nodes Explored: {result['totalNodesExplored']}")


def main():
    # Step 1: show the maze
    displayMaze()

    # Step 2: run BFS to find the path
    result = bfs()

    # Step 3: print what we found
    displayResults(result)


# This just means - only run main() if we're running this file directly
if __name__ == "__main__":
    main()