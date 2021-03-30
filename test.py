import pygame
import os
pygame.font.init()
pygame.mixer.init()
pygame.display.init()

# RESULATION,WINDOW SETTINGS
FPS = 60
WIDTH, HEIGHT = 1920, 1080
IMG_WIDTH, IMG_HEIGHT = 101, 151
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Save the Asude")

# INITIALIZING IMAGES
BATU_RAW = pygame.image.load(os.path.join("assets", "batur.png"))
UMUT_RAW = pygame.image.load(os.path.join("assets", "umut.jpg"))
BACKGROUND_RAW = pygame.image.load(os.path.join("assets", "background.jpg"))
BATU = pygame.transform.scale(BATU_RAW, (IMG_WIDTH,IMG_HEIGHT))
UMUT = pygame.transform.scale(UMUT_RAW, (IMG_WIDTH,IMG_HEIGHT))
BACKGROUND = pygame.transform.scale(BACKGROUND_RAW, (WIDTH,HEIGHT))
PLATFORM_RAW = pygame.image.load(os.path.join("assets", "platform.png"))

# INITIALIZING FONTS
## HIT = pygame.USEREVENT + 1
HP_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

# INITIALIZING SOUNDS
BRUH_SOUND = pygame.mixer.Sound(os.path.join("assets", "bruh.wav"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("assets", "hitsound.wav"))

# COLORS
WHITE = (255, 255, 255)
RED = (255,0,0)
BLACK = (0,0,0)

class Player(object):
	"""docstring for Player"""

	def __init__(self, width, height, x, y):
		super().__init__()
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.Velocity = 5
		self.jumpValue, self.fallValue = 20, 1
		self.jumping = False
		self.falling = False
		self.img = BATU
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.collide_list = []

	def update(self, platform_group):
		self.rect.x = self.x
		self.rect.y = self.y

		if (self.jumping):
			if (self.jumpValue > 0):
				self.y -= self.jumpValue
				self.jumpValue -= 1
			else:
				self.jumpValue = 20
				self.jumping = False
				self.falling = True

		elif (self.falling and not self.collide_list):
			if (self.fallValue <= 5):
				self.y += self.fallValue
				self.fallValue += 1
			if (self.fallValue > 5):
				self.y += 5
				self.jumping = False
				self.falling = True

		# if the player on air
		elif (self.y + 5 + IMG_HEIGHT -5 <= 1080 and not self.collide_list):
			self.y += 5
			self.falling = True
			self.jumping = False

		# if the player on ground or platform
		elif (self.collide_list):
			self.falling = False
			self.jumping = False
			if (self.rect.bottom == self.collide_list[0].rect.top):
				self.rect.bottom = self.collide_list[0].rect.top
				

	def draw(self):
		screen.blit(self.img, (self.x, self.y))

	def move_left(self):
		if (self.x - self.Velocity >= 0):
			self.x -= self.Velocity

	def move_right(self):				#   1770
		if (self.x + self.Velocity <= 1920-IMG_WIDTH+1):
			self.x += self.Velocity
	
	def jump(self):
		self.jumping = True
		self.falling = False

			
	

class Platform(object):
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
		screen.blit(self.img, (self.x, self.y))

def draw_window(batu,platform_group):
	screen.blit(BACKGROUND, (0,0))
	for platform in platform_group:
		platform.draw()
	batu.update(platform_group)
	batu.draw()
	pygame.display.update()

def start_menu():
	pass

def main():
	run = True
	clock = pygame.time.Clock()
	batu = Player(IMG_WIDTH, IMG_HEIGHT, 0, 1080-IMG_HEIGHT-530)
	ground = Platform(1920, 30, 0, 1080-30)
	platform1 = Platform(200, 30, 300, 950)
	platform_group = [ground,platform1]
	while (run):
		clock.tick(FPS)
		draw_window(batu,platform_group)
		
		keys_pressed = pygame.key.get_pressed()
		# Horizantally movement
		if (keys_pressed[pygame.K_a]):
			batu.move_left()
		elif (keys_pressed[pygame.K_d]):
			batu.move_right()

		# Check collide to platform
		for platform in platform_group:
			if (batu.rect.colliderect(platform) and platform not in batu.collide_list):
				batu.collide_list.append(platform)
			elif(not batu.rect.colliderect(platform)) and platform in batu.collide_list:
				batu.collide_list.remove(platform)

		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				run = False
				pygame.quit()
			
			if (event.type == pygame.KEYDOWN):
				if (event.key == pygame.K_ESCAPE):
					run = False
					pygame.quit()
				
				if (event.key == pygame.K_w or event.key == pygame.K_SPACE):
					print(batu.jumping, batu.falling)
					if not(batu.jumping or batu.falling) and batu.collide_list:
						batu.jump()
						
				if (event.key == pygame.K_d):
					batu.move_right()

if __name__ == '__main__':
	main()