from __future__ import division
import sys
import math 
import pygame



# colour globals
LAV = (100,100,200)
PEA = (100,200,100)
CORAL = (200,100,100)

AQUA = (100,200,200)
ROSE = (200,100,200)
SUN = (200,200,100)

GOOSE = (100,100,100)
CHALK = (200,200,200)

class pgmeMain(object):
	def __init__(self):

		pygame.init()
		self.width = 900
		self.height = 500
		self.screen = pygame.display.set_mode((self.width, self.height))
	
		self.FPS = 30
		self.REFRESH = pygame.USEREVENT+1
		pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

		
		
		#program variables
		#font
		fontfile = pygame.font.match_font('helvetica')
		self.font = pygame.font.Font(fontfile,18)
		msg1 = "mouse left : select vertex  |  mouse right : add vertex  "
		msg2 = "| c : clone "
		msg3 =	"|  s : switch graph  |  d : delete  |  m : morph "
		self.controls = self.font.render(msg1+msg2+msg3,True, CHALK)
		
		
		
		# current graph variables (g1 or g2)
		self.gcurrent = 1 #(1 for g1 or 2 for g2)
		self.gwidth = [0,self.width/2]
		
		
		
		
		#vertex and edge variables 
		#vertex list 
		self.vList1 = [(10,10),(100,300),(90,20)]
		self.vList2 = []
		 
		#adjacency list. 
		# First list index corresponds to the vertex at the 
		# same index in the vertex list	

		self.aList1 = [[self.vList1[1],self.vList1[2]], \
			[self.vList1[0],self.vList1[2]],[self.vList1[0],self.vList1[1]]]
		self.aList2 = []
		
		
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
		
				#for a left click, add a vertex at the clicked coordinate (in the primary window)				
				if pressed ==  (0,0,1) and self.gwidth[0] < pos[0] < self.gwidth[1]\
						 and 0 < pos[1] < self.height-20:
					
					
					if self.verSelect is None and self.gcurrent == 1:
						add = True
						for i in self.vList1:
							if ((i[0] - 10) < pos[0] < (i[0] + 10)) and \
									((i[1] - 10) < pos[1] < (i[1] + 10)):
										add = False
						if add == True:
							self.vList1.append(pos)
							self.aList1.append([])
						
					#elif self.verSelect is None and self.gcurrent == 2:
					#	add = True
					#	for i in self.vList2:
					#		if ((i[0] - 10) < pos[0] < (i[0] + 10)) and \
					#				((i[1] - 10) < pos[1] < (i[1] + 10)):
					#					add = False
						
					#	if add == True:
					#		self.vList2.append(pos)
					#		self.aList2.append([])
							
					else:
						self.verSelect = None
				
							
			#select two vertices to connect with an edge
			elif event.type == pygame.MOUSEBUTTONUP:
	
				
				if pressed == (1,0,0) and self.gcurrent == 1:				
					for i in self.vList1:
						if (i[0] - 10) < pos[0] < (i[0] + 10) and \
							(i[1] - 10) < pos[1] < (i[1] + 10):
							
							if self.verSelect is None:
								self.verSelect = self.vList1.index(i)
							elif self.verSelect is not None and self.vList1[self.verSelect] != i\
								 and i not in self.aList1[self.verSelect]:
											
								self.aList1[self.verSelect].append(i)
								self.verSelect = None	

	#		elif pressed == (1,0,0) and self.gcurrent ==2:
	#				for i in self.vList2:
	#					if (i[0] - 10) < pos[0] < (i[0] + 10) and \
	#						(i[1] - 10) < pos[1] < (i[1] + 10):
	#						print "yes G2"
	#						
	#						if self.verSelect is None:
	#							self.verSelect = self.vList2.index(i)
	#						elif self.verSelect is not None and self.vList2[self.verSelect] != i\
	#							 and i not in self.aList2[self.verSelect]:
											
	#							self.aList2[self.verSelect].append(i)
	#							self.verSelect = None		
										
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
				self.vList1 = []
				self.aList1 = []
				
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:

				if self.gcurrent == 1:
					self.gwidth = [self.width/2,self.width]
					self.gcurrent = 2
					self.verSelect = None

				elif self.gcurrent == 2:
					self.gwidth = [0,self.width/2]
					self.gcurrent = 1
					self.verSelect = None
					
			elif event.type == self.REFRESH:
				self.draw()
			else:
				pass
	

	def draw(self):
		self.screen.fill((0,0,0))
				
		#draw the primary and secondary view
		rect_g1 = (0,0,self.width/2-2,self.height-20)
		rect_g2 = (self.width/2,0,self.width/2-2,self.height-20)
		
		if self.gcurrent == 1:
			pygame.draw.rect(self.screen,SUN,rect_g1,4)
			pygame.draw.rect(self.screen,GOOSE,rect_g2,4)
		elif self.gcurrent == 2:
			pygame.draw.rect(self.screen,GOOSE,rect_g1,4)
			pygame.draw.rect(self.screen,SUN,rect_g2,4)

		# draw graph elements
		
		for i in self.vList1:
			pygame.draw.circle(self.screen,AQUA,i,8)
		for i in self.vList2:
			pygame.draw.circle(self.screen,AQUA,i,8)
		
		# Draw the edges of adjacent vertecies:
		# Draw a line from the i,jth vertex in the alist 
		# to each of the vertexes listed in the corresponding ith vertex in the vlist
		vIndexCount = 0
		for i in self.aList1:
			for j in i:
				pygame.draw.line(self.screen,LAV,self.vList1[vIndexCount],j, 2)
			vIndexCount += 1
			
		vIndexCount = 0	
		for i in self.aList2:
			for j in i:
				pygame.draw.line(self.screen,LAV,self.vList2[vIndexCount],j, 2)
			vIndexCount += 1
			
			
		#highlight the first selected vertex and draw the prospective edge
		if self.verSelect is not None:
			vertex = self.verSelect
			edge = pygame.mouse.get_pos()
			
			#redraw the selected vertex in a distinct colour
			if self.gcurrent == 1:
				pygame.draw.circle(self.screen,PEA,self.vList1[vertex],8)
			
				#draw the prospective edge in a distinct colour
				pygame.draw.line(self.screen,CORAL,self.vList1[vertex],edge,2)
			
			elif self.gcurrent == 2:
				pygame.draw.circle(self.screen,PEA,self.vList2[vertex],8)
			
				#draw the prospective edge in a distinct colour
				pygame.draw.line(self.screen,CORAL,self.vList2[vertex],edge,2)
		
		# draw controls
		rect = self.controls.get_rect()
		rect = rect.move(5,self.height-20)
		self.screen.blit(self.controls,rect)
		
		pygame.display.flip()
pgmeMain()
