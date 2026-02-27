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

#Defining Start and Goal nodes
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

if __name__ == "__main__":
    displayMaze()