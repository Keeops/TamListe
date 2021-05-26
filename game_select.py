import game_menu
import game_start
import pygame
import os
pygame.font.init()
pygame.mixer.init()
pygame.display.init()

# RESULATION,WINDOW SETTINGS
FPS = 60
WIDTH, HEIGHT = 1920, 1080
IMG_WIDTH, IMG_HEIGHT = 100, 150
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("Save the Asude")

# INITIALIZING IMAGES
BATU_RAW = pygame.image.load(os.path.join("assets", "batuv2.png"))
UMUT_RAW = pygame.image.load(os.path.join("assets", "duvarciv2.png"))
EMRE_RAW = pygame.image.load(os.path.join("assets", "emov2.png"))
GOKAY_RAW = pygame.image.load(os.path.join("assets", "samurluv2.png"))
BACKGROUND_RAW = pygame.image.load(os.path.join("assets", "background.jpg"))
BATU = pygame.transform.scale(BATU_RAW, (IMG_WIDTH,IMG_HEIGHT))
UMUT = pygame.transform.scale(UMUT_RAW, (IMG_WIDTH,IMG_HEIGHT))
EMRE = pygame.transform.scale(EMRE_RAW, (IMG_WIDTH,IMG_HEIGHT))
GOKAY = pygame.transform.scale(GOKAY_RAW, (IMG_WIDTH,IMG_HEIGHT))
BACKGROUND = pygame.transform.scale(BACKGROUND_RAW, (WIDTH,HEIGHT))
PLATFORM_RAW = pygame.image.load(os.path.join("assets", "platform.png"))
OKSAG_RAW = pygame.image.load(os.path.join("assets", "oksag.png"))
OKSOL_RAW = pygame.image.load(os.path.join("assets", "oksol.png"))
OKSAG = pygame.transform.scale(OKSAG_RAW, (75,50))
OKSOL = pygame.transform.scale(OKSOL_RAW, (75,50))


# COLORS
WHITE = (255, 255, 255)
RED = (255,0,0)
BLACK = (0,0,0)

class Character(object):
	"""docstring for Character"""
	def __init__(self,img,x,y,name):
		super().__init__()
		self.img = img
		self.x = x
		self.y = y
		self.name = name
		self.rect = pygame.Rect(self.x, self.y, IMG_WIDTH, IMG_HEIGHT)
		
	def draw(self,img,x,y):
		screen.blit(self.img, (self.x,self.y))
		
		
class Button(object):
	"""docstring for PlayButton"""
	def __init__(self, x, y, size, color, text):
		super().__init__()
		self.x = x
		self.y = y
		self.size = size
		self.color = color
		self.text = text
		self.Font = pygame.font.SysFont("comicsans", self.size)
		self.Text = self.Font.render(text,1,self.color)
		self.fontwidth = pygame.font.Font.size(self.Font, text)
		self.rect = pygame.Rect(self.x, self.y, self.fontwidth[0], self.fontwidth[1])

	def draw(self):
		screen.blit(self.Text, (self.x, self.y))
		

class Ok(object):
	"""docstring for Ok"""
	def __init__(self, img, x, y):
		super().__init__()
		self.img = img
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, 75, 50)
	
	def draw(self):
		screen.blit(self.img, (self.x,self.y))
		


def draw(character, buttons, oks):
	screen.blit(BACKGROUND, (0,0))
	character.draw(character.img,character.x, character.y)
	for ok in oks:
		ok.draw()
	for button in buttons:
		button.draw()
	pygame.display.update()

def change_character(direction, characters, cur_index):
	if (direction == "R"):
		if (cur_index < len(characters)-1):
			cur_index+=1
	
	elif direction == "L":
		if (cur_index > 0):
			cur_index-=1

	return characters[cur_index], cur_index

def main():
	run = True
	clock = pygame.time.Clock()
	batu = Character(BATU, 900, 550,"batu")
	umut= Character(UMUT, 900, 550,"umut")
	emre = Character(EMRE, 900, 550,"emre")
	gokay = Character(GOKAY, 900, 550,"gokay")
	oksag = Ok(OKSAG, 1050, 600)
	oksol = Ok(OKSOL, 775, 600)
	selectbutton = Button(710, 750, 85, RED, "Select Character")
	buttons = [selectbutton, oksag, oksol]
	oks = [oksag, oksol]
	CHARACTERS = [batu, umut, emre, gokay]
	CUR_CHAR = CHARACTERS[0]
	cur_index = 0
	while (run):
		clock.tick(FPS)
		draw(CUR_CHAR, buttons, oks)
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				run = False
				pygame.quit()
			
			if (event.type == pygame.KEYDOWN):
				if (event.key == pygame.K_ESCAPE):
					run = False
					game_menu.main()

			if (event.type == pygame.MOUSEBUTTONDOWN):
				pass

			if (event.type == pygame.MOUSEBUTTONUP):
				# Left click = 1
				# Middle click = 2
				# Right click = 3
				# Scroll up = 4
				# Scroll down = 5
				if (event.button == 1):
					mloc = pygame.mouse.get_pos()
					clicked_rects = [b for b in buttons if b.rect.collidepoint(mloc)]

					# Play button 
					if (clicked_rects and clicked_rects[0] == selectbutton):
						game_start.main(CUR_CHAR)

					# Right button
					if (clicked_rects and clicked_rects[0] == oksag):
						CUR_CHAR, cur_index = change_character("R", CHARACTERS, cur_index)

					# Left Button
					if (clicked_rects and clicked_rects[0] == oksol):
						CUR_CHAR, cur_index = change_character("L", CHARACTERS, cur_index)
				pass
		

if __name__ == '__main__':
	main()