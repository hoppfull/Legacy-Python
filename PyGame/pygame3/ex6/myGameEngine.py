import pygame as pg
from pygame.locals import KEYUP, K_ESCAPE, QUIT, MOUSEBUTTONUP, MOUSEMOTION

class GameEngine:
	def __init__(self, size = (640, 480), fps = 1):
		pg.init()
		self.size, self.fps = size, fps
		self.screen = pg.display.set_mode(self.size)
		
		self.running = True
		
	def mainLoop(self):
		while(self.running):
			self.inputEvents()
			self.update()
			self.draw()
			pg.display.flip()
			pg.time.Clock().tick(self.fps)
	
	def inputEvents(self):
		for events in pg.event.get():
			if(events.type == QUIT): #trigger if user press the x on the top right corner of the program window
				self.running = False
			elif(events.type == KEYUP and events.key == K_ESCAPE): #trigger if user press escape
				self.running = False
			elif(events.type == MOUSEBUTTONUP): #trigger if user press any mousebutton and if user move the mouse
				self.mouseUp(events.button, events.pos)
			elif(events.type == MOUSEMOTION): #trigger if user press and hold any mousebutton while and if the user move the mouse
				self.mouseMotion(events.buttons, events.pos, events.rel)

	def mouseUp(self, button, pos):
		pass
	
	def mouseMotion(self, buttons, pos, rel):
		pass
		
	def update(self):
		pass
	
	def draw(self):
		pass