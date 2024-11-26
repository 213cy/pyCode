import pygame
import random

#define game variables
FPS = 30
COEF_SPEED = 0.2 # 
PIPEGAPSIZE = 150

pygame.init()
# ===================================
#load images
IMAGES = {
		'bg':    'assets/bg.png',
		'ground':    'assets/ground.png',
		'bird1':    'assets/bird1.png',
		'bird2':    'assets/bird2.png',
		'bird3':    'assets/bird3.png',
		'pipe1':    'assets/pipe.png',
		'restart':    'assets/restart.png'
}
for n,p in IMAGES.items():
	IMAGES[n]= pygame.image.load(p)
IMAGES['pipe2']  = pygame.transform.flip(IMAGES['pipe1'], False, True)


img_height = 936
img_width = 864
img_height = IMAGES['bg'].get_height() + IMAGES['ground'].get_height()
img_width = IMAGES['bg'].get_width()
pipe_width = IMAGES['pipe1'].get_width()
# my screen resolution : (1280, 800)
# so set window height to 680
k = 680 / img_height
SCREENHEIGHT = int( k*img_height ) # 680
SCREENWIDTH = int( k*img_width ) # 627
GROUND_Y = int( k* IMAGES['bg'].get_height() ) + 1
PIPE_DISTANCE = int( 5 * k * pipe_width )

BIRD_X = SCREENWIDTH // 4 
SCROLL_SPEED = int( COEF_SPEED * SCREENWIDTH / FPS )

for n,img in IMAGES.items():
	w,h = img.get_size()
	IMAGES[n] = pygame.transform.scale(img, (k*w,k*h))

for n in ('bird1','bird2','bird3'):
	img = IMAGES[n].copy()
	pxarray = pygame.PixelArray( img )
	pxarray.replace((249, 58, 28), (249, 241, 36), distance=0.2, weights=(0.8, 0.1, 0.1) )
	pxarray.close()
	# IMAGES['bird1_b'] = pxarray.make_surface()
	IMAGES[f'{n}_b'] = img

# ===================================
# sounds
pygame.mixer.music.load('assets/bgm.mp3')
# pygame.mixer.music.play(-1)
SOUNDS = {}
SOUNDS['hit'] = pygame.mixer.Sound('assets/hit.wav')
SOUNDS['point'] = pygame.mixer.Sound('assets/point.wav')
SOUNDS['wing'] = pygame.mixer.Sound('assets/wing.wav')
# SOUNDS['hit'].play()

# =======================================
# =======================================


