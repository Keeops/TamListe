import pygame
import select
import menu
import os
pygame.font.init()
pygame.mixer.init()
pygame.display.init()

"""
Bugs:

	Player going through inside the platforms
	Player can jump under the platforms


"""

# RESULATION,WINDOW SETTINGS
FPS = 60
WIDTH, HEIGHT = 1920, 1080
IMG_WIDTH, IMG_HEIGHT = 100, 150
GOAL_WIDTH, GOAL_HEIGHT = 100, 100
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Save the Asude")

# INITIALIZING IMAGES
BATU_RAW = pygame.image.load(os.path.join("assets", "batur.png"))
UMUT_RAW = pygame.image.load(os.path.join("assets", "duvarci.png"))
BACKGROUND_RAW = pygame.image.load(os.path.join("assets", "background.jpg"))
GOAL_RAW = pygame.image.load(os.path.join("assets", "goal.jpg"))
BATU = pygame.transform.scale(BATU_RAW, (IMG_WIDTH,IMG_HEIGHT))
UMUT = pygame.transform.scale(UMUT_RAW, (IMG_WIDTH,IMG_HEIGHT))
GOAL = pygame.transform.scale(GOAL_RAW, (GOAL_WIDTH, GOAL_HEIGHT))
BACKGROUND = pygame.transform.scale(BACKGROUND_RAW, (WIDTH,HEIGHT))
PLATFORM_RAW = pygame.image.load(os.path.join("assets", "platform.png"))

# INITIALIZING FONTS
## HIT = pygame.USEREVENT + 1
HP_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

