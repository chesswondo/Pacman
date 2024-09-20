import pygame
import time
import random
from maze_generator import Maze
from characters import Pacman, Dot, Ghost
from utils import *

def run_pacman_game(screen_width: int,
                    screen_height: int,
                    map_width: int,
                    map_height: int,
                    move_delay: int,
                ):
    
    # Initialize Pygame
    pygame.init()

    # Set up screen parameters
    screen = pygame.display.set_mode((screen_width, screen_height))
    field_size = (screen_width//map_width, screen_height//map_height)
    x_scaling = screen_width//map_width
    y_scaling = screen_height//map_height

    # Maze generation
    wall_density = 0.3  # 30% of the maze will be walls
    maze = Maze(map_width, map_height, wall_density)
    grid = maze.generate_maze()

    # Characters initialization
    pacman = Pacman(grid, field_size, map_width, map_height, "images/pacman.png")
    pacman_image = pacman.image
    dot = Dot(grid, field_size, map_width, map_height, "images/dot.png")
    dot_image = dot.image

    ghost_images = ["images/ghost_red.png", "images/ghost_blue.png", "images/ghost_green.png", "images/ghost_yellow.png"]
    ghost_image = random.choice(ghost_images)

    ghost = Ghost(grid, field_size, map_width, map_height, ghost_image)
    ghost_image = ghost.image

    # Set the title and icon
    pygame.display.set_caption("Pac-Man")
    icon = pygame.image.load("images/pacman_icon.png")
    pygame.display.set_icon(icon)

    # Load the wall images
    wall_image = pygame.image.load("images/wall.jpg")
    wall_image = pygame.transform.scale(wall_image, field_size)

    # Set up the game variables
    running = True
    score = 0
    
    ghosts = [ghost]

    # Main game loop
    while running:
        keys = pygame.key.get_pressed()
        # Check for pacman input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Pacman behaviour
        if keys[pygame.K_LEFT]:
            pacman.make_move(command='left')
        elif keys[pygame.K_RIGHT]:
            pacman.make_move(command='right')
        elif keys[pygame.K_UP]:
            pacman.make_move(command='up')
        elif keys[pygame.K_DOWN]:
            pacman.make_move(command='down')
        
        # Update game state
        if abs(pacman.x - dot.x) < 0.5 and abs(pacman.y - dot.y) < 0.5:
            score += 1
            dot = Dot(grid, field_size, map_width, map_height, "images/dot.png")
            while(True):
                new_ghost = Ghost(grid, field_size, map_width, map_height, random.choice(ghost_images))
                if min(abs(new_ghost.x-pacman.x), abs(new_ghost.y-pacman.y)) > 5:
                    ghosts.append(new_ghost)
                    break
        
        # Ghost behaviour
        screen.fill((0, 0, 0))
        for ghost_id, ghost in enumerate(ghosts):

            screen.blit(ghost.image, (ghost.x*x_scaling, ghost.y*y_scaling))
            if abs(pacman.x - ghost.x) < 0.5 and abs(pacman.y - ghost.y) < 0.5:
                pygame.quit()

            ghosts[ghost_id].make_move(pacman.x, pacman.y)

        # Draw game
        screen.blit(pacman_image, (pacman.x*x_scaling, pacman.y*y_scaling))
        screen.blit(dot_image, (dot.x*x_scaling, dot.y*y_scaling))
        for field_x in range(grid.shape[0]):
            for field_y in range(grid.shape[1]):
                if grid[field_x][field_y] == 1:
                    screen.blit(wall_image, (field_x*x_scaling, field_y*y_scaling))

        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(text, (10, 10))
        pygame.display.flip()
        time.sleep(move_delay)

    # Quit Pygame
    pygame.quit()


def main():
    run_pacman_game(screen_width=800,
                    screen_height=600,
                    map_width=40,
                    map_height=30,
                    move_delay=0.15,
                )
    

if __name__ == "__main__":
    main()