class Bird(pygame.sprite.Sprite):
	# 若 bird 以加速度 acc 自由落体至速度 vel_step,
	# 耗时 t,其间 bird 水平移动 L,垂直位移为 S
	# 则有	vel_step = acc * t = acc *(L/SCROLL_SPEED)
	# 经观察 bird 一次跳跃跳过 半个 PIPE_DISTANCE 
	# 此时 	    跳高为 S =  4/4.5 * PIPE_DISTANCE / 2, 
	# 			管道间隔为 5.5/4.5 * PIPE_DISTANCE / 2
	#            L = PIPE_DISTANCE / 4
	#            t = L/SCROLL_SPEED
	#  则根据 vel_step * t = 2*S  = 2 * 4/4.5*2*L 
	#                   有 vel_step * (L/SCROLL_SPEED)  = 16/4.5*L
	#  根据 acc * t^2 = 2 * 4/4.5*2*L 两端同乘 acc
	#                   有 acc = vel_step^2 / (16/4.5*L)
	vel_step = - 16/4.5 * SCROLL_SPEED
	acc = vel_step * vel_step / (4 * PIPE_DISTANCE / 4.5) 
	images = [IMAGES['bird1'], IMAGES['bird2'], IMAGES['bird3'],
           IMAGES['bird1_b'], IMAGES['bird2_b'], IMAGES['bird3_b']]

	def __init__(self, index=0):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.index = index
		if index > 0:
			self.image_offset = 3
		else:
			self.image_offset = 0
		self.image = self.images[self.image_offset]
		self.rect = self.image.get_rect(center=(BIRD_X ,  SCREENHEIGHT // 2))

		self.alive = True
		self.clicked = False
		self.frame = 0
		self.vel = 0.0

	def update(self):
		if self.rect.bottom < GROUND_Y:
			#apply gravity
			self.vel += self.acc
			self.rect.y = round(self.rect.y + self.vel)
		else:
			self.rect.x -= SCROLL_SPEED
			if self.rect.right < 0:
				self.kill()

		if self.alive == True:
			#jump
			if self.clicked == True:
				SOUNDS['wing'].play()
				self.vel = self.vel_step
				self.clicked = False

			# handle the animation and rotate the bird
			self.frame += 1
			ind = self.frame // 5 % 3 + self.image_offset
			self.image = pygame.transform.rotate(self.images[ind], self.vel * -3)

	def draw(self,surface): # for test
		surface.blit(self.image, self.rect)
		if __name__ == '__main__':
		# if 'game' in globals():
			a = pygame.mask.from_surface(self.image)
			game.screen.blit( a.to_surface() ,(0,0) )
			
	def death(self):
		#point the bird at the ground
		self.image = pygame.transform.rotate(self.images[1 + self.image_offset], -90)
		self.alive = False

	def action(self):
		self.clicked = True

	def reset(self):
		self.alive = True
		self.frame = 0
		self.vel = 0.0
		self.rect = self.image.get_rect(center=(BIRD_X ,  SCREENHEIGHT // 2))

class Pipe(pygame.sprite.Sprite):
	__slot__ = ('affinity',)
	spawnline = SCREENWIDTH - PIPE_DISTANCE
	# 经观察 bird 一次跳跃跳过 半个 PIPE_DISTANCE 
	# 管道间隔为 5.5/4.5 * PIPE_DISTANCE / 2
	pipegapsize =  5.5/4.5 * PIPE_DISTANCE / 2
	ox = SCREENWIDTH 
	def __init__(self, yc, isbottom, linkedpipe = None):
		pygame.sprite.Sprite.__init__(self, self.containers)
		#position variable determines if the pipe is coming from the bottom or top
		#position 1 is from the top, -1 is from the bottom
		self.isbottom = isbottom
		self.reward = False
		self.spawn = False

		if isbottom:
			self.image = IMAGES['pipe1']
			self.rect = self.image.get_rect()
			self.rect.topleft = (Pipe.ox, yc + Pipe.pipegapsize // 2)
		else :
			self.image = IMAGES['pipe2']
			self.rect = self.image.get_rect()
			self.rect.bottomleft = (Pipe.ox, yc - Pipe.pipegapsize // 2)
		
		if linkedpipe is not None:
			self.affinity = linkedpipe
			linkedpipe.affinity = self

	def update(self):
		self.rect.x -= SCROLL_SPEED

		if self.isbottom and (self.spawn is False) and self.rect.left < Pipe.spawnline :
			y = SCREENHEIGHT // 2 + random.randint(-100, 100)
			Pipe(y, False, Pipe(y, True))
			self.spawn = True
		if self.rect.right < 0:
			self.kill()

class Ground(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.image = IMAGES['ground']
		self.rect = self.image.get_rect( top=GROUND_Y )

	def update(self):
		self.rect.left -= SCROLL_SPEED
		if self.rect.right  < SCREENWIDTH+1:
			self.rect.left = 0

class Button:

	def __init__(self):
		self.image = IMAGES['restart']
		self.rect = self.image.get_rect(center=(SCREENWIDTH // 2 , SCREENHEIGHT // 2  ) )

	def ispressed(self):
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			return True
		else:
			return False

	def draw(self,surface):
		surface.blit(self.image, self.rect)

class Game():
	stat = {'init': 0 ,	'wait': 1 ,	'run': 2 ,'end': 3 , 'over': 5 }
	def __init__(self, bird_num = 1, isobserv = False):
		self.isobserv = isobserv
		self.bird_num = bird_num
		self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
		pygame.display.set_caption('Flappy Bird')
		self.state = Game.stat['init']
		self.score = 0

		self.pipe_group = pygame.sprite.Group()
		self.bird_group = pygame.sprite.Group()
		self.ground_group = pygame.sprite.Group()
		self.all_sprites = pygame.sprite.RenderUpdates()

		# assign default groups to each sprite class
		Bird.containers =self.bird_group,self.all_sprites
		Pipe.containers = self.pipe_group,self.all_sprites
		Ground.containers = self.ground_group,self.all_sprites
		# TimedHint.containers = all_sprites

		# self.flappy = Bird()
		self.ground = Ground()
		self.button = Button()

		self.font = pygame.font.SysFont('Bauhaus 93', 60)
		self.clock = pygame.time.Clock()

	def play_step(self , input_actions = None ):
		self.clock.tick(FPS)

		if input_actions is None:
			input_actions = self.bird_num*[0]
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.state = Game.stat['over']
				pygame.quit()	
				return Game.stat['over'], self.score
			if event.type == pygame.MOUSEBUTTONDOWN:
				input_actions[0] = 1


		if self.state == Game.stat['init']:
			if input_actions[0] == 0:
				self.score = 0

				for k in range(1,self.bird_num):
					Bird(k)
				self.flappy = Bird(0)

				for ps in self.pipe_group.sprites():
					ps.kill()
				y = SCREENHEIGHT // 2 + random.randint(-100, 100)
				p = Pipe(y, True)
				Pipe(y, False , p)

				if self.isobserv is False:
					pygame.mixer.music.play(-1)
				self.state = Game.stat['wait']
		elif self.state == Game.stat['wait']:
			if input_actions[0] == 1:
				self.state = Game.stat['run']

		elif self.state == Game.stat['run']:
			for bird in self.bird_group: #.sprites():
				if input_actions[bird.index] == 1:
					bird.action()
				elif input_actions[bird.index] == 5:
					bird.reset()

			self.all_sprites.update()
			
			# look for collision
			def bird_collide(bird,pipe):
				if bird.alive is True:
					if bird.rect.bottom >= GROUND_Y or bird.rect.top < 0 :
						bird.death()
						return True
					elif BIRD_X - 50 < pipe.rect.centerx < BIRD_X +50 :
						if pygame.sprite.collide_mask(bird, pipe):
							bird.death()
							return True
				return False

			# once the bird has hit the ground it's dead
			if pygame.sprite.groupcollide(self.bird_group, self.pipe_group, False, False, bird_collide) :
				SOUNDS['hit'].play()

			#check the self.score
			for pp in self.pipe_group.sprites():
				if pp.isbottom and pp.reward is False :
					if pp.rect.right < self.flappy.rect.left :
						self.score += 1
						SOUNDS['point'].play()
						pp.reward = True

			if len( self.bird_group ) == 0:
				self.state = Game.stat['end']
				pygame.mixer.music.stop()


		elif self.state == Game.stat['end']:
			self.bird_group.update()
			#check mouseover and clicked conditions
			if input_actions[0] == 1:
				if self.button.ispressed():
					self.state = Game.stat['init']


		#draw background
		self.screen.blit(IMAGES['bg'], (0,0))
		self.pipe_group.draw(self.screen)
		self.ground_group.draw(self.screen)
		self.bird_group.draw(self.screen)
		self.flappy.draw(self.screen)

		if self.state == Game.stat['end']:
			self.button.draw(self.screen)
		# output text on screen
		img = self.font.render(str(self.score), True, (220,220,220))
		self.screen.blit(img, (SCREENWIDTH/2, 40))

		# pygame.display.update()
		pygame.display.flip()

		if self.isobserv is True :
			frame_data ={}
			frame_data['bird'] = \
                            [(b.index, b.frame, b.alive, b.rect.centerx, b.rect.centery, b.vel)
                             for b in self.bird_group.sprites()]
			frame_data['pipe'] = \
                            [(p.rect.left, p.rect.right, p.rect.top, p.affinity.rect.bottom)
                             for p in self.pipe_group.sprites() if p.isbottom and not p.reward]

			# image_data = pygame.surfarray.array3d( pygame.display.get_surface() )
			return self.state, frame_data
		else:
			return self.state, self.score 



if __name__ == '__main__':
	game = Game(2)
	while True:
		game_stat, score  = game.play_step()
		if game_stat == Game.stat['over']:
			break

	print('Final Score', score)
	
