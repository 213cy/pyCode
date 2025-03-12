from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import time

# https://github.com/mcfletch/openglcontext/blob/0382cd0179a7e99b5bab671b00a0de8c4d0f8409/tests/nehe4.py


class ThreePlanet():
    def __init__(self) -> None:
        self.common_para = 1/6


    def update(self, event):
        # 1 degree / second
        self.degree_per_second = time.time()%360
        # 1 cycle /second
        self.speed = time.time()%360 * 360

    def render(self):
        
        glDisable( GL_LIGHTING) 
        glDisable( GL_CULL_FACE)
        '''The call to time.time creates a float value which is
        converted to a fraction of three seconds then multiplied
        by 360 (degrees) to get the current appropriate rotation
        for an object spinning at 1/3 rps.
        
        Note that OpenGL uses *degrees*, not radians!
        '''
        glTranslatef(10,1,10)
        glPushMatrix()
        glRotated( self.speed/3, 1,0,0)
        self.draw_quad()
        

        '''Note the need to re-load the identity matrix, as the 
        glRotated/glTranslatef functions modify the current matrix.
        '''
        # glLoadIdentity()
        glPopMatrix()
        '''Animating as above, but at 6 rev/s'''
        glRotated( self.speed*self.common_para, 0,1,0)
        glTranslatef(5,0,0)
        glPushMatrix()
        glRotated( self.speed, 0,1,0)
        self.draw_triangle()

        glPopMatrix()
        glRotated(360 -self.speed*self.common_para, 0,1,0)
        glTranslatef(2,0,0)
        glRotated( 90, 0,0,1)
        glRotated( self.speed/0.5, 0,1,0)

        self.draw_triangle()

 
    def draw_quad(self):
        size = 1 
        glColor3f(0.5,0.5,1.0)
        glBegin(GL_QUADS)
        glVertex3f(-size,-size, 0.0)
        glVertex3f( size,-size, 0.0)
        glVertex3f( size, size, 0.0)
        glVertex3f(-size, size, 0.0)
        glEnd()


    def draw_triangle(self):
        size = 1
        glBegin(GL_TRIANGLES)
        glColor3f(1,0,0)
        glVertex3f(-size,-size,0.0)
        glColor3f(0, 1, 0)
        glVertex3f(size, -size, 0)
        glColor3f(0, 0, 1)
        glVertex3f(0, size, 0)
        glEnd()


if __name__ == "__main__":
    from main import App
    app = App()
    app.add_object(ThreePlanet())
    app.run()
    app.end()
