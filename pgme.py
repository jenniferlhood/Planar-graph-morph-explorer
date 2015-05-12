from __future__ import division
import sys
import math 
import pygame
import time
import glob

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
		self.width = 1500
		self.height = 700
		self.screen = pygame.display.set_mode((self.width, self.height))
	
		self.FPS = 30
		self.REFRESH = pygame.USEREVENT+1
		pygame.time.set_timer(self.REFRESH, 1000//self.FPS)

		
		
		#program variables
		#fonts
		fontfile = pygame.font.match_font('helvetica')
		self.control_font = pygame.font.Font(fontfile,20)
		self.msg_font = pygame.font.Font(fontfile,40)
			
		self.save_msg = self.msg_font.render("saved",True,CHALK)
		self.load_msg = self.msg_font.render("loaded",True,CHALK)
		
		self.morph_ok_msg = self.msg_font.render("",True,CHALK)
		

		#State switch: Used to communicate board state to user 
		# 0 for normal; 1 to save, 2 for load screen,
		# 3 for load msg, 4 for morph mode
		self.state = 0 
		self.timer = 0

		# save load varables
		# displaying messages
		self.load_list = []
		self.pg_num = 0


		# current graph variables (g1 or g2)
		self.current_graph = 1 #(1 for g1 or 2 for g2)
		self.gwidth = [0,self.width/2]
		
		#vertex and edge variables 
		#vertex list 
		self.v_list1 = []
		self.v_list2 = []
		 
		#adjacency list. 
		# First list index corresponds to the vertex at the 
		# same index in the vertex list	
		self.a_list1 = []
		self.a_list2 = []
		
		
		# selected vertices 
		self.selected_index = None
		self.move_vertex = False

		#morph varbales
		self.morph_ok = False #check for conditions for morph
		self.morph = False #morph mode switch	
		self.morph_time = 3 #time it takes to animate the morph

		self.v_list_vector = [] #a list of caculated morph speed from g1 to g2)

		#after variable initialization, run the main program loop
		self.event_loop()



	#Methods assisiting with program function
	#
	#
	#returns a list with the number of vertices and edges in g1 and in g2
	# in this order: [v_g1,e_g1,v_g2,e_g2]
	def count_v_and_e(self):
		v1 = len(self.v_list1)
		e1 = len(reduce(lambda x,y: x + y, self.a_list1,[]))
		v2 = len(self.v_list2)
		e2 = len(reduce(lambda x,y: x + y, self.a_list2,[]))		
		
		return [v1,e1,v2,e2]

	def v_list_coordinates(self,v_list):
		return [i.xy for i in v_list]

	def a_list_coordinates(self,a_list):
		a_cord = []
		index = 0
		for i in a_list:
			a_cord.append([])
			for j in i:
				a_cord[index].append(j.xy)
			index += 1
		return a_cord


	def load_data(self,select_file):
		f=open(select_file,"r")
		f1=f.readline()
		self.v_list1 = []
		self.a_list1 = []
		self.v_list2 = []
		self.a_list2 = []
	
		#parse the lines and generate v and a lists
		f2 = f.readline() # self.v_list1
		if f2 != '[]\n':
			f2 = f2.rstrip(')]\n')
			f2 = f2.lstrip('[(')
			f2 = f2.split('), (')
			for i in f2:
				j = i.split(', ')
				if j[0] is not '' and j[1] is not '':
					self.v_list1.append(Vertex((int(j[0]),int(j[1]))))
		
		
		f3 = f.readline() #self.a_list1
		if f3 != '[]\n':
			f3 = f3.rstrip(')]]\n')
			f3 = f3.lstrip('[[(')
			f3 = f3.split('], [')
			for i in f3:
				temp_list = []
				l = i.rstrip(')')
				l = l.lstrip('(')
				l = l.split('), (')
				for j in l:
					k = j.split(', ')
					if k[0] is not '' and k[1] is not '':
						temp_list.append(Vertex((int(k[0]),int(k[1]))))
				self.a_list1.append(temp_list)
				
	
		f4 = f.readline() #self.v_list2
		if f4 != '[]\n':
			f4 = f4.rstrip(')]\n')
			f4 = f4.lstrip('[(')
			f4 = f4.split('), (')
	
			for i in f4:
				j = i.split(', ')
				if j[0] is not '' and j[1] is not '':
					self.v_list2.append(Vertex((int(j[0]),int(j[1]))))
	
		f5 = f.readline() #self.a_list2
		if f5 != '[]\n':
			f5 = f5.rstrip(')]]\n')
			f5 = f5.lstrip('[[(')
			f5 = f5.split('], [')
	
			for i in f5:
				temp_list = []
				l = i.rstrip(')')
				l = l.lstrip('(')
				l = l.split('), (')
				for j in l:
					k = j.split(', ')
					if k[0] is not '' and k[1] is not '':
						temp_list.append(Vertex((int(k[0]),int(k[1]))))
				self.a_list2.append(temp_list)
		
		
		self.timer = time.time()
		self.state = 3


	# Main Event handling method
	#
	#
	def event_loop(self):

		while True:

			event = pygame.event.wait()
			pos = pygame.mouse.get_pos()
		
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:

				pressed = pygame.mouse.get_pressed()
		
				#for a left click, 
				# add a vertex at the clicked coordinate (in the primary window)
				# (and only when the loadfile screen isn't displayed)				
				if pressed ==  (1,0,0) and (self.gwidth[0]+10) < pos[0] < \
								(self.gwidth[1]-10) and 0 < pos[1] < self.height-20\
								 and self.state == 0:

					#add move vertex to current_graph
					if self.selected_index is None and self.current_graph == 1:  
						add = True

						# when a space without a vertex is clicked, a new vertex is 
						# created. Otherwise, the vertex can be moved.	
						for i in self.v_list1:
							if ((i.xy[0] - 10) < pos[0] < (i.xy[0] + 10)) and \
								((i.xy[1] - 10) < pos[1] < (i.xy[1] + 10)):
								add = False
								self.move_vertex = True
								self.selected_index = self.v_list1.index(i)
								

						if add:
							self.v_list1.append(Vertex(pos))
							self.a_list1.append([])
					
					elif self.selected_index is None and self.current_graph == 2:
										
						for i in self.v_list2:
							if ((i.xy[0] - 10) < pos[0] < (i.xy[0] + 10)) and \
								((i.xy[1] - 10) < pos[1] < (i.xy[1] + 10)):
								add = False
								self.move_vertex = True
								self.selected_index = self.v_list2.index(i)
								


				elif pressed == (1,0,0) and self.state == 2:
					
					select_file = None
				
					while select_file == None:
						#if there are more than 20 entries, click the down button
						if len(self.load_list) // 20 > 0:
					
					
							if 2*self.width/3 -8 < pos[0] < \
									2*self.width/3 + 8 and 2*self.height/3 - 8 <\
									pos[1] < 2*self.height/3 + 8:
								self.pg_num += 1
						
							
					#click on the desired file
						if self.width/3 < pos[0] < self.width/2 \
								and self.height/3 < pos[1] < 2*self.height/3:
					
							if int(self.pg_num+(pos[1]-40-self.height/3)//20)\
															 < len(self.load_list):
								#######
								print self.load_list[int(self.pg_num+\
										(pos[1]-40-self.height/3)//20)]
								select_file = self.load_list[int(self.pg_num+\
										(pos[1]-40-self.height/3)//20)]
								self.load_data(select_file)
							
						elif self.width/2 < pos[0] < 2*self.width/3	\
								and self.height/3 < pos[1] < 2*self.height/3:
					
							if 10+int(self.pg_num+(pos[1]-40-self.height/3)//20)\
																 < len(self.load_list):
									#######
								print self.load_list[10+int(self.pg_num+\
										(pos[1]-40-self.height/3)//20)]
								select_file = self.load_list[10+int(self.pg_num+\
										(pos[1]-40-self.height/3)//20)]
								self.load_data(select_file)
						else:
							select_file = 0
							self.state = 0	
						#elif len(self.load_list) == 0:
		



			elif event.type == pygame.MOUSEBUTTONUP:

				#when a moved vertex is "dropped", 
				#  update the vertex list and adjacency list
				if pressed == (1,0,0) and self.move_vertex and \
						(self.gwidth[0]+10)< pos[0] < (self.gwidth[1]-10) and \
						0 < pos[1] < self.height-40:
					
					if self.current_graph == 1:
						self.v_list1[self.selected_index].xy = pos
						self.selected_index = None
						self.move_vertex = False
					else:
						self.v_list2[self.selected_index].xy = pos
						self.selected_index = None
						self.move_vertex = False

					
				elif pressed == (0,0,1) and self.current_graph == 1 \
					 and (self.gwidth[0]+10) < pos[0] < (self.gwidth[1]-10) and \
					 0 < pos[1] < self.height-20:
					

					for i in self.v_list1:
						if (i.xy[0] - 10) < pos[0] < (i.xy[0] + 10) and \
								(i.xy[1] - 10) < pos[1] < (i.xy[1] + 10):
							
							if self.selected_index is None:
								self.selected_index = self.v_list1.index(i)

							elif self.selected_index is not None and \
									self.v_list1[self.selected_index] != i\
									and i not in self.a_list1[self.selected_index]:

								self.a_list1[self.selected_index].append(i)
								self.a_list1[self.v_list1.index(i)].append(\
										self.v_list1[self.selected_index])
							
								self.selected_index = None
								# after adding edges to g1 graphs are no longer similar,
								# so morphing cannot occur.								
								self.morph_ok = False 
							else:
								self.selected_index = None
								self.move_vertex = None
				else:
					self.selected_index = None
					self.move_vertex = None

			elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
				self.morph_ok = False
				if self.current_graph == 1:
					self.v_list1 = []
					self.a_list1 = []
				elif self.current_graph ==2:
					self.v_list2 = []
					self.a_list2 = []

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
					#after cloning, the graphs are similar, 
					# thus morphing can happen									
					self.morph_ok = True	
					self.v_list2 = []
					self.a_list2 = []
					index = 0
					
					for i in self.v_list1:
						g2v = (i.xy[0]+int(self.width/2),i.xy[1])
						self.v_list2.append(Vertex(g2v))
						self.a_list2.append([])

					for i in self.v_list2:					
						for j in self.a_list1[index]:
							self.a_list2[index].append(\
									self.v_list2[self.v_list1.index(j)])

						index += 1

				elif self.current_graph == 2 and self.v_list2!= []:
					#after cloning, the graphs are similar, 
					# thus morphing can happen					
					self.morph_ok = True					
					self.v_list1 = []
					self.a_list1 = []
					index = 0
					
					for i in self.v_list2:
						g2v = (i.xy[0]-int(self.width/2),i.xy[1])
						self.v_list1.append(Vertex(g2v))
						self.a_list1.append([])

					for i in self.v_list1:					
						for j in self.a_list2[index]:
							self.a_list1[index].append(\
									self.v_list1[self.v_list2.index(j)])

						index += 1

			elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
				tm = time.localtime(time.time())
				self.timer = time.time()
				
				filename = str(tm.tm_year) + "_" + str(tm.tm_mon) + "_" + \
									str(tm.tm_mday) + "_" + str(tm.tm_hour) + \
									str(tm.tm_min) + str(tm.tm_sec)+".graph"

				f = open(filename,"w")
 				f.write(str(self.count_v_and_e()) + "\n")
				f.write(str(self.v_list_coordinates(self.v_list1)) + "\n")
				f.write(str(self.a_list_coordinates(self.a_list1)) + "\n")
				f.write(str(self.v_list_coordinates(self.v_list2)) + "\n")
				f.write(str(self.a_list_coordinates(self.a_list2)) + "\n")
				f.close()
				self.state = 1

			elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
				#glob to read files into self.load_list
						#determine number of files, can display 20 per page
					self.state = 2
					self.load_list = glob.glob("*.graph")
					
					
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:			
				self.timer= time.time()

				if self.morph_ok:
					self.morph_ok_msg = self.msg_font.render\
								("Morphing G1 to G2",True,CHALK)
					self.calc_morph()					
					self.morph = True

				else:		
					self.morph_ok_msg = self.msg_font.render\
								("No morph: Graphs not simlar",True,CHALK)


				self.state = 4	
			elif event.type == self.REFRESH:
			
				# Draw the interface 
				self.draw()


			else:
				pass
	
	
	def calc_morph(self):
		self.v_list_vector = []

		#Calculate the xy speed vector
		index = 0
		for i in self.v_list1:
		
			dx = (self.v_list2[index].xy[0]-self.width/4)-(i.xy[0]+self.width/4)
			dy = self.v_list2[index].xy[1]-i.xy[1]

			self.v_list_vector.append((dx,dy))
			
			index +=1

	
	#
	# Graphical and interface methods associated with self.draw()	
	#
	#
	def state_msg(self,msg):
		#messages to user regarding program state
			
		rect = self.save_msg.get_rect()
		rect = rect.move(10,self.height-120)
		self.screen.blit(msg,rect)

		if time.time() - self.timer > 2:
			self.state = 0
		

	def load_files(self):
		#load file window
		rect_load = (self.width/3,self.height/3,self.width/3,self.height/3)
		pygame.draw.rect(self.screen,(0,0,0),rect_load)		
		pygame.draw.rect(self.screen,AQUA,rect_load,4)	

		loadmsg = self.control_font.render("select a file",True, AQUA)
		rect = loadmsg.get_rect()
		rect = rect.move(self.width/3+10, self.height/3 + 10)
		self.screen.blit(loadmsg,rect)
		page = len(self.load_list)

		if self.pg_num > page:
			self.pg_num = 0
		move_pos = 40		
		for i in self.load_list[self.pg_num+0:self.pg_num+9]:
				 # list the files under each other
				files = self.control_font.render(i,True, CHALK)
				rect = files.get_rect()
				rect = rect.move(self.width/3+10,self.height/3+move_pos)
				self.screen.blit(files,rect)
				move_pos += 20

		move_pos = 40	
		for i in self.load_list[self.pg_num+10:self.pg_num+19]:
				 # list the files under each other
				files = self.control_font.render(i,True, CHALK)
				rect = files.get_rect()
				rect = rect.move(self.width/2+10,self.height/3+move_pos)
				self.screen.blit(files,rect)
				move_pos += 20

		if page // 20 > 0:
			self.next_pg_button()

		#if there are more than 20 files to diplay, do next screen
	
	def next_pg_button(self):
		x = self.width/3
		y = self.height/3

		pygame.draw.circle(self.screen,PEA,(int(2*x),int(2*y)),10)
		pygame.draw.polygon(self.screen,(0,0,0),\
								((2*x-6,2*y-5),(2*x+6,2*y-5),(2*x,2*y+6)))
	
	def draw_board(self):
		#draw the primary and secondary view
		rect_g1 = (0,0,self.width/2-2,self.height-50)
		rect_g2 = (self.width/2,0,self.width/2-2,self.height-50)
		
		if self.current_graph == 1:
			pygame.draw.rect(self.screen,SUN,rect_g1,4)
			pygame.draw.rect(self.screen,GOOSE,rect_g2,4)
		elif self.current_graph == 2:
			pygame.draw.rect(self.screen,GOOSE,rect_g1,4)
			pygame.draw.rect(self.screen,SUN,rect_g2,4)


		#graw title/description for g1 and g2
		
		title = self.msg_font.render("G1", True, CHALK)
		rect = title.get_rect()
		rect = rect.move(10, 10)
		self.screen.blit(title, rect)
		
		title2 = self.msg_font.render("G2", True, CHALK)
		rect = title.get_rect()
		rect = rect.move((self.width/2)+10, 10)
		self.screen.blit(title2, rect)


		# draw controls
		msg1 = "mouse left : add/move vertex  |  mouse right : connect vertex    "
		msg2 = "|    s : switch graph  |  c : clone current  |  d : delete   "
		msg3 =	"|    f : save to file |  l: load from file   |    m : morph "
		
		controls = self.control_font.render(msg1+msg2+msg3,True, CHALK)
		rect = controls.get_rect()
		rect = rect.move(10,self.height-40)
		self.screen.blit(controls,rect)
	
		


		#messages regarding board state
	def draw_messages(self):
		if self.state == 1:
			self.state_msg(self.save_msg)
		
		elif self.state == 2:
			self.load_files()
			
		elif self.state == 3:
			self.state_msg(self.load_msg)

		elif self.state == 4:
			self.state_msg(self.morph_ok_msg)

		

	def draw_graphs(self):
		pos = pygame.mouse.get_pos()

		#extract the selected vertex
		if self.current_graph == 1 and self.selected_index is not None:
			selected_vertex = self.v_list1[self.selected_index]
		elif self.current_graph == 2 and self.selected_index is not None:
			selected_vertex = self.v_list2[self.selected_index]
		elif self.selected_index is None:
			selected_vertex = None
		
		

		# Draw the edges of adjacent vertecies:
		# Draw a line from the i,jth vertex in the a_list 
		# to each of the vertexes listed in the corresponding
		# ith vertex in the v_list
		
		# when one vertex is being moved, make sure not to draw the edges
		# until it reaches its final destination
		if self.move_vertex:
			index_counter = 0
			for i in self.a_list1:
			
				for j in i:
					if j is not selected_vertex and self.v_list1[index_counter]\
																	 is not selected_vertex:

							pygame.draw.line(self.screen,LAV,self.v_list1[\
														index_counter].xy,j.xy, 2)
					else:
						for j in self.a_list1[self.selected_index]:
							pygame.draw.line(self.screen,LAV,pos,j.xy, 2)
				index_counter += 1
			

			index_counter = 0	
			for i in self.a_list2:
			
				for j in i:
					if j is not selected_vertex and self.v_list2[index_counter]\
																	 is not selected_vertex:
					
							pygame.draw.line(self.screen,LAV,self.v_list2[\
														index_counter].xy,j.xy, 2)
					else:
						for j in self.a_list2[self.selected_index]:
							pygame.draw.line(self.screen,LAV,pos,j.xy, 2)
				index_counter += 1
	
		else:
			index_counter = 0
			for i in self.a_list1:
				for j in i:
					pygame.draw.line(self.screen,LAV,self.v_list1[\
												index_counter].xy,j.xy, 2)

				index_counter += 1

			index_counter = 0
			for i in self.a_list2:
				for j in i:
					pygame.draw.line(self.screen,LAV,self.v_list2[\
												index_counter].xy,j.xy, 2)

				index_counter += 1
		

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
					pygame.draw.line(self.screen,CORAL,i.xy,pos,2)
					
		for i in self.v_list2:
			if i is not selected_vertex:
				pygame.draw.circle(self.screen,AQUA,i.xy,8)
				
			else:
				if pygame.mouse.get_pressed() == (1,0,0) and self.move_vertex:
					pygame.draw.circle(self.screen,PEA,pos,8)
				else:
					pygame.draw.circle(self.screen,PEA,i.xy,8)





	def draw_morph(self):
		rect = (self.width/4,0,self.width/2-2,self.height-50)
		pygame.draw.rect(self.screen,(0,0,0),rect)
		pygame.draw.rect(self.screen,SUN,rect,4)

		elapsed = (time.time() - self.timer) * self.FPS
		total = self.morph_time * self.FPS

		# draw the animated graph
		index = 0
		for i in self.v_list1:
			#calculate this frame's xy depending on the speed vector
			# and the elapsed time			
			dx = int(i.xy[0] + self.width/4 \
					+ self.v_list_vector[index][0]*(elapsed/total))
					
			dy = int(i.xy[1] + self.v_list_vector[index][1]*(elapsed/total))
			
			
			pygame.draw.circle(self.screen,AQUA,(dx,dy),8)
			
			for j in self.a_list1[index]:
				dx_j = int(j.xy[0] + self.width/4 \
					+ self.v_list_vector[self.v_list1.index(j)][0]*(elapsed/total))

				dy_j = int(j.xy[1] + self.v_list_vector[self.v_list1.index(j)][1]*(elapsed/total))
				
				pygame.draw.line(self.screen,LAV,(dx,dy),(dx_j,dy_j), 2)



			
			index += 1
					


		if time.time() - self.timer > self.morph_time:

			self.morph = False
			self.state = 0







	def draw(self):
		self.screen.fill((0,0,0))
		self.draw_board()

		if self.morph:
			self.draw_morph()
		else:
			self.draw_graphs()		
		
		self.draw_messages()
	
				
		pygame.display.flip()





PgmeMain()
