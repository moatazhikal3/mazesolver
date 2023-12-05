# maze_solver_backend.py
import numpy as np #logical computations for generation of maze
import random
from queue import PriorityQueue

#building of random maze, each run of 'generate maze' is a new list of vertices
def generate_maze_iterative(width, height):
    maze = np.zeros((height, width), dtype=np.int8)
    #left, right
    DX = [0, 1, 0, -1]
    #up, down
    DY = [-1, 0, 1, 0]
    stack = [(1, 1)]

    #carving out the maze using depth first search
    maze[1:-1, 1:-1] = 0
    while stack:
        x, y = stack.pop()

        #checking if the current cell has unvisited neighbors
        if any(0 <= x + 2*DX[i] < width and 0 <= y + 2*DY[i] < height and maze[y + 2*DY[i], x + 2*DX[i]] == 0 for i in range(4)):
            stack.append((x, y))

            #all unvisited neighbors
            neighbors = [(DX[i], DY[i]) for i in range(4) if 0 <= x + 2*DX[i] < width and 0 <= y + 2*DY[i] < height and maze[y + 2*DY[i], x + 2*DX[i]] == 0]

            #select a cell space neighbor to visit using random
            DX_i, DY_i = random.choice(neighbors)
            
            #carve the path to the selected neighbor
            maze[y + DY_i, x + DX_i] = 1
            maze[y + 2*DY_i, x + 2*DX_i] = 1
            
            #add a new cell to the stack to become white cell
            stack.append((x + 2*DX_i, y + 2*DY_i))

    #starting point and the end point
    maze[0, 1] = 1
    maze[height - 1, width - 2] = 1
    #printing the maze on the console
    print(maze)
    return maze
#dijkstra algorithm, find the shortest path through the carved maze.
def dijkstra(maze, start, end):
    #directions that the d algorithm has to take
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    height, width = maze.shape

    #initializing the visited and distance matrix
    visited = [[False] * width for _ in range(height)]
    distance = [[float('inf')] * width for _ in range(height)]
    distance[start[1]][start[0]] = 0
    #total steps taken in maze in list
    all_steps = []

    #exploring the nodes
    pq = PriorityQueue()
    pq.put((0, start))

    #adding to the queues
    while not pq.empty():
        dist, (x, y) = pq.get()
        visited[y][x] = True
        all_steps.append((x, y))

        #if at end, it will stop
        if (x, y) == end:
            break
            
        #exploring the neighbors until reaches end
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx] and maze[ny][nx] == 1:
                new_dist = dist + 1
                if new_dist < distance[ny][nx]:
                    distance[ny][nx] = new_dist
                    pq.put((new_dist, (nx, ny)))
                    
    #once it reaches the end, it will traverse to find the shortest path
    path = []
    if distance[end[1]][end[0]] != float('inf'):
        x, y = end
        while (x, y) != start:
            path.append((x, y))
            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]
                if 0 <= nx < width and 0 <= ny < height and distance[ny][nx] == distance[y][x] - 1:
                    x, y = nx, ny
                    break
        path.append(start)
        path.reverse()
        
    #return the path
    return path, all_steps
    
#heuristic for a_star calculating value/cost of cells from destination
#estimated shortest path of each node from the start to the end
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
#a_star algorithm
def a_star(maze, start, end):
    #direction of movement
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    height, width = maze.shape
    #initializing the visited and distance matrix
    visited = [[False] * width for _ in range(height)]
    distance = [[float('inf')] * width for _ in range(height)]
    distance[start[1]][start[0]] = 0
    all_steps = []

    pq = PriorityQueue()
    pq.put((0, start))
    
    #exploring the nodes
    while not pq.empty():
        _, (x, y) = pq.get()
        visited[y][x] = True
        all_steps.append((x, y))

        if (x, y) == end:
            break
            
        #exploring unvisited neighbors
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx] and maze[ny][nx] == 1:
                new_dist = distance[y][x] + 1
                if new_dist < distance[ny][nx]:
                    distance[ny][nx] = new_dist
                     #using heuristic here to put priority on a node
                    priority = new_dist + heuristic((nx, ny), end)
                    pq.put((priority, (nx, ny)))
                    
    #traverseing through to store the shortest path
    path = []
    if distance[end[1]][end[0]] != float('inf'):
        x, y = end
        while (x, y) != start:
            path.append((x, y))
            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]
                if 0 <= nx < width and 0 <= ny < height and distance[ny][nx] == distance[y][x] - 1:
                    x, y = nx, ny
                    break
        path.append(start)
        path.reverse()

    return path, all_steps
