import random
import pygame
import math
import pygame_widgets
from pygame_widgets.button import Button as buttonsss

def hyper_dash(display):
	win = pygame.Surface(SCREEN)
	clock = pygame.time.Clock()
	FPS = 60
	RED = (255, 0, 0)
	GREEN = (0, 177, 64)
	BLUE = (30, 144, 255)
	ORANGE = (252, 76, 2)
	YELLOW = (254, 221, 0)
	PURPLE = (155, 38, 182)
	AQUA = (0, 103, 127)
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)
	GRAY = (32, 32, 32)

	color_list = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE]
	color_index = 0
	color = color_list[color_index]

	death_color_list = [BLUE, ORANGE, YELLOW, PURPLE, RED, GREEN]
	death_color_index = 0
	death_color = death_color_list[color_index]

	# FONTS ***********************************************************************

	title_font = "Fonts1/Aladin-Regular.ttf"
	tap_to_play_font = "Fonts1/BubblegumSans-Regular.ttf"
	score_font = "Fonts1/DalelandsUncialBold-82zA.ttf"
	game_over_font = "Fonts1/ghostclan.ttf"

	HyperTile = Message(WIDTH // 2, HEIGHT // 2 - 20, 50, "HyperTiles", title_font, BLUE, win)
	dash = Message(WIDTH // 2 + 40, HEIGHT // 2 + 40, 50, "Dash...", title_font, GREEN, win)
	tap_to_play = BlinkingText(WIDTH // 2, HEIGHT - 50, 20, "Tap To Play", tap_to_play_font, WHITE, win)

	score_msg = Message(WIDTH // 2, HEIGHT // 2, 50, "0", score_font, (100, 100, 100), win)
	final_score = Message(WIDTH // 3, HEIGHT // 2 - 20, 90, "0", score_font, WHITE, win)
	best_msg = Message(WIDTH // 2 + 45, HEIGHT // 2 - 40, 25, "BEST", None, WHITE, win)
	high_score_msg = Message(WIDTH // 2 + 35, HEIGHT // 2 - 5, 35, "0", None, WHITE, win)

	# Button images

	home_img = pygame.image.load('Assets/homeBtn.png')
	replay_img = pygame.image.load('Assets/replay.png')
	sound_off_img = pygame.image.load("Assets/soundOffBtn.png")
	sound_on_img = pygame.image.load("Assets/soundOnBtn.png")

	# Buttons

	home_btn = Button(home_img, (24, 24), WIDTH // 4 - 18, HEIGHT // 2 + 50)
	replay_btn = Button(replay_img, (36, 36), WIDTH // 2 - 18, HEIGHT // 2 + 45)
	sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, HEIGHT // 2 + 50)

	# OBJECTS *********************************************************************

	tile_group = pygame.sprite.Group()

	for i in range(8):
		tile = Tile(i, 1, win)
		tile_group.add(tile)
		tile = Tile(i, 2, win)
		tile_group.add(tile)

	particle_group = pygame.sprite.Group()
	skull_group = pygame.sprite.Group()
	p = Player(win, tile_group)

	# FUNCTIONS *******************************************************************

	deadly_tiles_list = []

	def get_index():
		if p.tile_type == 1:
			indices = [2 * index + 1 for index in range(8)]
		elif p.tile_type == 2:
			indices = [2 * index for index in range(8)]

		index = random.choice(indices)
		return index

	def generate_target_tile(color):
		for tile in tile_group:
			if not tile.is_deadly_tile:
				tile.color = WHITE
				tile.is_target_tile = False

		index = get_index()
		tile = tile_group.sprites()[index]
		if tile.is_deadly_tile:
			generate_target_tile(color)
		else:
			tile.color = color
			tile.is_target_tile = True

		return tile

	def generate_deadly_tile(color):
		for tile in tile_group:
			if tile.is_deadly_tile:
				tile.color = color

		index = get_index()
		tile = tile_group.sprites()[index]
		if tile.is_target_tile:
			generate_deadly_tile(color)
		else:
			if tile.is_deadly_tile:
				generate_deadly_tile(color)
			else:
				tile.color = color
				tile.is_deadly_tile = True
				deadly_tiles_list.append(tile)

	clicked = False
	num_clicks = 0
	index = None
	target_tile = None
	auto_generate_deadly_tile = True

	player_alive = True
	score = 0
	highscore = 0
	sound_on = True

	home_page = True
	game_page = False
	score_page = False

	running = True
	a = []
	sss = []
	dddd = []

	button = buttonsss(
		display,  # Surface to place button on
		488,
		0,  # Y-coordinate of top left corner
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
		win.fill(GRAY)
		if sss:
			running = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or \
						event.key == pygame.K_q:
					running = False

			if event.type == pygame.MOUSEBUTTONDOWN and home_page:
				home_page = False
				game_page = True
				score_page = False

				player_alive = True
				p.reset()
				p.reset_path_variables()

				for tile in tile_group:
					tile.color = WHITE

			if event.type == pygame.MOUSEBUTTONDOWN and game_page:
				if not clicked:
					if p.can_move:

						index = p.path_index
						tile = p.path_target_tile
						x = p.path_x
						y = p.path_y
						p.set_move(x, y, index)

					num_clicks += 1
					if num_clicks % 5 == 0:
						color_index += 1
						if color_index > len(color_list) - 1:
							color_index = 0
						color = color_list[color_index]

						death_color_index += 1
						if death_color_index > len(death_color_list) - 1:
							death_color_index = 0
						death_color = death_color_list[death_color_index]
						for tile in deadly_tiles_list:
							tile.color = death_color

			if event.type == pygame.MOUSEBUTTONDOWN:
				clicked = False

		if home_page:
			tile_group.update()
			HyperTile.update()
			dash.update()
			tap_to_play.update()

		if score_page:
			running = False
		if game_page:

			if p.first_tile and auto_generate_deadly_tile:
				target_tile = generate_target_tile(color)
				generate_deadly_tile(death_color)
				auto_generate_deadly_tile = False

			if score and score % 3 == 0 and len(skull_group) == 0 and player_alive:
				type_ = random.randint(1, 2)
				print(type_)
				y = random.randint(200, HEIGHT - 190)
				if type_ == 1:
					x = 0
				elif type_ == 2:
					x = WIDTH + 5
				skull = SkullCircle(x, y, type_, death_color, win)
				skull_group.add(skull)

			score_msg.update(score)
			particle_group.update()
			skull_group.update()
			p.update(color, player_alive)
			tile_group.update()

			if pygame.sprite.spritecollide(p, skull_group, False) and player_alive:
				x, y = p.x, p.y
				for i in range(20):
					particle = Particle(x, y, color, win)
					particle_group.add(particle)
				player_alive = False
				skull_group.empty()

			if player_alive:
				for tile in tile_group:
					collision = tile.check_collision(p)
					if collision and target_tile:
						if tile.is_deadly_tile:
							for i in range(30):
								particle = Particle(x, y, color, win)
								particle_group.add(particle)
							player_alive = False
						if tile.is_target_tile:
							for i in range(10):
								particle = Particle(x, y, color, win)
								particle_group.add(particle)
							score += 1
							if highscore <= score:
								highscore = score

							if len(deadly_tiles_list) > 0:
								tile = deadly_tiles_list.pop()
								tile.color = WHITE
								tile.is_deadly_tile = False
							else:
								for tile in tile_group:
									tile.is_deadly_tile = False

							target_tile = generate_target_tile(color)
						else:
							for i in range(10):
								particle = Particle(x, y, color, win)
								particle_group.add(particle)
							target_tile = generate_target_tile(color)
							generate_deadly_tile(death_color)

			if not player_alive and len(particle_group) == 0:
				game_page = False
				score_page = True

				deadly_tiles_list.clear()

				for tile in tile_group:
					tile.color = random.choice(color_list)
					tile.is_target_tile = False
					tile.is_deadly_tile = False

				final_score = Message(WIDTH // 3, HEIGHT // 2 - 20, 90, f'{score}', score_font, WHITE, win)

		pygame_widgets.update(pygame.event.get())
		display.blit(win, (0, 0))
		clock.tick(FPS)
		pygame.display.update()
	return score




SCREEN = WIDTH, HEIGHT = 488, 800
CENTER = WIDTH // 2, HEIGHT // 2
TILE_Y = 100

pygame.font.init()
pygame.mixer.init()

skull_image = pygame.image.load('Assets/skull.png')
skull_image = pygame.transform.scale(skull_image, (15, 15))


class Tile(pygame.sprite.Sprite):
	def __init__(self, index, type_, win):
		super(Tile, self).__init__()

		self.index = index
		self.type = type_
		self.win = win

		self.width = 20
		self.height = 60
		self.gap = 10
		self.color = (255, 255, 255)
		self.is_target_tile = False
		self.is_deadly_tile = False

		self.x = index * self.width + (index + 2) * self.gap + 9
		if self.type == 1:
			self.y = TILE_Y
		elif self.type == 2:
			self.y = HEIGHT - int(1.5 * TILE_Y)

		self.rect = pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))

	def highlight(self):
		pygame.draw.rect(self.win, (255, 70, 70), (self.x, self.y, self.width, self.height), 2)

	def check_collision(self, p):
		if self.rect.colliderect(p.rect):
			p.x = self.rect.x + self.width // 2
			if self.type == 1:
				p.y = TILE_Y + self.height + p.radius + 1
			elif self.type == 2:
				p.y = HEIGHT - int(1.5 * TILE_Y) - p.radius

			p.dx = p.dy = 0
			p.can_move = True
			p.tile_type = self.type

			if not p.first_tile:
				p.first_tile = True

			return True

		return False

	def update(self):
		pygame.draw.rect(self.win, (12, 12, 12), (self.x + 3, self.y + 3, self.width, self.height))
		self.rect = pygame.draw.rect(self.win, self.color, (self.x, self.y, self.width, self.height))

		if self.is_deadly_tile:
			self.win.blit(skull_image, (self.x + self.width // 2 - 8, self.y + self.height // 2 - 8))


class Player:
	def __init__(self, win, tile_group):
		self.win = win
		self.tile_group = tile_group
		self.reset()
		self.reset_path_variables()

	def reset(self):
		self.radius = 10
		self.shadow_radius = 20
		self.first_tile = False

		self.x = WIDTH + 10
		self.y = HEIGHT // 2 - 100
		self.vel = 8
		self.tile_type = None

		self.counter = 0
		self.dr = 1
		self.dx = self.dy = 0
		self.can_move = True
		self.new_tile = True
		self.index = None

		self.set_move(159, HEIGHT - int(1.5 * TILE_Y), 4)
		self.rect = pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), 10)

	def reset_path_variables(self):
		self.path_d = 10
		self.path_di = 1
		self.path_index = -1

		self.path_points = []
		self.path_counter = 0

		self.path_x = 0
		self.path_y = 0

	def get_path_direction(self):
		self.path_points.clear()
		if self.tile_type == 1:
			index = 2 * self.path_index + 1
			self.path_y = HEIGHT - int(1.5 * TILE_Y)
		else:
			index = 2 * self.path_index
			self.path_y = TILE_Y + 60
		self.path_target_tile = self.tile_group.sprites()[index]
		self.path_x = self.path_target_tile.rect.centerx

		dx = self.path_x - self.x
		dy = self.path_y - self.y
		angle = math.atan2(dy, dx)
		thetax = math.cos(angle)
		thetay = math.sin(angle)

		for i in range(5):
			pointx = self.x + thetax * self.path_d * i
			pointy = self.y + thetay * self.path_d * i
			self.path_points.append((pointx, pointy))

	def draw_path(self, color):
		if self.path_index == -1:
			self.path_index = self.index
			self.get_path_direction()

		self.path_counter += 1
		if self.path_counter % 10 == 0:
			self.path_index += self.path_di
			if self.path_index > 7:
				self.path_index = 6
				self.path_di *= -1
			if self.path_index < 0:
				self.path_index = 1
				self.path_di *= -1

			self.get_path_direction()

		for index, point in enumerate(self.path_points):
			pygame.draw.circle(self.win, color, point, 5 - index)

	def update(self, color, player_alive):
		if player_alive:
			if self.can_move:
				self.draw_shadow()
				self.draw_path(color)

			self.x += self.dx * self.vel
			self.y += self.dy * self.vel

			self.rect = pygame.draw.circle(self.win, color, (self.x, self.y), self.radius)
			pygame.draw.circle(self.win, (255, 255, 255), (self.x, self.y), 6)
			pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), 3)

	def draw_shadow(self):
		pygame.draw.circle(self.win, (12, 12, 12), (self.x, self.y), self.shadow_radius)
		self.counter += 1
		if self.counter % 5 == 0:
			self.shadow_radius += self.dr
			if self.shadow_radius >= 25 or self.shadow_radius <= 16:
				self.dr *= -1

	def set_move(self, x, y, index):
		if self.can_move:
			self.index = index
			dx = x - self.x
			dy = y - self.y
			angle = math.atan2(dy, dx)
			self.dx = math.cos(angle)
			self.dy = math.sin(angle)

			self.can_move = False
			self.new_tile = False
			self.path_index = -1


class SkullCircle(pygame.sprite.Sprite):
	def __init__(self, x, y, type_, color, win):
		super(SkullCircle, self).__init__()

		self.x = x
		self.y = y
		self.type = type_
		self.color = color
		self.win = win

		self.angle = 0
		self.image = skull_image
		self.rect = self.image.get_rect(center=(self.x, self.y))

		if self.type == 1:
			self.dx = 1
			self.dtheta = -2
		elif self.type == 2:
			self.dx = -1
			self.dtheta = 2

	def rotate(self):
		image = pygame.transform.rotate(self.image, self.angle)
		rect = image.get_rect(center=self.rect.center)

		return image, rect

	def update(self):
		self.rect.x += self.dx
		if self.rect.x < -10 or self.rect.x > WIDTH + 10:
			self.kill()

		self.angle += self.dtheta
		image, self.rect = self.rotate()

		pygame.draw.circle(self.win, self.color, (self.rect.centerx + 1, self.rect.centery), 9)
		self.win.blit(image, self.rect)


class Particle(pygame.sprite.Sprite):
	def __init__(self, x, y, color, win):
		super(Particle, self).__init__()
		self.x = x
		self.y = y
		self.color = color
		self.win = win
		self.size = random.randint(4, 7)
		xr = (-3, 3)
		yr = (-3, 3)
		f = 2
		self.life = 40
		self.x_vel = random.randrange(xr[0], xr[1]) * f
		self.y_vel = random.randrange(yr[0], yr[1]) * f
		self.lifetime = 0

	def update(self):
		self.size -= 0.1
		self.lifetime += 1
		if self.lifetime <= self.life:
			self.x += self.x_vel
			self.y += self.y_vel
			s = int(self.size)
			pygame.draw.rect(self.win, self.color, (self.x, self.y, s, s))
		else:
			self.kill()


class Message:
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


class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()

		self.scale = scale
		self.image = pygame.transform.scale(img, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action