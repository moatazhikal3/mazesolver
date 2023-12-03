# maze_solver_backend.py
import numpy as np
import random
from queue import PriorityQueue
def generate_maze_iterative(width, height):
    maze = np.zeros((height, width), dtype=np.int8)
    DX = [0, 1, 0, -1]
    DY = [-1, 0, 1, 0]
    stack = [(1, 1)]

    maze[1:-1, 1:-1] = 0
    while stack:
        x, y = stack.pop()
        if any(0 <= x + 2*DX[i] < width and 0 <= y + 2*DY[i] < height and maze[y + 2*DY[i], x + 2*DX[i]] == 0 for i in range(4)):
            stack.append((x, y))
            neighbors = [(DX[i], DY[i]) for i in range(4) if 0 <= x + 2*DX[i] < width and 0 <= y + 2*DY[i] < height and maze[y + 2*DY[i], x + 2*DX[i]] == 0]
            DX_i, DY_i = random.choice(neighbors)
            maze[y + DY_i, x + DX_i] = 1
            maze[y + 2*DY_i, x + 2*DX_i] = 1
            stack.append((x + 2*DX_i, y + 2*DY_i))

    maze[0, 1] = 1
    maze[height - 1, width - 2] = 1
    # Printing the maze on the console
    print(maze)
    return maze

def dijkstra(maze, start, end):
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    height, width = maze.shape
    visited = [[False] * width for _ in range(height)]
    distance = [[float('inf')] * width for _ in range(height)]
    distance[start[1]][start[0]] = 0
    all_steps = []

    pq = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        dist, (x, y) = pq.get()
        visited[y][x] = True
        all_steps.append((x, y))

        if (x, y) == end:
            break

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx] and maze[ny][nx] == 1:
                new_dist = dist + 1
                if new_dist < distance[ny][nx]:
                    distance[ny][nx] = new_dist
                    pq.put((new_dist, (nx, ny)))

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

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(maze, start, end):
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    height, width = maze.shape
    visited = [[False] * width for _ in range(height)]
    distance = [[float('inf')] * width for _ in range(height)]
    distance[start[1]][start[0]] = 0
    all_steps = []

    pq = PriorityQueue()
    pq.put((0, start))

    while not pq.empty():
        _, (x, y) = pq.get()
        visited[y][x] = True
        all_steps.append((x, y))

        if (x, y) == end:
            break

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx] and maze[ny][nx] == 1:
                new_dist = distance[y][x] + 1
                if new_dist < distance[ny][nx]:
                    distance[ny][nx] = new_dist
                    priority = new_dist + heuristic((nx, ny), end)
                    pq.put((priority, (nx, ny)))

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