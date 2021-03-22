import pygame
import os
pygame.font.init()
pygame.mixer.init()
pygame.display.init()

# RESULATION,WINDOW SETTINGS
FPS = 120
WIDTH, HEIGHT = 1920, 1080
IMG_WIDTH, IMG_HEIGHT = 100, 100
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Tam liste")

# INITIALIZING IMAGES
BATU_RAW = pygame.image.load(os.path.join("assets", "batu.jpg"))
UMUT_RAW = pygame.image.load(os.path.join("assets", "umut.jpg"))
BACKGROUND_RAW = pygame.image.load(os.path.join("assets", "background.jpg"))
BATU = pygame.transform.scale(BATU_RAW, (IMG_WIDTH,IMG_HEIGHT))
UMUT = pygame.transform.scale(UMUT_RAW, (IMG_WIDTH,IMG_HEIGHT))
BACKGROUND = pygame.transform.scale(BACKGROUND_RAW, (WIDTH,HEIGHT))

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

# INTS
BATU_VEL = 5
BATU_JUMPVALUE = 20
BATU_FALLVALUE = 20
ISJUMP = False
CANJUMP = False

def handle_movement(keys_pressed, batu, ISJUMP, BATU_JUMPVALUE):
	#if batu.y + 1 <= (HEIGHT-IMG_HEIGHT+1):
		#batu.y += 1
	if (keys_pressed[pygame.K_a] and batu.x - BATU_VEL > 0): #left
		batu.x -= BATU_VEL
	if (keys_pressed[pygame.K_d] and batu.x + BATU_VEL < (WIDTH-IMG_WIDTH)): #right
		batu.x += BATU_VEL
	#if (keys_pressed[pygame.K_w] and batu.y - BATU_VEL > 0): #jump
		#ISJUMP = True
	#if (keys_pressed[pygame.K_s] and batu.y + 1 <= (HEIGHT-IMG_HEIGHT)): #down
		#batu.y += 1

def draw_window(batu):
	WIN.blit(BACKGROUND, (0,0))
	WIN.blit(BATU, (batu.x, batu.y))
	WIN.blit(UMUT, (1920-IMG_WIDTH,1080/2 - IMG_HEIGHT/2))
	pygame.display.update()


def main(ISJUMP, BATU_JUMPVALUE, CANJUMP, BATU_FALLVALUE):
	run = True
	clock = pygame.time.Clock()
					#     position 0,980            	  size
	batu = pygame.Rect(0,1080-IMG_HEIGHT,  IMG_WIDTH, IMG_HEIGHT)
	ground = pygame.Rect(0, 1079, 1920, 1)
	
	while (run):
		clock.tick(FPS)
		keys_pressed = pygame.key.get_pressed()
		
		
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				run = False
				pygame.quit()
			if (event.type == pygame.KEYDOWN):
				if (event.key == pygame.K_ESCAPE):
					run = False
					pygame.quit()
				if (event.key == pygame.K_w):
					if (batu.colliderect(ground) and ISJUMP == False):
						CANJUMP = True
				if (event.type == pygame.K_s):
					if (keys_pressed[pygame.K_s] and batu.y + 1 <= (HEIGHT-IMG_HEIGHT)): #down
						batu.y += 1

		if (CANJUMP):
			ISJUMP = True
			acceleration = 1
			if (BATU_JUMPVALUE > 0):
				batu.y -= BATU_JUMPVALUE
				BATU_JUMPVALUE -= acceleration
			elif (BATU_FALLVALUE > 0):
				batu.y += BATU_FALLVALUE
				BATU_FALLVALUE -= acceleration
			else:
				CANJUMP = False
				ISJUMP = False
				BATU_JUMPVALUE, BATU_FALLVALUE = 20,20
						
		handle_movement(keys_pressed, batu, ISJUMP, BATU_JUMPVALUE)
		draw_window(batu)
		
	main(ISJUMP, BATU_JUMPVALUE, CANJUMP, BATU_FALLVALUE)

if __name__ == '__main__':
	main(ISJUMP, BATU_JUMPVALUE, CANJUMP, BATU_FALLVALUE)