from OpenGL.GL import *
# from OpenGL.GLU import *
# from pygame.locals import *
import numpy as np


class CubeFrame():
    def __init__(self) -> None:
        self.position = [10, 5, 10]
        self.color = 0.5*np.random.rand(3)+0.5
        self.d_color = np.random.rand(3)
        self.angle = 1
        self.size = rr = 2
        self.vertices = [
            [rr, -rr, -rr],
            [rr, rr, -rr],
            [-rr, rr, -rr],
            [-rr, -rr, -rr],
            [rr, -rr, rr],
            [rr, rr, rr],
            [-rr, -rr, rr],
            [-rr, rr, rr]
        ]

        self.edges = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [0, 4],
            [1, 5],
            [2, 6],
            [3, 7],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 4]
        ]

    def update(self, event):
        self.angle += 1
        color = np.array(self.color + self.d_color)
        # print(self.color,color)
        if np.all((color > 0.3) & (color < 1)):
            self.color = color
        else:
            color_target = 0.5*np.random.rand(3)+0.5
            d_color = (color_target-color)
            self.d_color = d_color / np.linalg.norm(d_color)/ 30

    def render(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.angle, 3, 1, 1)
        glColor3f(*self.color)
        glLineWidth(4)
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()
        glLineWidth(1)

        glPopMatrix()


if __name__ == "__main__":
    from main import App
    app = App()
    app.add_object(CubeFrame())
    app.run()
    app.end()
