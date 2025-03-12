from OpenGL.GL import *
from OpenGL.GLU import *
# from pygame.locals import *

class ObjectFromGlu():
    def __init__(self) -> None:
        self.position = [10,0,10]
        self.slices = 8
        self.stacks = 8
        self.quad = gluNewQuadric()
        gluQuadricNormals(self.quad, GLU_SMOOTH)


    def update(self, event):
        pass

    def render(self):
        glPushMatrix()
        glTranslatef(*self.position)
        gluSphere(self.quad, 1, 8, 8)
        glPopMatrix()
