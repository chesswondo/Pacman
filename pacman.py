import pygame
import time
import random
import numpy as np
from maze_generator import Maze
from characters import Pacman, Dot, Ghost, Bonus
from utils import *

def run_pacman_game(screen_width: int,
                    screen_height: int,
                    map_width: int,
                    map_height: int,
                    move_delay: int,
                    wall_density: float,
                    images: dict,
                    fireball_time: int,
                    heart_time: int,
                ):
    
    # Initialize Pygame
    pygame.init()

    # Set up screen parameters
    screen = pygame.display.set_mode((screen_width, screen_height))
    field_size = (screen_width//map_width, screen_height//map_height)
    x_scaling = screen_width//map_width
    y_scaling = screen_height//map_height

    # Maze generation
    grid = None
    while(True):
        try:
            maze = Maze(map_width, map_height, wall_density)
            grid = maze.generate_maze()
        except Exception:
            continue
        if np.sum(grid) > grid.size//10:
            break

    # Characters initialization
    image_folder = images["folder"]
    pacman = Pacman(grid, field_size, map_width, map_height, image_folder+images["pacman"])
    pacman_image = pacman.image
    dot = Dot(grid, field_size, map_width, map_height, image_folder+images["dot"])
    dot_image = dot.image
    fireball = Bonus(grid, field_size, map_width, map_height, image_folder+images["fireball"])
    fireball.x, fireball.y = -1, -1
    fireball_image = fireball.image
    heart = Bonus(grid, field_size, map_width, map_height, image_folder+images["heart"])
    heart.x, heart.y = -1, -1
    heart_image = heart.image

    ghost_images = [image_folder+ghost_img for ghost_img in images["ghosts"]]
    ghost_image = random.choice(ghost_images)

    ghost = Ghost(grid, field_size, map_width, map_height, ghost_image)
    ghost_image = ghost.image

    # Set the title and icon
    pygame.display.set_caption("Pac-Man")
    icon = pygame.image.load(image_folder+images["pacman_icon"])
    pygame.display.set_icon(icon)

    # Load the wall images
    wall_image = pygame.image.load(image_folder+images["wall"])
    wall_image = pygame.transform.scale(wall_image, field_size)
    ghost_reverse_image = pygame.image.load(image_folder+images["ghost_reverse"])
    ghost_reverse_image = pygame.transform.scale(ghost_reverse_image, field_size)

    # Set up the game variables
    running = True
    score = 0
    
    ghosts = [ghost]
    fireball_counter = fireball_time
    heart_counter = heart_time

    # Main game loop
    while running:

        # Ghost behaviour mode
        ghost_mode = 'hunt'

        # To immediate change
        if fireball_counter == 0: heart_counter += heart_time
        if heart_counter == 0: fireball_counter += fireball_time

        fireball_counter += 1
        if fireball_counter < fireball_time:
            ghost_mode = 'calm'
        
        heart_counter += 1
        if heart_counter < heart_time:
            ghost_mode = 'fear'

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
        if pacman.x == dot.x and pacman.y == dot.y:
            score += 1
            dot = Dot(grid, field_size, map_width, map_height, image_folder+images["dot"])

            if random.randrange(10) == 0:
                fireball = Bonus(grid, field_size, map_width, map_height, image_folder+images["fireball"])
            if random.randrange(5) == 0:
                heart = Bonus(grid, field_size, map_width, map_height, image_folder+images["heart"])

            while(True):
                new_ghost = Ghost(grid, field_size, map_width, map_height, random.choice(ghost_images))
                if min(abs(new_ghost.x-pacman.x), abs(new_ghost.y-pacman.y)) > 5:
                    ghosts.append(new_ghost)
                    break

        # Fireball catching
        if pacman.x == fireball.x and pacman.y == fireball.y:
            fireball_counter = 0
            fireball.x, fireball.y = -1, -1

        # Heart catching
        if pacman.x == heart.x and pacman.y == heart.y:
            heart_counter = 0
            heart.x, heart.y = -1, -1
        
        # Ghost behaviour
        screen.fill((0, 0, 0))
        for ghost_id, ghost in enumerate(ghosts):
            
            ghost_image = ghost.image
            if ghost_mode == 'calm':
                ghost_image = ghost_reverse_image

            if pacman.x == ghost.x and pacman.y == ghost.y:
                if ghost_mode != 'calm':
                    pygame.quit()
                else:
                    del ghosts[ghost_id]
                    continue

            screen.blit(ghost_image, (ghost.x*x_scaling, ghost.y*y_scaling))
            ghosts[ghost_id].make_move(pacman.x, pacman.y, ghost_mode)

        # Draw game
        screen.blit(pacman_image, (pacman.x*x_scaling, pacman.y*y_scaling))
        screen.blit(dot_image, (dot.x*x_scaling, dot.y*y_scaling))
        screen.blit(fireball_image, (fireball.x*x_scaling, fireball.y*y_scaling))
        screen.blit(heart_image, (heart.x*x_scaling, heart.y*y_scaling))
        for field_x in range(grid.shape[0]):
            for field_y in range(grid.shape[1]):
                if grid[field_x][field_y] == 1:
                    screen.blit(wall_image, (field_x*x_scaling, field_y*y_scaling))

        font = pygame.font.Font("freesansbold.ttf", 16)
        text_score = font.render("Score: " + str(score), True, (255, 255, 255))
        text_mode = font.render("Mode: " + ghost_mode, True, (255, 255, 255))
        screen.blit(text_score, (10, 10))
        screen.blit(text_mode,  (10, 26))
        pygame.display.flip()
        time.sleep(move_delay)

    # Quit Pygame
    pygame.quit()


def main():
    config = load_config("config.json")

    run_pacman_game(screen_width=config["screen_width"],
                    screen_height=config["screen_height"],
                    map_width=config["map_width"],
                    map_height=config["map_height"],
                    move_delay=config["move_delay"],
                    wall_density=config["wall_density"],
                    images=config["images"],
                    fireball_time=config["fireball_time"],
                    heart_time=config["heart_time"],
                )
    

if __name__ == "__main__":
    main()