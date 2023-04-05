import pygame
import random
import sys

pygame.init()

# Window dimensions and grid size
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20

# Colors
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Game objects
class PacMan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([GRID_SIZE, GRID_SIZE])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update_position(self, dx, dy, walls):
        self.rect.x += dx
        self.rect.y += dy

        wall_collision = pygame.sprite.spritecollide(self, walls, False)
        if wall_collision or self.rect.x < 0 or self.rect.x > WIDTH - GRID_SIZE or self.rect.y < 0 or self.rect.y > HEIGHT - GRID_SIZE:
            self.rect.x -= dx
            self.rect.y -= dy

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([GRID_SIZE, GRID_SIZE])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def update(self, walls):
        dx = 0
        dy = 0
        if self.direction == "UP":
            dy = -GRID_SIZE
        elif self.direction == "DOWN":
            dy = GRID_SIZE
        elif self.direction == "LEFT":
            dx = -GRID_SIZE
        elif self.direction == "RIGHT":
            dx = GRID_SIZE

        self.rect.x += dx
        self.rect.y += dy

        wall_collision = pygame.sprite.spritecollide(self, walls, False)
        if wall_collision or self.rect.x < 0 or self.rect.x > WIDTH - GRID_SIZE or self.rect.y < 0 or self.rect.y > HEIGHT - GRID_SIZE:
            self.rect.x -= dx
            self.rect.y -= dy
            self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        elif random.random() < 0.1:
            self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([GRID_SIZE // 2, GRID_SIZE // 2])
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([GRID_SIZE, GRID_SIZE])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Main game loop
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")

    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    pellets = pygame.sprite.Group()
    ghosts = pygame.sprite.Group()

    # Create game objects (Pacman, Ghosts, Pellets, Walls)
    pacman = PacMan(200, 200)
    all_sprites.add(pacman)

    # Add walls
    for _ in range(50):
        x = random.randrange(1, WIDTH // GRID_SIZE - 1) * GRID_SIZE
        y = random.randrange(1, HEIGHT // GRID_SIZE - 1) * GRID_SIZE
        wall = Wall(x, y)
        walls.add(wall)
        all_sprites.add(wall)

    # Add walls around the edges
    for i in range(0, WIDTH, GRID_SIZE):
        wall = Wall(i, 0)
        walls.add(wall)
        all_sprites.add(wall)

        wall = Wall(i, HEIGHT - GRID_SIZE)
        walls.add(wall)
        all_sprites.add(wall)

    for i in range(0, HEIGHT, GRID_SIZE):
        wall = Wall(0, i)
        walls.add(wall)
        all_sprites.add(wall)

        wall = Wall(WIDTH - GRID_SIZE, i)
        walls.add(wall)
        all_sprites.add(wall)

    # Add pellets
    for _ in range(100):
        x = random.randrange(1, WIDTH // GRID_SIZE - 1) * GRID_SIZE
        y = random.randrange(1, HEIGHT // GRID_SIZE - 1) * GRID_SIZE
        pellet = Pellet(x, y)
        pellets.add(pellet)
        all_sprites.add(pellet)

    # Add ghosts
    for _ in range(5):
        x = random.randrange(1, WIDTH // GRID_SIZE - 1) * GRID_SIZE
        y = random.randrange(1, HEIGHT // GRID_SIZE - 1) * GRID_SIZE
        ghost = Ghost(x, y)
        ghosts.add(ghost)
        all_sprites.add(ghost)

    # Initialize score
    score = 0

    # Main game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle user input (move Pac-Man)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pacman.update_position(0, -GRID_SIZE, walls)
            pygame.time.delay(120)
        if keys[pygame.K_DOWN]:
            pacman.update_position(0, GRID_SIZE, walls)
            pygame.time.delay(120)
        if keys[pygame.K_LEFT]:
            pacman.update_position(-GRID_SIZE, 0, walls)
            pygame.time.delay(120)
        if keys[pygame.K_RIGHT]:
            pacman.update_position(GRID_SIZE, 0, walls)
            pygame.time.delay(120)

        # Update ghosts' positions
        for ghost in ghosts:
            ghost.update(walls)

        # Check for collisions
        pellet_collision = pygame.sprite.spritecollide(pacman, pellets, True)
        ghost_collision = pygame.sprite.spritecollide(pacman, ghosts, False)

        # Update score
        score += len(pellet_collision)

        # Draw game objects
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, GREEN)
        screen.blit(text, (10, 10))

        # Refresh display
        pygame.display.flip()

        if ghost_collision:
            # Game Over
            running = False

        # Limit frames per second
        clock.tick(15)

    # Display the score card
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    text = font.render(f"Game Over! Your score: {score}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()