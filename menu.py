import pygame
import test
import select
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



# COLORS
WHITE = (255, 255, 255)
RED = (255,0,0)
BLACK = (0,0,0)


def draw_menu(buttons):
	screen.blit(BACKGROUND, (0,0))
	for button in buttons:
		button.draw()
	pygame.display.update()

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


def main():
	run = True
	clicking = False
	clock = pygame.time.Clock()
	playbutton = Button(150, 400, 100, BLACK, "Play")
	settingsbutton = Button(150, 500, 100,BLACK,"Settings")
	quitbutton = Button(150, 600, 100,BLACK,"Quit")
	buttons = [playbutton,settingsbutton,quitbutton]
	while (run):
		clock.tick(FPS)
		draw_menu(buttons)
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				run = False
				pygame.quit()
			
			if (event.type == pygame.KEYDOWN):
				if (event.key == pygame.K_ESCAPE):
					run = False
					pygame.quit()
			if (event.type == pygame.MOUSEBUTTONDOWN):
				# Left click = 1
				# Middle click = 2
				# Right click = 3
				# Scroll up = 4
				# Scroll down = 5
				if (event.button == 1):
					clicking = True
			
			if (event.type == pygame.MOUSEBUTTONUP):
				if (event.button == 1):
					mloc = pygame.mouse.get_pos()
					clicked_rects = [b for b in buttons if b.rect.collidepoint(mloc)]
					
					# Play button 
					if (clicked_rects and clicked_rects[0] == playbutton):
						select.main()

					# Settings button
					elif (clicked_rects and clicked_rects[0] == settingsbutton):
						pass

					# Quit Button
					elif (clicked_rects and clicked_rects[0] == quitbutton):
						pygame.quit()
		
					clicking = False

if __name__ == '__main__':
	main()