import pygame
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

		if (self.jumping):
			if (self.jumpValue > 0):
				self.rect.y -= self.jumpValue
				self.jumpValue -= 1
			else:
				self.jumpValue = 20
				self.jumping = False
				self.falling = True

		elif (self.falling and not self.collide_list):
			if (self.fallValue <= 5):
				self.rect.y += self.fallValue
				self.fallValue += 1
			if (self.fallValue > 5):
				self.rect.y += 5
				self.jumping = False
				self.falling = True

		# if the player on air
		elif (self.rect.y + 5 + IMG_HEIGHT <= 1080-30 and not self.collide_list):
			self.rect.y += 5
			self.falling = True
			self.jumping = False

		# if the player on ground
		elif (self.collide_list):
			if (self.rect.bottom == self.collide_list[0].rect.top):
				self.rect.bottom = self.collide_list[0].rect.top

			self.falling = False
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
				self.falling = True

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
				self.falling = True

		# if the player on ground and platform is right of the player
		elif (ground in self.collide_list and len(self.collide_list) >= 2):
			if (self.rect.x + IMG_WIDTH == self.collide_list[1].rect.left):
				self.rect.x = self.collide_list[1].rect.left - IMG_WIDTH
		
		# if the player on the ground
		elif (self.rect.x + self.Velocity <= 1920-IMG_WIDTH+1) and (ground in self.collide_list):
			self.rect.x += self.Velocity

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
		screen.blit(self.img, (self.rect.x, self.rect.y))






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
	platform2 = Platform(200, 30, 700, 750)
	platform3 = Platform(200, 30, 1100, 550)
	platform4 = Platform(200, 30, 1500, 550)
	platform5 = Platform(200, 30, 1700, 350)
	platform6 = Platform(200, 30, 1200, 150)
	platform7 = Platform(200, 30, 600, 150)
	platform8 = Platform(200, 30, 200, 150)
	platform_group = [ground,platform1,platform2,platform3,platform4,platform5,platform6,platform7,platform8]
	while (run):
		clock.tick(FPS)
		draw_window(batu,platform_group)
		print(batu.rect.right, platform_group[1].rect.left)
		keys_pressed = pygame.key.get_pressed()
		# Horizantally movement
		if (keys_pressed[pygame.K_a]):
			batu.move_left(platform_group,ground)
		elif (keys_pressed[pygame.K_d]):
			batu.move_right(platform_group,ground)

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
					menu.main()
				
				if (event.key == pygame.K_w or event.key == pygame.K_SPACE):
					if not(batu.jumping or batu.falling) and batu.collide_list:
						batu.jump()
						

if __name__ == '__main__':
	main()