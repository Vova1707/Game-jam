import pygame
import pickle
import random
import os
import math
import pygame_widgets
from pygame_widgets.button import Button as buttonsss

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Player, self).__init__()
		self.x = x
		self.y = y

		self.idle_list = []
		self.walk_left = []
		self.walk_right = []
		self.attack_list = []
		self.death_list = []
		self.hit_list = []

		self.size = 24

		for i in range(1, 3):
			image = pygame.image.load(f'For_Mini_Gaming/Assets/Player/PlayerIdle{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.idle_list.append(image)
		for i in range(1, 6):
			image = pygame.image.load(f'For_Mini_Gaming/Assets/Player/PlayerWalk{i}.png')
			right = pygame.transform.scale(image, (24, 24))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)
		for i in range(1, 5):
			image = pygame.image.load(f'For_Mini_Gaming/Assets/Player/PlayerAttack{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.attack_list.append(image)
		for i in range(1, 11):
			image = pygame.image.load(f'For_Mini_Gaming/Assets/Player/PlayerDead{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.death_list.append(image)
		for i in range(1, 3):
			image = pygame.image.load(f'For_Mini_Gaming/Assets/Player/PlayerHit{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.hit_list.append(image)

		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.fall_index = 0

		self.jump_height = 15
		self.speed = 3
		self.vel = self.jump_height
		self.mass = 1
		self.gravity = 1

		self.counter = 0
		self.direction = 0

		self.alive = True
		self.attack = False
		self.hit = False
		self.jump = False

		self.grenades = 5
		self.health = 100

		self.image = self.idle_list[self.idle_index]
		self.image = pygame.transform.scale(self.image, (24, 24))
		self.rect = self.image.get_rect(center=(x, y))

	def check_collision(self, world, dx, dy):
		# Checking collision with ground
		for tile in world.ground_list:
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# above ground
				if self.rect.y + dy <= tile[1].y:
					# if self.vel < 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
		# print(self.vel, dy)

		# Checking collision with rocks & stones
		for tile in world.rock_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
				# left / right collision
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# below ground
				if self.vel > 0 and self.vel != self.jump_height:
					dy = 0
					self.jump = False
					self.vel = self.jump_height
				# above ground
				elif self.vel <= 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom

		return dx, dy

	def update_animation(self):
		self.counter += 1
		if self.counter % 7 == 0:
			if self.health <= 0:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.alive = False
			else:
				if self.attack:
					self.attack_index += 1
					if self.attack_index >= len(self.attack_list):
						self.attack_index = 0
						self.attack = False
				if self.hit:
					self.hit_index += 1
					if self.hit_index >= len(self.hit_list):
						self.hit_index = 0
						self.hit = False
				if self.direction == 0:
					self.idle_index = (self.idle_index + 1) % len(self.idle_list)
				if self.direction == -1 or self.direction == 1:
					self.walk_index = (self.walk_index + 1) % len(self.walk_left)
			self.counter = 0

		if self.alive:
			if self.health <= 0:
				self.image = self.death_list[self.death_index]
			elif self.attack:
				self.image = self.attack_list[self.attack_index]
				if self.direction == -1:
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
			elif self.direction == 0:
				self.image = self.idle_list[self.idle_index]
			elif self.direction == -1:
				self.image = self.walk_left[self.walk_index]
			elif self.direction == 1:
				self.image = self.walk_right[self.walk_index]

	def update(self, moving_left, moving_right, world):
		self.dx = 0
		self.dy = 0

		if moving_left:
			self.dx = -self.speed
			self.direction = -1
		if moving_right:
			self.dx = self.speed
			self.direction = 1
		if (not moving_left and not moving_right) and not self.jump:
			self.direction = 0
			self.walk_index = 0

		if self.jump:
			F = (1 / 2) * self.mass * self.vel
			self.dy -= F
			self.vel -= self.gravity

			if self.vel < -15:
				self.vel = self.jump_height
				self.jump = False
		else:
			self.dy += self.vel

		self.dx, self.dy = self.check_collision(world, self.dx, self.dy)

		if self.rect.left + self.dx < 0 or self.rect.right + self.dx > WIDTH:
			self.dx = 0

		self.rect.x += self.dx
		self.rect.y += self.dy

		self.update_animation()

	def draw(self, win):
		win.blit(self.image, self.rect)


class Text:
	''' This class returns an image '''

	def __init__(self, font, font_size):
		self.font = pygame.font.Font(font, font_size)

	def render(self, text, color):
		image = self.font.render(text, False, color)
		return image


class Message:
	''' This class blits an image at given position '''

	def __init__(self, x, y, size, text, font, color, win):
		self.win = win
		self.color = color
		self.x, self.y = x, y
		if not font:
			self.font = pygame.font.SysFont("Verdana", size)
			anti_alias = True
		else:
			self.font = pygame.font.Font(font, size)
			anti_alias = False
		self.image = self.font.render(text, anti_alias, color)
		self.rect = self.image.get_rect(center=(x, y))
		if self.color == (200, 200, 200):
			self.shadow_color = (255, 255, 255)
		else:
			self.shadow_color = (54, 69, 79)
		self.shadow = self.font.render(text, anti_alias, self.shadow_color)
		self.shadow_rect = self.image.get_rect(center=(x + 2, y + 2))

	def update(self, text=None, color=None, shadow=True):
		if text:
			if not color:
				color = self.color
			self.image = self.font.render(f"{text}", False, color)
			self.rect = self.image.get_rect(center=(self.x, self.y))
			self.shadow = self.font.render(f"{text}", False, self.shadow_color)
			self.shadow_rect = self.image.get_rect(center=(self.x + 2, self.y + 2))
		if shadow:
			self.win.blit(self.shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)


class BlinkingText(Message):
	''' This class creates a blinking text image surface '''

	def __init__(self, x, y, size, text, font, color, win):
		super(BlinkingText, self).__init__(x, y, size, text, font, color, win)
		self.index = 0
		self.show = True

	def update(self):
		self.index += 1
		if self.index % 40 == 0:
			self.show = not self.show

		if self.show:
			self.win.blit(self.image, self.rect)


def MessageBox(win, font, name, text):
	''' This class creates a message box and automatically fills the text '''
	WIDTH = 640
	HEIGHT = 284
	x = 35
	y = 65  # depends on message box location
	pygame.draw.rect(win, (255, 255, 255), (25, 25, WIDTH - 40, HEIGHT - 84), border_radius=10)
	for word in text.split(' '):
		rendered = font.render(word, 0, (0, 0, 0))
		width = rendered.get_width()
		if x + width >= WIDTH:
			x = 35
			y += 25
		win.blit(rendered, (x, y))
		x += width + 5

	title = font.render(name, 0, (0, 0, 0))
	title_width = 120
	pygame.draw.rect(win, (255, 255, 255), (WIDTH // 2 - title_width // 2 + 10, 10,
											title_width, 30), border_radius=10)
	win.blit(title, (WIDTH // 2 - title.get_width() // 2 + 10, 10))

class Trail(pygame.sprite.Sprite):
	def __init__(self, pos, color, win):
		super(Trail, self).__init__()
		self.color = color
		self.win = win

		self.x, self.y = pos
		self.y += 10
		self.dx = random.randint(0, 20) / 10 - 1
		self.dy = -2
		self.size = random.randint(4, 7)

		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.size)

	def update(self):
		self.x -= self.dx
		self.y -= self.dy
		self.size -= 0.1

		if self.size <= 0:
			self.kill()

		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.size)


class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Explosion, self).__init__()
		self.x = x
		self.y = y
		self.win = win

		self.size = random.randint(4, 9)
		self.life = 40
		self.lifetime = 0

		self.x_vel = random.randrange(-4, 4)
		self.y_vel = random.randrange(-4, 4)

		self.color = 150

	def update(self, screen_scroll):
		self.size -= 0.2
		self.lifetime += 1
		self.color -= 2
		if self.lifetime <= self.life:
			self.x += self.x_vel + screen_scroll
			self.y += self.y_vel
			s = int(self.size)
			pygame.draw.rect(self.win, (self.color, self.color, self.color), (self.x, self.y, s, s))
		else:
			self.kill()

NUM_TILES = 60
TILE_SIZE = 16

img_list = []
for index in range(1, NUM_TILES+1):
	img = pygame.image.load(f'For_Mini_Gaming/Tiles/{index}.png')
	img_list.append(img)

pygame.mixer.init()
grenade_blast_fx = pygame.mixer.Sound('For_Mini_Gaming/Sounds/grenade blast.wav')
grenade_blast_fx.set_volume(0.6)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, color, type_, win):
		super(Bullet, self).__init__()

		self.x = x
		self.y = y
		self.direction = direction
		self.color = color
		self.type = type_
		self.win = win

		self.speed = 10
		self.radius = 4

		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)

	def update(self, screen_scroll, world):
		if self.direction == -1:
			self.x -= self.speed + screen_scroll
		if self.direction == 0 or self.direction == 1:
			self.x += self.speed + screen_scroll

		for tile in world.ground_list:
			if tile[1].collidepoint(self.x, self.y):
				self.kill()
		for tile in world.rock_list:
			if tile[1].collidepoint(self.x, self.y):
				self.kill()

		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)


