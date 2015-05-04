from __future__ import division
import sys
import math 
import pygame
import random


# colour globals

AQUA = (100,200,200)
LAV = (100,100,200)
PEA = (100,200,100)
CORAL = (200,100,100)


class pgmeMain(object):
	def __init__(self):

		pygame.init()
		self.width = 800
		self.height = 600
		self.screen = pygame.display.set_mode((self.width, self.height))
	
		self.FPS = 30
		self.REFRESH = pygame.USEREVENT+1
		pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

		#list of vertices for drawing on the screen
		self.listOfVertices = []

		#adjacency list for graph representation
		self.adjacent = []

		#vertex list 
		self.vList = [(100,100),(300,500),(500,300)]
		
		#adjacency list. 
		# First list index corresponds to the vertex at the 
		# same index in the vertex list	

		self.aList = [[self.vList[1],self.vList[2]], \
			[self.vList[0],self.vList[2]],[self.vList[0],self.vList[1]]]


		#after initialization, run the main program loop
		self.event_loop()
	
	def event_loop(self):

		while True:
			event = pygame.event.wait()
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == self.REFRESH:
				self.draw()
			else:
				pass
	

	def draw(self):
		self.screen.fill((0,0,0))
		
		for i in self.vList:
				pygame.draw.circle(self.screen,AQUA,i,10)

		
		# Draw the edges of adjacent vertecies:
		# Draw a line from the ith vertex in the list
		# to each of the vertexes listed in the corresponding
		vIndexCount = 0
		for i in self.aList:
			for j in i:
				pygame.draw.line(self.screen,LAV,self.vList[vIndexCount],j, 2)
			vIndexCount += 1
		

		pygame.display.flip()
pgmeMain()
