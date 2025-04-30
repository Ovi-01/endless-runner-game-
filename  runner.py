import pygame
import random
import sys

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_Y = SCREEN_HEIGHT - 50 # Y-coordinate for the ground

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# --- Game Variables ---
INITIAL_GAME_SPEED = 5
GAME_SPEED_INCREASE = 0.001 # How much speed increases per frame
GRAVITY = 0.6
PLAYER_JUMP_STRENGTH = 12
OBSTACLE_FREQUENCY = 90 # Lower number = more frequent obstacles (frames)
OBSTACLE_MIN_WIDTH = 20
OBSTACLE_MAX_WIDTH = 50
OBSTACLE_MIN_HEIGHT = 30
OBSTACLE_MAX_HEIGHT = 70

# --- Player Class ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 50
        # Use a Surface and fill it with color for simplicity
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.bottom = GROUND_Y # Start on the ground
        self.vel_y = 0
        self.is_jumping = False

    def jump(self):
        # Only jump if on the ground
        if not self.is_jumping:
            self.vel_y = -PLAYER_JUMP_STRENGTH
            self.is_jumping = True

    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Check if landed on the ground
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.is_jumping = False # Can jump again

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# --- Obstacle Class ---
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, current_game_speed):
        super().__init__()
        self.width = random.randint(OBSTACLE_MIN_WIDTH, OBSTACLE_MAX_WIDTH)
        self.height = random.randint(OBSTACLE_MIN_HEIGHT, OBSTACLE_MAX_HEIGHT)
        # Use a Surface and fill it with color
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH # Start off-screen to the right
        self.rect.bottom = GROUND_Y # Place on the ground
        self.speed = current_game_speed

    def update(self, current_game_speed):
        # Update speed in case it increased
        self.speed = current_game_speed
        self.rect.x -= self.speed
        # Remove sprite if it goes off-screen left
        if self.rect.right < 0:
            self.kill() # Removes the sprite from all groups

    def draw(self, screen):
         screen.blit(self.image, self.rect)

# --- Helper Function to Display Text ---
def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# --- Main Game Function ---
def game_loop():
    pygame.init()

    # --- Screen Setup ---
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Endless Runner")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36) # Default font, size 36
    game_over_font = pygame.font.Font(None, 72)

    # --- Game State Variables ---
    running = True
    game_over = False
    score = 0
    game_speed = INITIAL_GAME_SPEED
    obstacle_timer = 0 # Timer to control obstacle spawning

    # --- Sprite Groups ---
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    # --- Create Player ---
    player = Player()
    all_sprites.add(player)

    # --- Main Game Loop ---
    while running:
        # --- Game Over Handling ---
        while game_over:
            screen.fill(BLACK) # Clear screen for game over message
            draw_text(screen, "GAME OVER", game_over_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            draw_text(screen, f"Final Score: {int(score)}", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_text(screen, "Press [R] to Restart or [Q] to Quit", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        game_loop() # Restart the game by calling the function again
            clock.tick(30) # Lower framerate for game over screen


        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_ESCAPE: # Allow quitting mid-game
                     running = False

        # --- Updates ---
        player.update()
        obstacles.update(game_speed) # Pass current game speed to obstacles

        # --- Spawn Obstacles ---
        obstacle_timer += 1
        if obstacle_timer >= OBSTACLE_FREQUENCY:
            obstacle_timer = 0
            # Randomly adjust frequency slightly for variety
            if random.randint(0, 5) > 0 : # Occasionally skip spawning
                new_obstacle = Obstacle(game_speed)
                obstacles.add(new_obstacle)
                all_sprites.add(new_obstacle) # Add to all_sprites for drawing if needed, though we draw groups separately

        # --- Collision Detection ---
        # pygame.sprite.spritecollide(sprite, group, dokill)
        # dokill=False means the obstacle isn't removed upon collision (player handles game over)
        hits = pygame.sprite.spritecollide(player, obstacles, False)
        if hits:
            game_over = True # Set game over flag

        # --- Increase Score and Speed ---
        score += 0.1 # Increment score continuously
        game_speed += GAME_SPEED_INCREASE

        # --- Drawing ---
        screen.fill(WHITE) # Background

        # Draw the ground line
        pygame.draw.line(screen, BLACK, (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 2)

        # Draw Sprites
        # all_sprites.draw(screen) # Alternative way if not drawing separately
        player.draw(screen)
        obstacles.draw(screen) # Draw all obstacles in the group

        # Draw Score
        draw_text(screen, f"Score: {int(score)}", font, BLACK, 70, 20)
        draw_text(screen, f"Speed: {game_speed:.1f}", font, BLACK, SCREEN_WIDTH - 80, 20)

        # --- Flip Display ---
        pygame.display.flip()

        # --- Control Framerate ---
        clock.tick(60) # Aim for 60 FPS

    pygame.quit()
    sys.exit()

# --- Start the Game ---
if __name__ == "__main__":
    game_loop()