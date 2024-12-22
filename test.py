import pygame
import random


pygame.init()

BLACK = pygame.Color('black')

display = pygame.display.set_mode((600, 300))
# Create a rect with the dimensions of the screen at coords (0, 0).
display_rect = display.get_rect()
clock = pygame.time.Clock()

# SNAKE_IMAGE = pygame.image.load('SnakePart.png').convert_alpha()
# APPLE_IMAGE = pygame.image.load('Apple.png').convert_alpha()
# Replacement images.
SNAKE_IMAGE = pygame.Surface((30, 30))
SNAKE_IMAGE.fill((30, 150, 0))
APPLE_IMAGE = pygame.Surface((30, 30))
APPLE_IMAGE.fill((150, 30, 0))


class Player:

    def __init__(self):
        self.x = display_rect.w // 2
        self.y = display_rect.h - 30 - 5
        self.image = SNAKE_IMAGE
        # Create a rect with the size of the image at coords (0, 0).
        self.rect = self.image.get_rect()
        # Set the topleft coords of the rect.
        self.rect.x = self.x
        self.rect.y = self.y
        self.x_change = 0

    def update(self):
        """Move the player."""
        self.x += self.x_change
        # Always update the rect, because it's
        # needed for the collision detection.
        self.rect.x = self.x

    def draw(self, display):
        display.blit(self.image, self.rect)


class Enemy:

    def __init__(self):
        self.x = random.randint(0, display_rect.w - 30)
        self.y = 1
        self.image = APPLE_IMAGE
        # You can also pass the coords directly to `get_rect`.
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = 10

    def change_x(self):
        self.x = random.randint(0, display_rect.w - self.rect.w)
        self.rect.x = self.x

    def change_y(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, display):
        display.blit(self.image, self.rect)

    def reset(self):
        """Reset self.y position."""
        self.y = -30


player = Player()
enemy = Enemy()
dodged = 0
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.x_change = 5
            if event.key == pygame.K_LEFT:
                player.x_change = -5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                player.x_change = 0

    # Game logic.
    player.update()
    enemy.change_y()
    # Brings enemy back to top once it has gotten to th bottom
    if enemy.y > display_rect.h:
        enemy.change_x()
        dodged += 1
        enemy.reset()

    # Check if the player and the rect collide.
    if player.rect.colliderect(enemy.rect):
        print('Collided!')

    # Draw everything.
    display.fill(BLACK)
    enemy.draw(display)
    player.draw(display)

    pygame.display.update()
    clock.tick(60)

pygame.quit()