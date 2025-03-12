from OpenGL.GL import *
# from OpenGL.GLU import *

import pygame
# from pygame.locals import *

class CursorCube():
    def __init__(self) -> None:
        self.size = 0.4
        self.position= [0,0,0]
        self.last_active_time = pygame.time.get_ticks()

    def update(self, event):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_active_time < 50 :
            return
        self.last_active_time = current_time
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a] :
            self.position[0] -= 1
        elif pressed_keys[pygame.K_d] :
            self.position[0] += 1
        elif pressed_keys[pygame.K_w] :
            self.position[2] -= 1
        elif pressed_keys[pygame.K_s] :
            self.position[2] += 1
        elif pressed_keys[pygame.K_q] :
            self.position[1] += 1
        elif pressed_keys[pygame.K_z] :
            self.position[1] -= 1

    def render(self):
        rr = self.size
        glPushMatrix()
        glTranslatef(*self.position)

        glBegin(GL_QUADS)       
        # 前面
        glColor3f(0.8, 0.0, 0.0)
        glVertex3f(rr, rr, -rr)
        glVertex3f(-rr, rr, -rr)
        glVertex3f(-rr, -rr, -rr)
        glVertex3f(rr, -rr, -rr)
        # 后面
        glColor3f(0.0, 0.8, 0.0)
        glVertex3f(rr, rr, rr)
        glVertex3f(-rr, rr, rr)
        glVertex3f(-rr, -rr, rr)
        glVertex3f(rr, -rr, rr)
        # 顶面
        glColor3f(0.0, 0.0, 0.8)
        glVertex3f(rr, rr, -rr)
        glVertex3f(-rr, rr, -rr)
        glVertex3f(-rr, rr, rr)
        glVertex3f(rr, rr, rr)
        # 底面
        glColor3f(0.6, 0.6, 0.0)
        glVertex3f(rr, -rr, -rr)
        glVertex3f(-rr, -rr, -rr)
        glVertex3f(-rr, -rr, rr)
        glVertex3f(rr, -rr, rr)
        # 左面
        glColor3f(0.6, 0.0, 0.6)
        glVertex3f(-rr, rr, -rr)
        glVertex3f(-rr, -rr, -rr)
        glVertex3f(-rr, -rr, rr)
        glVertex3f(-rr, rr, rr)
        # 右面
        glColor3f(0.0, 0.6, 0.6)
        glVertex3f(rr, rr, -rr)
        glVertex3f(rr, -rr, -rr)
        glVertex3f(rr, -rr, rr)
        glVertex3f(rr, rr, rr)
        
        glEnd()
        glPopMatrix()
