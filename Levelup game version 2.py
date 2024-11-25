import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Collision Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Load assets
background_img = pygame.image.load("background.jpg").convert()  # Add a path to your image
player_img = pygame.image.load("player.png").convert_alpha()  # Player sprite
enemy_img = pygame.image.load("enemy.png").convert_alpha()  # Enemy sprite
goal_img = pygame.image.load("goal.png").convert_alpha()  # Goal sprite

# Resize images
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Fit background to screen
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
goal_img = pygame.transform.scale(goal_img, (50, 50))

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game Variables
player_pos = [50, HEIGHT // 2]
player_speed = 5
enemies = [{"pos": [WIDTH, random.randint(0, HEIGHT - 50)], "speed": random.randint(3, 7)} for _ in range(5)]
goal_pos = [random.randint(200, WIDTH - 100), random.randint(50, HEIGHT - 100)]
score = 0
lives = 3
level = 1
win_condition = 10


def draw_text(text, font, color, x, y):
    """Helper function to draw text on the screen."""
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


def reset_game():
    """Resets the game variables for the next level."""
    global enemies, goal_pos, player_pos, score, level
    enemies = [{"pos": [WIDTH, random.randint(0, HEIGHT - 50)], "speed": random.randint(3, 7 + level)} for _ in range(5 + level)]
    goal_pos = [random.randint(200, WIDTH - 100), random.randint(50, HEIGHT - 100)]
    player_pos = [50, HEIGHT // 2]


# Game Loop
running = True
while running:
    screen.blit(background_img, (0, 0))  # Draw background

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos[1] > 0:  # Move Up
        player_pos[1] -= player_speed
    if keys[pygame.K_s] and player_pos[1] < HEIGHT - 50:  # Move Down
        player_pos[1] += player_speed
    if keys[pygame.K_a] and player_pos[0] > 0:  # Move Left
        player_pos[0] -= player_speed
    if keys[pygame.K_d] and player_pos[0] < WIDTH - 50:  # Move Right
        player_pos[0] += player_speed

    # Draw Player
    screen.blit(player_img, player_pos)

    # Draw Goal
    screen.blit(goal_img, goal_pos)

    # Move and Draw Enemies
    for enemy in enemies:
        enemy["pos"][0] -= enemy["speed"]  # Move enemy from right to left
        if enemy["pos"][0] < -50:  # Reset enemy position
            enemy["pos"] = [WIDTH, random.randint(0, HEIGHT - 50)]
        screen.blit(enemy_img, enemy["pos"])

        # Check Collision with Player
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_img.get_width(), player_img.get_height())
        enemy_rect = pygame.Rect(enemy["pos"][0], enemy["pos"][1], enemy_img.get_width(), enemy_img.get_height())
        if player_rect.colliderect(enemy_rect):
            lives -= 1
            if lives == 0:
                draw_text("Game Over", big_font, RED, WIDTH // 2 - 150, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.wait(3000)
                pygame.quit()
                sys.exit()
            enemy["pos"] = [WIDTH, random.randint(0, HEIGHT - 50)]  # Reset enemy position

    # Check Collision with Goal
    goal_rect = pygame.Rect(goal_pos[0], goal_pos[1], goal_img.get_width(), goal_img.get_height())
    if player_rect.colliderect(goal_rect):
        score += 1
        if score >= win_condition:
            draw_text(f"You Win! Level {level} Complete", big_font, GREEN, WIDTH // 2 - 300, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(3000)
            level += 1
            reset_game()
        else:
            goal_pos = [random.randint(200, WIDTH - 100), random.randint(50, HEIGHT - 100)]  # New Goal Position

    # Draw HUD
    draw_text(f"Score: {score}", font, WHITE, 10, 10)
    draw_text(f"Lives: {lives}", font, WHITE, 10, 50)
    draw_text(f"Level: {level}", font, WHITE, 10, 90)
    draw_text("Controls: W (Up), S (Down), A (Left), D (Right)", font, WHITE, WIDTH // 2 - 250, HEIGHT - 30)

    # Update the Screen
    pygame.display.flip()
    clock.tick(FPS)