class Grenade(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, win):
		super(Grenade, self).__init__()

		self.x = x
		self.y = y
		self.direction = direction
		self.win = win

		self.speed = 10
		self.vel_y = -11
		self.timer = 15
		self.radius = 4

		if self.direction == 0:
			self.direction = 1

		pygame.draw.circle(self.win, (200, 200, 200), (self.x, self.y), self.radius + 1)
		self.rect = pygame.draw.circle(self.win, (255, 50, 50), (self.x, self.y), self.radius)
		pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), 1)

	def update(self, screen_scroll, p, enemy_group, explosion_group, world):
		self.vel_y += 1
		dx = self.direction * self.speed
		dy = self.vel_y

		for tile in world.ground_list:
			if tile[1].colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
				if self.rect.y <= tile[1].y:
					dy = 0
					self.speed -= 1
					if self.speed <= 0:
						self.speed = 0

		for tile in world.rock_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
				self.direction *= -1
				dx = self.direction * self.speed
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
				if self.rect.y <= tile[1].y:
					dy = 0
					self.speed -= 1
					if self.speed <= 0:
						self.speed = 0

		if self.rect.y > WIDTH:
			self.kill()

		if self.speed == 0:
			self.timer -= 1
			if self.timer <= 0:
				grenade_blast_fx.play()
				for _ in range(30):
					explosion = Explosion(self.x, self.y, self.win)
					explosion_group.add(explosion)

				p_distance = math.sqrt((p.rect.centerx - self.x) ** 2 + (p.rect.centery - self.y) ** 2)
				if p_distance <= 100:
					if p_distance > 80:
						p.health -= 20
					elif p_distance > 40:
						p.health -= 50
					elif p_distance >= 0:
						p.health -= 80
					p.hit = True

				for e in enemy_group:
					e_distance = math.sqrt((e.rect.centerx - self.x) ** 2 + (e.rect.centery - self.y) ** 2)
					if e_distance < 80:
						e.health -= 100

				self.kill()

		self.x += dx + screen_scroll
		self.y += dy

		pygame.draw.circle(self.win, (200, 200, 200), (self.x, self.y), self.radius + 1)
		self.rect = pygame.draw.circle(self.win, (255, 50, 50), (self.x, self.y), self.radius)
		pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), 1)