# INITIALIZING SOUNDS
BRUH_SOUND = pygame.mixer.Sound(os.path.join("assets", "bruhv2.wav"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("assets", "hitsound.wav"))

# COLORS
WHITE = (255, 255, 255)
RED = (255,0,0)
BLACK = (0,0,0)

class Player():
	"""docstring for Player"""

	def __init__(self, img, width, height, x, y):
		super().__init__()
		self.img = img
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.Velocity = 5
		self.jumpValue= 20
		self.jumping = False
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.collide_list = []

	def update(self, platform_group):

		if (self.jumping):
			if self.collide_list and self.collide_list[0].rect.collidepoint(self.rect.x + IMG_WIDTH/2, self.rect.top):
				self.rect.top = self.collide_list[0].rect.bottom
				self.jumpValue = 20
				self.jumping = False
			
			else:
				if (self.jumpValue > 0):
					self.rect.y -= self.jumpValue
					self.jumpValue -= 1
				else: 
					self.jumpValue = 20
					self.jumping = False

		elif (self.collide_list):
			# if the player on ground
			if (self.rect.bottom == self.collide_list[0].rect.top):
				self.rect.bottom = self.collide_list[0].rect.top

			# if the player hits his head
			if (self.rect.top == self.collide_list[0].rect.bottom):
				self.rect.top = self.collide_list[0].rect.bottom
			
			self.jumping = False

		# if the player on air
		elif (self.rect.y + 5 + IMG_HEIGHT <= 1080-25 and not self.collide_list):
			self.rect.y += 5
			self.jumping = False

	def draw(self):
		screen.blit(self.img, (self.rect.x, self.rect.y))

	def move_left(self,platform_group,ground):
		# if the player is on the platform
		if (self.collide_list and (ground not in self.collide_list) and self.rect.bottom == self.collide_list[0].rect.top + 5):
			self.rect.x -= self.Velocity

		# if the player is on the air
		elif (not self.collide_list):
			self.rect.x -= self.Velocity

		# if the player on air and platform is left of the player
		elif (ground not in self.collide_list and self.collide_list):
			if (self.rect.x == self.collide_list[0].rect.right):
				self.rect.x = self.collide_list[0].rect.right

		# if the player on ground and platform is left of the player
		elif (ground in self.collide_list and len(self.collide_list) >= 2):
			if (self.rect.x == self.collide_list[1].rect.right):
				self.rect.x = self.collide_list[1].rect.right
		
		# if the player on the ground
		elif (self.rect.x - self.Velocity <= 1920-IMG_WIDTH+1) and (ground in self.collide_list):
			self.rect.x -= self.Velocity

	def move_right(self,platform_group, ground):
		# if the player is on the platform
		if (self.collide_list and (ground not in self.collide_list) and self.rect.bottom == self.collide_list[0].rect.top + 5):
			self.rect.x += self.Velocity

		# if the player is on the air
		elif (not self.collide_list):
			self.rect.x += self.Velocity

		# if the player on air and platform is right of the player
		elif (ground not in self.collide_list and self.collide_list):
			if (self.rect.x + IMG_WIDTH == self.collide_list[0].rect.left):
				self.rect.x = self.collide_list[0].rect.left - IMG_WIDTH

		# if the player on ground and platform is right of the player
		elif (ground in self.collide_list and len(self.collide_list) >= 2):
			if (self.rect.x + IMG_WIDTH == self.collide_list[1].rect.left):
				self.rect.x = self.collide_list[1].rect.left - IMG_WIDTH
		
		# if the player on the ground
		elif (self.rect.x + self.Velocity <= 1920-IMG_WIDTH+1) and (ground in self.collide_list):
			self.rect.x += self.Velocity

	def jump(self):
		self.jumping = True

class Platform():
	"""docstring for Platform"""
	def __init__(self, width, height, x, y):
		super().__init__()
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.img = pygame.transform.scale(PLATFORM_RAW, (self.width, self.height))
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

	def draw(self):
		screen.blit(self.img, (self.rect.x, self.rect.y))

class Goal():
	"""docstring for Goal"""
	def __init__(self, x, y, img):
		super().__init__()
		self.x = x
		self.y = y
		self.img = img
		self.rect = pygame.Rect(self.x, self.y, GOAL_WIDTH, GOAL_HEIGHT)

	def draw(self):
		screen.blit(self.img, (self.rect.x, self.rect.y))
		

def draw_window(player,platform_group,goal):
	screen.blit(BACKGROUND, (0,0))
	goal.draw()
	for platform in platform_group:
		platform.draw()
	player.update(platform_group)
	player.draw()
	pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, RED)
    screen.blit(draw_text, (WIDTH/2 - draw_text.get_width(), HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main(cur_char):
	run = True
	clock = pygame.time.Clock()
	player = Player(cur_char.img,IMG_WIDTH, IMG_HEIGHT, 0, 1080-IMG_HEIGHT-30)
	ground = Platform(1920, 30, 0, 1080-30)
	platform1 = Platform(200, 30, 300, 950)
	platform2 = Platform(200, 30, 700, 750)
	platform3 = Platform(200, 30, 1100, 550)
	platform4 = Platform(200, 30, 1500, 550)
	platform5 = Platform(200, 30, 1700, 350)
	platform6 = Platform(200, 30, 1200, 150)
	platform7 = Platform(200, 30, 600, 150)
	platform8 = Platform(200, 30, 200, 150)
	goal = Goal(250, 50, GOAL)
	platform_group = [ground,platform1,platform2,platform3,platform4,platform5,platform6,platform7,platform8]
	while (run):
		clock.tick(FPS)
		draw_window(player,platform_group,goal)
		keys_pressed = pygame.key.get_pressed()
		
		# Horizantally movement
		if (keys_pressed[pygame.K_a]):
			player.move_left(platform_group,ground)
		elif (keys_pressed[pygame.K_d]):
			player.move_right(platform_group,ground)

		# Check collide to platform
		for platform in platform_group:
			if (player.rect.colliderect(platform) and platform not in player.collide_list):
				player.collide_list.append(platform)
			elif(not player.rect.colliderect(platform)) and platform in player.collide_list:
				player.collide_list.remove(platform)

		# Check collide to GOAL
		if (player.rect.colliderect(goal)):
			draw_winner("ASUDE SAVED")
			main(cur_char)

		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				run = False
				pygame.quit()
			
			if (event.type == pygame.KEYDOWN):
				if (event.key == pygame.K_ESCAPE):
					run = False
					menu.main()
				
				if (event.key == pygame.K_w or event.key == pygame.K_SPACE):
					if not(player.jumping) and player.collide_list:
						BRUH_SOUND.play()
						player.jump()
						

if __name__ == '__main__':
	main()