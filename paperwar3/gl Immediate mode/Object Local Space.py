from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import numpy as np


class CubeDrawer():
    cubeVertices = ((1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1),
                    (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1))
    cubeEdges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5),
                 (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))
    cubeQuads = ((0, 3, 6, 4), (2, 5, 6, 3), (1, 2, 5, 7),
                 (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))

    def __init__(self) -> None:
        self.position = [10, 5, 10]
        self.color = 0.5*np.random.rand(3)+0.5
        self.color_list = [[k/5, 1, 1]for k in range(5)]
        self.param = 0
        self.angle = 1
        self.size = rr = 2
        self.cube_list = []

    def draw_wireCube(self):
        glBegin(GL_LINES)
        for cubeEdge in self.cubeEdges:
            for cubeVertex in cubeEdge:
                glVertex3fv(self.cubeVertices[cubeVertex])
        glEnd()

    def draw_solidCube(self):
        glBegin(GL_QUADS)
        for cubeQuad in self.cubeQuads:
            for cubeVertex in cubeQuad:
                glVertex3fv(self.cubeVertices[cubeVertex])
        glEnd()


class drawer_manager():
    def __init__(self) -> None:
        self.cube_list = [CubeDrawer()]
        self.cube_index = 0
        self.cube_len = 1

    def draw(self, is_first=False):
        if is_first:
            glColor3f(0, 1, 1)
            self.cube_list[0].draw_solidCube()
            self.cube_index = 1
            return

        ind = self.cube_index
        if ind >= self.cube_len:
            self.cube_list.append(CubeDrawer())
            self.cube_len += 1

        temp = ind/self.cube_len
        glColor3f(1, temp, 1-temp)
        # print(1-ind/self.cube_len)
        self.cube_list[ind].draw_wireCube()

        self.cube_index += 1


###############################################

def display(cm: drawer_manager):
    glLoadIdentity()
    # glTranslatef(-5, 0, -20)
    glTranslatef(0, 0, -20)
    # glRotatef(20, 1, 1, 0)
    tim = pygame.time.get_ticks()/20
    # print(tim)
    glRotatef(20, 1, 0, 0)
    glRotatef(tim, 0, 1, 0)

    cm.draw(True)

def _display(cm: drawer_manager):
    glLoadIdentity()
    # cm.draw(True)

    gluLookAt(
        50, 50, 50,       # 眼睛位置 (Eye Position)
        0.0, 0.0, 0.0,       # 观察目标 (Look At Target)
        0.0, 1.0, 0.0        # 上方向 (Up Direction)
    )
    glPushMatrix()

    # self.param = 0
    cm.draw(True)
    glTranslatef(40, 0, 0)
    cm.draw(True)
    glTranslatef(-40, 0, 20)
    cm.draw(True)
    glTranslatef(0, 0, -20)

    glTranslatef(-20, 0, 30)
    cm.draw()
    for k in range(3):
        glTranslatef(5, 0, 0)
        glRotatef(30, 1, 0, 0)
        cm.draw()
    for k in range(5):
        glTranslatef(5, 0, 0)
        cm.draw()
    for k in range(3):
        glTranslatef(0, -5, 0)
        glRotatef(30, 0, 1, 0)
        cm.draw()
    for k in range(5):
        glTranslatef(0, -5, 0)
        cm.draw()

    glPopMatrix()


if __name__ == "__main__":
    win_size = [800, 600]
    pygame.init()
    pygame.display.set_mode(win_size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('PyOpenGL with Pygame Example')

    glEnable(GL_DEPTH_TEST)
    # glEnable(GL_LINE_SMOOTH)
    # glShadeModel(GL_SMOOTH)

    # '''Prevents OpenGL from removing faces which face backward'''
    # glDisable( GL_CULL_FACE )
    glClearColor(0.2, 0.3, 0.4, 1)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (win_size[0] / win_size[1]), 1, 999.0)
    # gluLookAt(0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    # gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

    glMatrixMode(GL_MODELVIEW)

    obj = drawer_manager()
    while not pygame.event.get(pygame.QUIT):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)



        display(obj)

        # glFlush()
        pygame.display.flip()

        pygame.time.wait(10)

    pygame.quit()