class World:
	def __init__(self, objects_group):
		self.objects_group = objects_group

		self.ground_list = []
		self.rock_list = []
		self.decor_list = []

	def generate_world(self, data, win):
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = img_list[tile-1]
					rect = img.get_rect()
					rect.x = x * TILE_SIZE
					rect.y = y * TILE_SIZE
					tile_data = (img, rect)

					if tile in (0, 1, 2, 3, 4, 5, 6, 11):
						self.ground_list.append(tile_data)

					if tile in (7, 14, 18, 19, 20, 21, 25, 26, 27, 28, 32, 33, 34, 35, 42, 43, 44, 45):
						self.rock_list.append(tile_data)

					if tile in (8, 9, 10, 13, 15, 16, 17, 23, 24, 30, 31, 37, 38, 39, 40, 46, 47, 48, 49, 50, 51):
						self.decor_list.append(tile_data)

					if tile == 12:
						exit = Exit(x*TILE_SIZE, y*TILE_SIZE, tile_data)
						self.objects_group[4].add(exit)

					if tile == 41:
						water = Water(x*TILE_SIZE, y*TILE_SIZE, tile_data)
						self.objects_group[0].add(water)

					if tile in (52, 53, 56, 57):
						diamond = Diamond(x*TILE_SIZE, y*TILE_SIZE, tile_data)
						self.objects_group[1].add(diamond)

					if tile in (54, 55, 58, 59):
						potion = Potion(x*TILE_SIZE, y*TILE_SIZE, tile_data)
						self.objects_group[2].add(potion)

					if tile == 60:
						enemy = Ghost(x*TILE_SIZE, y*TILE_SIZE, win)
						self.objects_group[3].add(enemy)

	def draw_world(self, win, screen_scroll):
		for tile in self.ground_list:
			tile[1][0] += screen_scroll
			win.blit(tile[0], tile[1])
		for tile in self.rock_list:
			tile[1][0] += screen_scroll
			win.blit(tile[0], tile[1])
		for tile in self.decor_list:
			tile[1][0] += screen_scroll
			win.blit(tile[0], tile[1])


