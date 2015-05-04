from __future__ import division
import sys
import math 
import pygame



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

		
		#program variables
		#vertex list 
		self.vList = [(100,100),(300,500),(500,300)]
		
		#adjacency list. 
		# First list index corresponds to the vertex at the 
		# same index in the vertex list	

		self.aList = [[self.vList[1],self.vList[2]], \
			[self.vList[0],self.vList[2]],[self.vList[0],self.vList[1]]]
		
		# selected vertex 
		self.verSelect = None
	
		#after initialization, run the main program loop
		self.event_loop()
	
	def event_loop(self):

		while True:
			event = pygame.event.wait()
		
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				pressed = pygame.mouse.get_pressed()
		
				#for a left click, add a vertex at the clicked coordinate				
				if pressed ==  (0,0,1):
					
					if self.verSelect is None:
						self.vList.append(pos)
						self.aList.append([])
					else:
						self.verSelect = None
				
				elif pressed == (1,0,0):
					
				
				
					for i in self.vList:
						if (i[0] - 10) < pos[0] < (i[0] + 10) and \
							(i[1] - 10) < pos[1] < (i[1] + 10):
						
							i = pygame.mouse.get_pos()
							
				#				if self.verSelect is None:
				#					self.verSelect = self.vList.index(i)
				#				else:
				#					if self.vList[self.verSelect] != i:
				#						self.aList[self.verSelect].append(i)
				#						self.verSelect = None	
					
					
							
			#select two vertices to connect with an edge
			elif event.type == pygame.MOUSEBUTTONUP:		
				if pressed == (1,0,0):
					
					for i in self.vList:
						if (i[0] - 10) < pos[0] < (i[0] + 10) and \
							(i[1] - 10) < pos[1] < (i[1] + 10):
						
								if self.verSelect is None:
									self.verSelect = self.vList.index(i)
								else:
									if self.vList[self.verSelect] != i and i not in\
											self.aList[self.verSelect]:
											
										self.aList[self.verSelect].append(i)
										self.verSelect = None			
			elif event.type == self.REFRESH:
				self.draw()
			else:
				pass
	

	def draw(self):
		self.screen.fill((0,0,0))
		
		for i in self.vList:
				pygame.draw.circle(self.screen,AQUA,i,10)

		
		# Draw the edges of adjacent vertecies:
		# Draw a line from the i,jth vertex in the alist 
		# to each of the vertexes listed in the corresponding ith vertex in the vlist
		vIndexCount = 0
		for i in self.aList:
			for j in i:
				pygame.draw.line(self.screen,LAV,self.vList[vIndexCount],j, 2)
			vIndexCount += 1


			
		#highlight the first selected vertex and draw the prospective edge
		if self.verSelect is not None:
			vertex = self.verSelect
			edge = pygame.mouse.get_pos()
			
			#redraw the selected vertex in a distinct colour
			pygame.draw.circle(self.screen,PEA,self.vList[vertex],8)
			
			#draw the prospective edge in a distinct colour
			pygame.draw.line(self.screen,CORAL,self.vList[vertex],edge,2)


		pygame.display.flip()
pgmeMain()
