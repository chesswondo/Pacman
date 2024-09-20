import random
import numpy as np

# Directions for moving in the grid: right, down, left, up
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class Maze:
    def __init__(self, rows, cols, wall_density=0.3):
        self.rows = rows
        self.cols = cols
        self.wall_density = wall_density
        # Start with a grid full of walls
        self.grid = [[1 for _ in range(cols)] for _ in range(rows)]

        # Mark the start point (could be randomized)
        self.start = (0, 0)
        self.grid[self.start[0]][self.start[1]] = 0
    
    def is_within_bounds(self, r, c):
        """ Check if the (r, c) coordinate is within grid bounds. """
        return 0 <= r < self.rows and 0 <= c < self.cols
    
    def get_neighbors(self, r, c):
        """ Get valid neighbors (within bounds) of a cell (r, c). """
        neighbors = []
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if self.is_within_bounds(nr, nc):
                neighbors.append((nr, nc))
        return neighbors
    
    def dfs(self, r, c, visited):
        """ Depth-First Search to mark visited cells and ensure connectivity. """
        visited.add((r, c))
        # Shuffle directions to make maze more random
        neighbors = self.get_neighbors(r, c)
        random.shuffle(neighbors)
        
        for nr, nc in neighbors:
            if (nr, nc) not in visited and self.grid[nr][nc] == 0:
                self.dfs(nr, nc, visited)
    
    def is_fully_connected(self):
        """ Ensure all open cells are reachable using DFS from the start. """
        visited = set()
        self.dfs(self.start[0], self.start[1], visited)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 0 and (r, c) not in visited:
                    return False
        return True
    
    def generate_maze(self):
        """ Generate the maze by removing walls and ensuring connectivity. """
        total_cells = self.rows * self.cols
        target_open_cells = int(total_cells * (1 - self.wall_density))
        open_count = 1  # The start point is already open
        open_list = [(0, 0)]
        
        while open_count < target_open_cells:
            if not open_list:
                # If the list of open cells is empty, add a new random cell to keep progressing
                open_list.append((random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)))
                
            r, c = open_list.pop()
            
            if self.grid[r][c] == 0:
                continue
            
            # Make this cell an open space
            self.grid[r][c] = 0
            open_count += 1
            
            # Get neighbors and try to open more paths
            neighbors = self.get_neighbors(r, c)
            random.shuffle(neighbors)
            
            for nr, nc in neighbors:
                if self.grid[nr][nc] == 1:
                    # Open path with a certain probability
                    if random.random() > 0.3:
                        open_list.append((nr, nc))
        
        # Ensure the maze is fully connected
        while not self.is_fully_connected():
            # Randomly remove walls to connect isolated areas
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r][c] == 1:
                        neighbors = self.get_neighbors(r, c)
                        open_neighbors = [n for n in neighbors if self.grid[n[0]][n[1]] == 0]
                        # Remove a wall if it connects two open areas
                        if len(open_neighbors) >= 2:
                            self.grid[r][c] = 0

        return np.array(self.grid)

    def display(self):
        """ Display the maze in the console. """
        for row in self.grid:
            print("".join(["█" if cell == 1 else " " for cell in row]))
