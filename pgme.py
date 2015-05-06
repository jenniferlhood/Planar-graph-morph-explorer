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

class Vertex(object):
	def __init__(self,(x,y)):
		self.xy = (x,y)

class PgmeMain(object):
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
		self.font = pygame.font.Font(fontfile,16)
		msg1 = "mouse left : add/move vertex  |  mouse right : connect vertex  "
		msg2 = "| c : clone "
		msg3 =	"|  s : switch graph  |  d : delete  |  m : morph "
		self.controls = self.font.render(msg1+msg2+msg3,True, CHALK)
		
		
		# current graph variables (g1 or g2)
		self.current_graph = 1 #(1 for g1 or 2 for g2)
		self.gwidth = [0,self.width/2]
		
	
		#vertex and edge variables 
		#vertex list 
		self.v_list1 = [Vertex((10,10)),Vertex((100,300)),Vertex((90,20))]
		self.v_list2 = []
		 
		#adjacency list. 
		# First list index corresponds to the vertex at the 
		# same index in the vertex list	

		self.a_list1 = [[self.v_list1[1],self.v_list1[2]], \
			[self.v_list1[0],self.v_list1[2]],[self.v_list1[0],self.v_list1[1]]]
		self.a_list2 = []
		
		
		# selected vertex 
		self.selected_index = None
		self.move_vertex = False
	
	
		#after initialization, run the main program loop
		self.event_loop()
	
	def event_loop(self):

		while True:

			event = pygame.event.wait()
			pos = pygame.mouse.get_pos()
		

			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:

				pressed = pygame.mouse.get_pressed()
		
				#for a left click, add a vertex at the clicked coordinate (in the primary window)
								
				if pressed ==  (1,0,0) and self.gwidth[0] < pos[0] < self.gwidth[1]\
						 and 0 < pos[1] < self.height-20:
					
					if self.selected_index is None and self.current_graph == 1: #add move vertex to current_graph 
						add = True

						# when a space without a vertex is clicked, a new vertex is 
						# created. Otherwise, the vertex can be moved.	
						for i in self.v_list1:
							if ((i.xy[0] - 10) < pos[0] < (i.xy[0] + 10)) and \
								((i.xy[1] - 10) < pos[1] < (i.xy[1] + 10)):
								add = False
								self.selected_index = self.v_list1.index(i)
								self.move_vertex = True

						if add:
							self.v_list1.append(Vertex(pos))
							self.a_list1.append([])
					
					elif self.selected_index is None and self.current_graph == 2:
						for i in self.v_list2:
							if ((i.xy[0] - 10) < pos[0] < (i.xy[0] + 10)) and \
								((i.xy[1] - 10) < pos[1] < (i.xy[1] + 10)):
								add = False
								self.selected_index = self.v_list2.index(i)
								self.move_vertex = True

				elif pressed == (0,0,1) and self.gwidth[0] < pos[0] < self.gwidth[1]\
					 and 0 < pos[1] < self.height-20 and self.current_graph == 1:	

					for i in self.v_list1:
						if (i.xy[0] - 10) < pos[0] < (i.xy[0] + 10) and \
								(i.xy[1] - 10) < pos[1] < (i.xy[1] + 10):
							
							if self.selected_index is None:
								self.selected_index = self.v_list1.index(i)

							elif self.selected_index is not None and self.v_list1[self.selected_index] != i\
									 and i not in self.a_list1[self.selected_index]:
			
								self.a_list1[self.selected_index].append(i)
								self.selected_index = None

		
			#when a moved vertex is "dropped"
			elif event.type == pygame.MOUSEBUTTONUP:

							
				if pressed == (1,0,0) and self.move_vertex and \
						self.gwidth[0] < pos[0] < self.gwidth[1] and \
						0 < pos[1] < self.height-20:
					
					if self.current_graph == 1:
						self.v_list1[self.selected_index].xy = pos
						self.selected_index = None
						self.move_vertex = False
					else:
						self.v_list2[self.selected_index].xy = pos
						self.selected_index = None
						self.move_vertex = False

	
					
	#		elif pressed == (1,0,0) and self.current_graph ==2:
	#				for i in self.v_list2:
	#					if (i.xy[0] - 10) < pos[0] < (i.xy[0] + 10) and \
	#						(i.xy[1] - 10) < pos[1] < (i.xy[1] + 10):
	#						print "yes G2"
	#						
	#						if self.selected_index is None:
	#							self.selected_index = self.v_list2.index(i)
	#						elif self.selected_index is not None and self.v_list2[self.selected_index] != i\
	#							 and i not in self.a_list2[self.selected_index]:
											
	#							self.a_list2[self.selected_index].append(i)
	#							self.selected_index = None		
										
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
				self.v_list1 = []
				self.a_list1 = []
				
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:

				if self.current_graph == 1:
					self.gwidth = [self.width/2,self.width]
					self.current_graph = 2
					self.selected_index = None

				elif self.current_graph == 2:
					self.gwidth = [0,self.width/2]
					self.current_graph = 1
					self.selected_index = None
			
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
				if self.current_graph == 1 and self.v_list1 != []:
					self.v_list2 = []
					self.a_list2 = []
					indexCount = 0
					
					for i in self.v_list1:
						g2v = (i.xy[0]+int(self.width/2),i.xy[1])
						self.v_list2.append(Vertex(g2v))
						self.a_list2.append([])

					for i in self.v_list2:					
						for j in self.a_list1[indexCount]:
							self.a_list2[indexCount].append(self.v_list2[self.v_list1.index(j)])

						indexCount += 1
							
			elif event.type == self.REFRESH:
				self.draw()
			else:
				pass
	

	def draw(self):
		self.screen.fill((0,0,0))
				
		self.draw_board()
	
		self.draw_graphs()

		
		pygame.display.flip()

	def draw_board(self):
		#draw the primary and secondary view
		rect_g1 = (0,0,self.width/2-2,self.height-20)
		rect_g2 = (self.width/2,0,self.width/2-2,self.height-20)
		
		if self.current_graph == 1:
			pygame.draw.rect(self.screen,SUN,rect_g1,4)
			pygame.draw.rect(self.screen,GOOSE,rect_g2,4)
		elif self.current_graph == 2:
			pygame.draw.rect(self.screen,GOOSE,rect_g1,4)
			pygame.draw.rect(self.screen,SUN,rect_g2,4)

		# draw controls
		rect = self.controls.get_rect()
		rect = rect.move(5,self.height-20)
		self.screen.blit(self.controls,rect)



	def draw_graphs(self):
		pos = pygame.mouse.get_pos()


		if self.current_graph == 1 and self.selected_index is not None:
			selected_vertex = self.v_list1[self.selected_index]
		elif self.current_graph == 2 and self.selected_index is not None:
			selected_vertex = self.v_list2[self.selected_index]
		elif self.selected_index is None:
			selected_vertex = None
		
		#draw the vertices,
		# if one in the list is the selected vertex, draw it a different colour,
		# or draw it moving with the cursor.
		for i in self.v_list1:
			if i is not selected_vertex:
				pygame.draw.circle(self.screen,AQUA,i.xy,8)
			else:
				if pygame.mouse.get_pressed() ==(1,0,0) and self.move_vertex:
					pygame.draw.circle(self.screen,PEA,pos,8)
				else:
					pygame.draw.circle(self.screen,PEA,i.xy,8)
					##
					pygame.draw.line(self.screen,CORAL,i.xy,pos,2)
		for i in self.v_list2:
			if i is not selected_vertex:
				pygame.draw.circle(self.screen,AQUA,i.xy,8)
				
			else:
				if pygame.mouse.get_pressed() ==(1,0,0) and self.move_vertex:
					pygame.draw.circle(self.screen,PEA,pos,8)
				else:
					pygame.draw.circle(self.screen,PEA,i.xy,8)
					##
					pygame.draw.line(self.screen,CORAL,i.xy,pos,2)	


		# Draw the edges of adjacent vertecies:
		# Draw a line from the i,jth vertex in the a_list 
		# to each of the vertexes listed in the corresponding ith vertex in the v_list
		vIndexCount = 0

		for i in self.a_list1:
			
			for j in i:
				if j is not selected_vertex and self.v_list1[vIndexCount] is not selected_vertex:
					
						pygame.draw.line(self.screen,LAV,self.v_list1[vIndexCount].xy,j.xy, 2)
				else:
					for j in self.a_list1[self.selected_index]:
						pygame.draw.line(self.screen,LAV,pos,j.xy, 2)
			vIndexCount += 1
			
		vIndexCount = 0	
		for i in self.a_list2:
			
			for j in i:
				if j is not selected_vertex and self.v_list2[vIndexCount] is not selected_vertex:
					
						pygame.draw.line(self.screen,LAV,self.v_list2[vIndexCount].xy,j.xy, 2)
				else:
					for j in self.a_list2[self.selected_index]:
						pygame.draw.line(self.screen,LAV,pos,j.xy, 2)
			vIndexCount += 1

		

PgmeMain()