class Ladder(pygame.sprite.Sprite):
	def __init__(self, x, y, tile_data):
		super(Ladder, self).__init__()

		self.image = tile_data[0]
		self.rect = tile_data[1]
		self.rect.x = x
		self.rect.y = y

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)

class Water(pygame.sprite.Sprite):
	def __init__(self, x, y, tile_data):
		super(Water, self).__init__()

		self.image = tile_data[0]
		self.rect = tile_data[1]
		self.rect.x = x
		self.rect.y = y

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)

class Diamond(pygame.sprite.Sprite):
	def __init__(self, x, y, tile_data):
		super(Diamond, self).__init__()

		self.image = tile_data[0]
		self.rect = tile_data[1]
		self.rect.x = x
		self.rect.y = y

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)

class Potion(pygame.sprite.Sprite):
	def __init__(self, x, y, tile_data):
		super(Potion, self).__init__()

		self.image = tile_data[0]
		self.rect = tile_data[1]
		self.rect.x = x
		self.rect.y = y

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)

class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y, tile_data):
		super(Exit, self).__init__()

		self.image = pygame.transform.scale(tile_data[0], (24,24))
		self.rect = tile_data[1]
		self.rect.x = x
		self.rect.y = y - 8

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

	def draw(self, win):
		win.blit(self.image, self.rect)

def load_level(level):
	file = f'For_Mini_Gaming/Levels/level{level}_data'
	with open(file, 'rb') as f:
		data = pickle.load(f)
		for y in range(len(data)):
			for x in range(len(data[0])):
				if data[y][x] >= 0:
					data[y][x] += 1
	return data, len(data[0])

class Button():
	def __init__(self,x, y, image, scale, text=None, xoff=None):
		self.width = int(image.get_width() * scale)
		self.height = int(image.get_height() * scale)
		self.image = pygame.transform.scale(image, (self.width, self.height))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

		self.text = None
		if text:
			self.text = text
			if xoff:
				self.xoff = xoff
			else:
				self.xoff = self.text.get_width() // 2
			self.yoff = self.text.get_height() // 2

		self.clicked = False

	def draw(self, surface):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))
		if self.text:
			self.image.blit(self.text, (self.width//2 - self.xoff, self.height//2 - self.yoff))

		return action






TILE_SIZE = 16

bullet_fx = pygame.mixer.Sound('For_Mini_Gaming/Sounds/ghost_shot.mp3')

class Ghost(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Ghost, self).__init__()

		self.x = x
		self.y = y
		self.win = win
		self.initial_pos_x = x

		self.size = 32

		self.walk_left = []
		self.walk_right = []
		self.hit_list = []
		self.death_list = []

		for i in range(1,6):
			image = pygame.image.load(f'For_Mini_Gaming/Assets/Ghost/Enemywalk{i}.png')
			right = right = pygame.transform.scale(image, (self.size, self.size))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)
		for i in range(1, 3):
			image = pygame.image.load(f'For_Mini_Gaming/Assets/Ghost/Enemyhit{i}.png')
			image = pygame.transform.scale(image, (self.size, self.size))
			self.hit_list.append(image)
		for i in range(1,9):
			image = pygame.image.load(f'For_Mini_Gaming/Assets/Ghost/Enemydead{i}.png')
			image = pygame.transform.scale(image, (self.size, self.size))
			self.death_list.append(image)

		self.walk_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.counter = 0

		self.dx = random.choice([-1, 1])
		self.alive = True
		self.health = 100
		self.hit = False
		self.on_death_bed = False

		self.image = self.walk_right[self.walk_index]
		self.rect = self.image.get_rect(center=(self.x, self.y))

	def update(self, screen_scroll, bullet_group, p):
		if self.health:
			self.rect.x += (self.dx + screen_scroll)
			self.x += screen_scroll
			if abs(self.rect.x - self.x) >= 2 * TILE_SIZE:
				self.dx *= -1

		if self.health <= 0:
			self.on_death_bed = True

		self.counter += 1
		if self.counter % 5 == 0:
			if self.on_death_bed:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.kill()
					self.alive = False
			if self.hit:
				self.hit_index += 1
				if self.hit_index >= len(self.hit_list):
					self.hit_index = 0
					self.hit = False
			else:
				self.walk_index  = (self.walk_index + 1) % len(self.walk_left)

		if self.counter % 50 == 0:
			if self.health > 0 and (abs(p.rect.x - self.rect.x) <= 200):
				x, y = self.rect.center
				direction = self.dx
				bullet = Bullet(x, y, direction, (160, 160, 160), 2, self.win)
				bullet_group.add(bullet)
				bullet_fx.play()

		if self.alive:
			if self.on_death_bed:
				self.image = self.death_list[self.death_index]
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
			else:
				if self.dx == -1:
					self.image = self.walk_left[self.walk_index]
				elif self.dx == 1:
					self.image = self.walk_right[self.walk_index]

	def draw(self, win):
		win.blit(self.image, self.rect)


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800
MARGIN_LEFT = 300
WIDTH = SCREEN_WIDTH + MARGIN_LEFT
HEIGHT = SCREEN_HEIGHT

TILE_WIDTH = 16
TILE_HEIGHT = 16
NUM_TILES = 60

ROWS = SCREEN_HEIGHT // TILE_HEIGHT
COLS = SCREEN_WIDTH // TILE_WIDTH
MAX_COLS = 100

clock = pygame.time.Clock()
FPS = 30

# game_variables **************************************************************
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
current_tile = 0
current_level = 1

# color variabes
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (255, 25, 25)

#font = pygame.font.SysFont('Futura', 24)


































def game_from_ps(display):
	WIDTH, HEIGHT = 900, 800
	win = pygame.Surface((WIDTH, HEIGHT))
	TILE_SIZE = 16
	pygame.mixer.init()
	clock = pygame.time.Clock()
	FPS = 45

	# IMAGES **********************************************************************

	BG1 = pygame.transform.scale(pygame.image.load('For_Mini_Gaming/Assets/BG1.png'), (WIDTH, HEIGHT))
	BG2 = pygame.transform.scale(pygame.image.load('For_Mini_Gaming/Assets/BG2.png'), (WIDTH, HEIGHT))
	BG3 = pygame.transform.scale(pygame.image.load('For_Mini_Gaming/Assets/BG3.png'), (WIDTH, HEIGHT))
	MOON = pygame.transform.scale(pygame.image.load('For_Mini_Gaming/Assets/moon.png'), (300, 220))

	# FONTS ***********************************************************************

	title_font = "Fonts/Aladin-Regular.ttf"
	instructions_font = 'Fonts/BubblegumSans-Regular.ttf'
	# about_font = 'Fonts/DalelandsUncialBold-82zA.ttf'

	ghostbusters = Message(WIDTH // 2 + 50, HEIGHT // 2 - 90, 90, "GhostBusters", title_font, (255, 255, 255), win)
	left_key = Message(WIDTH // 2 + 10, HEIGHT // 2 - 90, 20, "Press left arrow key to go left", instructions_font,
					   (255, 255, 255), win)
	right_key = Message(WIDTH // 2 + 10, HEIGHT // 2 - 65, 20, "Press right arrow key to go right", instructions_font,
						(255, 255, 255), win)
	up_key = Message(WIDTH // 2 + 10, HEIGHT // 2 - 45, 20, "Press up arrow key to jump", instructions_font,
					 (255, 255, 255), win)
	space_key = Message(WIDTH // 2 + 10, HEIGHT // 2 - 25, 20, "Press space key to shoot", instructions_font,
						(255, 255, 255), win)
	g_key = Message(WIDTH // 2 + 10, HEIGHT // 2 - 5, 20, "Press g key to throw grenade", instructions_font,
					(255, 255, 255), win)
	game_won_msg = Message(WIDTH // 2 + 10, HEIGHT // 2 - 5, 20, "You have won the game", instructions_font,
						   (255, 255, 255), win)

	t = Text(instructions_font, 18)
	font_color = (12, 12, 12)
	play = t.render('Play', font_color)
	about = t.render('About', font_color)
	controls = t.render('Controls', font_color)
	exit = t.render('Exit', font_color)
	main_menu = t.render('Main Menu', font_color)

	about_font = pygame.font.SysFont('Times New Roman', 20)
	with open('Data/about.txt') as f:
		info = f.read().replace('\n', ' ')

	# BUTTONS *********************************************************************

	ButtonBG = pygame.image.load('For_Mini_Gaming/Assets/ButtonBG.png')
	bwidth = ButtonBG.get_width()

	play_btn = Button(WIDTH // 2 - bwidth // 4, HEIGHT // 2, ButtonBG, 0.5, play, 10)
	about_btn = Button(WIDTH // 2 - bwidth // 4, HEIGHT // 2 + 35, ButtonBG, 0.5, about, 10)
	controls_btn = Button(WIDTH // 2 - bwidth // 4, HEIGHT // 2 + 70, ButtonBG, 0.5, controls, 10)
	exit_btn = Button(WIDTH // 2 - bwidth // 4, HEIGHT // 2 + 105, ButtonBG, 0.5, exit, 10)
	main_menu_btn = Button(WIDTH // 2 - bwidth // 4, HEIGHT // 2 + 130, ButtonBG, 0.5, main_menu, 20)

	# MUSIC ***********************************************************************
	# GROUPS **********************************************************************

	trail_group = pygame.sprite.Group()
	bullet_group = pygame.sprite.Group()
	grenade_group = pygame.sprite.Group()
	explosion_group = pygame.sprite.Group()
	enemy_group = pygame.sprite.Group()
	water_group = pygame.sprite.Group()
	diamond_group = pygame.sprite.Group()
	potion_group = pygame.sprite.Group()
	exit_group = pygame.sprite.Group()

	objects_group = [water_group, diamond_group, potion_group, enemy_group, exit_group]

	p_image = pygame.transform.scale(pygame.image.load('For_Mini_Gaming/Assets/Player/PlayerIdle1.png'), (32, 32))
	p_rect = p_image.get_rect(center=(470, 200))
	p_dy = 1
	p_ctr = 1

	# LEVEL VARIABLES **************************************************************

	ROWS = 24
	COLS = 40
	SCROLL_THRES = 200
	MAX_LEVEL = 3

	level = 1
	level_length = 0
	screen_scroll = 0
	bg_scroll = 0
	dx = 0

	# RESET ***********************************************************************

	def reset_level(level):
		trail_group.empty()
		bullet_group.empty()
		grenade_group.empty()
		explosion_group.empty()
		enemy_group.empty()
		water_group.empty()
		diamond_group.empty()
		potion_group.empty()
		exit_group.empty()

		# LOAD LEVEL WORLD

		world_data, level_length = load_level(level)
		w = World(objects_group)
		w.generate_world(world_data, win)

		return world_data, level_length, w

	def reset_player():
		p = Player(250, 50)
		moving_left = False
		moving_right = False

		return p, moving_left, moving_right

	# MAIN GAME *******************************************************************

	main_menu = True
	about_page = False
	controls_page = False
	exit_page = False
	game_start = False
	game_won = True
	running = True

	a = []
	sss = []

	button = buttonsss(
		display,  # Surface to place button on
		900,
		100,  # Y-coordinate of top left corner
		100,  # Width
		50,
		colour=(255, 0, 0),
		text='X',  # Heigh
		onClick=lambda: stopping(sss), )
	a.append(button)
	print(a)
	def stopping(ss):
		ss.append(1)

	while running:
		win.fill((0, 0, 0))
		for x in range(5):
			win.blit(BG1, ((x * WIDTH) - bg_scroll * 0.6, 0))
			win.blit(BG2, ((x * WIDTH) - bg_scroll * 0.7, 0))
			win.blit(BG3, ((x * WIDTH) - bg_scroll * 0.8, 0))

		if not game_start:
			win.blit(MOON, (-40, 150))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif sss:
				running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					moving_left = True
				if event.key == pygame.K_RIGHT:
					moving_right = True
				if event.key == pygame.K_UP:
					if not p.jump:
						p.jump = True
				if event.key == pygame.K_g:
					if p.grenades:
						p.grenades -= 1
						grenade = Grenade(p.rect.centerx, p.rect.centery, p.direction, win)
						grenade_group.add(grenade)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					moving_left = False
				if event.key == pygame.K_RIGHT:
					moving_right = False

		if main_menu:
			ghostbusters.update()
			trail_group.update()
			win.blit(p_image, p_rect)
			p_rect.y += p_dy
			p_ctr += p_dy
			if p_ctr > 15 or p_ctr < -15:
				p_dy *= -1
			t = Trail(p_rect.center, (220, 220, 220), win)
			trail_group.add(t)

			if play_btn.draw(win):
				world_data, level_length, w = reset_level(level)
				p, moving_left, moving_right = reset_player()

				game_start = True
				main_menu = False
				game_won = False

			if about_btn.draw(win):
				about_page = True
				main_menu = False

			if controls_btn.draw(win):
				controls_page = True
				main_menu = False

			if exit_btn.draw(win):
				running = False

		elif about_page:
			MessageBox(win, about_font, 'GhostBusters', info)
			if main_menu_btn.draw(win):
				about_page = False
				main_menu = True

		elif controls_page:
			left_key.update()
			right_key.update()
			up_key.update()
			space_key.update()
			g_key.update()

			if main_menu_btn.draw(win):
				controls_page = False
				main_menu = True

		elif exit_page:
			pass

		elif game_won:
			game_won_msg.update()
			if main_menu_btn.draw(win):
				controls_page = False
				main_menu = True
				level = 1


		elif game_start:
			win.blit(MOON, (-40, -10))
			w.draw_world(win, screen_scroll)

			# Updating Objects ********************************************************

			bullet_group.update(screen_scroll, w)
			grenade_group.update(screen_scroll, p, enemy_group, explosion_group, w)
			explosion_group.update(screen_scroll)
			trail_group.update()
			water_group.update(screen_scroll)
			water_group.draw(win)
			diamond_group.update(screen_scroll)
			diamond_group.draw(win)
			potion_group.update(screen_scroll)
			potion_group.draw(win)
			exit_group.update(screen_scroll)
			exit_group.draw(win)

			enemy_group.update(screen_scroll, bullet_group, p)
			enemy_group.draw(win)

			if p.jump:
				t = Trail(p.rect.center, (220, 220, 220), win)
				trail_group.add(t)

			screen_scroll = 0
			p.update(moving_left, moving_right, w)
			p.draw(win)

			if (p.rect.right >= WIDTH - SCROLL_THRES and bg_scroll < (level_length * TILE_SIZE) - WIDTH) \
					or (p.rect.left <= SCROLL_THRES and bg_scroll > abs(dx)):
				dx = p.dx
				p.rect.x -= dx
				screen_scroll = -dx
				bg_scroll -= screen_scroll

			# Collision Detetction ****************************************************

			if p.rect.bottom > HEIGHT:
				p.health = 0

			if pygame.sprite.spritecollide(p, water_group, False):
				p.health = 0
				level = 1

			if pygame.sprite.spritecollide(p, diamond_group, True):
				pass

			if pygame.sprite.spritecollide(p, exit_group, False):
				level += 1
				if level <= MAX_LEVEL:
					health = p.health

					world_data, level_length, w = reset_level(level)
					p, moving_left, moving_right = reset_player()
					p.health = health

					screen_scroll = 0
					bg_scroll = 0
				else:
					game_won = True

			potion = pygame.sprite.spritecollide(p, potion_group, False)
			if potion:
				if p.health < 100:
					potion[0].kill()
					p.health += 15
					if p.health > 100:
						p.health = 100

			for bullet in bullet_group:
				enemy = pygame.sprite.spritecollide(bullet, enemy_group, False)
				if enemy and bullet.type == 1:
					if not enemy[0].hit:
						enemy[0].hit = True
						enemy[0].health -= 50
					bullet.kill()
				if bullet.rect.colliderect(p):
					if bullet.type == 2:
						if not p.hit:
							p.hit = True
							p.health -= 20
							print(p.health)
						bullet.kill()

			# drawing variables *******************************************************

			if p.alive:
				color = (0, 255, 0)
				if p.health <= 40:
					color = (255, 0, 0)
				pygame.draw.rect(win, color, (6, 8, p.health, 20), border_radius=10)
			pygame.draw.rect(win, (255, 255, 255), (6, 8, 100, 20), 2, border_radius=10)

			for i in range(p.grenades):
				pygame.draw.circle(win, (200, 200, 200), (20 + 15 * i, 40), 5)
				pygame.draw.circle(win, (255, 50, 50), (20 + 15 * i, 40), 4)
				pygame.draw.circle(win, (0, 0, 0), (20 + 15 * i, 40), 1)

			if p.health <= 0:
				world_data, level_length, w = reset_level(level)
				p, moving_left, moving_right = reset_player()

				screen_scroll = 0
				bg_scroll = 0

				main_menu = True
				about_page = False
				controls_page = False
				game_start = False
		pygame_widgets.update(pygame.event.get())
		display.blit(win, (0, 0))
		clock.tick(FPS)
		pygame.display.update()
	running = True
	sss = []
	return 1
	pygame.mixer.stop()