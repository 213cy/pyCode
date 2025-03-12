import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import pyrr

from cursor_cube import CursorCube
from object_glu import ObjectFromGlu
from cube_frame import CubeFrame

# https://www.youtube.com/watch?v=exQ43PFWJBU


class GroundGrid():
    def __init__(self) -> None:
        self.position = [0, 0, 0]

    def update(self, event):
        pass

    def render(self):
        glLineWidth(1.0)

        glColor3f(1, 1, 0.5)
        for k in range(21):
            glPushMatrix()
            glTranslate(0, 0, k)

            glBegin(GL_LINES)
            glVertex3f(0, -0.1, 0)
            glVertex3f(20, -0.1, 0)
            glEnd()

            glPopMatrix()

        glColor3f(1, 1, 1)
        for k in range(21):
            glBegin(GL_LINES)
            glVertex3f(k, -0.1, 0)
            glVertex3f(k, -0.1, 20)
            glEnd()


class Camera():
    def __init__(self) -> None:
        self.position = np.array([15, 0, 30])
        self.target_pos = [10, 0, 10]
        self.angle = [0, 0, 0]
        self.rotation = np.array([40, 30, 0])
        # Trackball控制器变量
        self.last_mouse_pos = None
        self.mult_matrix = pyrr.matrix44.create_identity()
        self.scale = 3*[1.0]
        self.mouse_sensitivity = 1

    def update(self, stat):
        pressed_buttons = pygame.mouse.get_pressed()
        # print(pressed_buttons)
        a = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        if a != []:
            # print(a)
            dx, dy = pygame.mouse.get_rel()
            return

        if pressed_buttons[0]:
            dx, dy = pygame.mouse.get_rel()
            self.rotation[0] += dy * self.mouse_sensitivity
            self.rotation[1] += dx * self.mouse_sensitivity

    def _set_view(self):
        glLoadIdentity()
        glTranslatef(*(-self.position))
        print(glGetFloatv(GL_MODELVIEW_MATRIX))
        glRotatef(self.rotation[0], 1, 0, 0)
        print(glGetFloatv(GL_MODELVIEW_MATRIX))
        glRotatef(self.rotation[1], 0, 1, 0)
        print(glGetFloatv(GL_MODELVIEW_MATRIX))

    def _set_view(self):
        glLoadIdentity()

        yaw, pitch, roll = np.deg2rad(self.rotation)
        # yaw , pitch, roll = np.deg2rad( [40,40,0] )

        ts = pyrr.matrix44.create_from_translation(-self.position)
        # ts = pyrr.matrix44.create_from_translation([-13, 0, -30])
        rx = pyrr.matrix44.create_from_axis_rotation([1.0, 0, 0], yaw)
        ry = pyrr.matrix44.create_from_axis_rotation([0, 1.0, 0], pitch)
        self.mult_matrix = mult_matrix = ry @ rx @ ts
        # mult_matrix = rx @ ry @ ts
        glMultMatrixf(mult_matrix.flatten())

    def _set_view(self):
        glLoadIdentity()

        glTranslatef(-13.6, 2.35, -25)
        # print(self.rotation)
        glRotatef(self.rotation[0], 1.0, 0.0, 0.0)  # 绕x轴旋转
        glRotatef(self.rotation[1], 0.0, 1.0, 0.0)  # 绕y轴旋转
        # glRotatef(self.rotation[2], 0.0, 0.0, 1.0)  # 绕z轴旋转

        glScalef(*self.scale)

    def set_view(self):
        yaw, pitch, roll = np.deg2rad(self.rotation)
        rx = pyrr.matrix44.create_from_axis_rotation([1.0, 0, 0], yaw)
        ry = pyrr.matrix44.create_from_axis_rotation([0, 1.0, 0], pitch)

        pos = [10, 0, 10, 1]@ry@rx

        glTranslatef(*(-pos[0], -pos[1], -pos[2]-25))

        glRotatef(self.rotation[0], 1.0, 0.0, 0.0)  # 绕x轴旋转
        glRotatef(self.rotation[1], 0.0, 1.0, 0.0)  # 绕y轴旋转
        # mode_mat = glGetFloatv(GL_MODELVIEW_MATRIX)

    def set_view_3(self):
        glScalef(*self.scale)
        gluLookAt(
            20, 20, 20,       # 眼睛位置 (Eye Position)
            0.0, 0.0, 0.0,       # 观察目标 (Look At Target)
            0.0, 1.0, 0.0        # 上方向 (Up Direction)
        )

    def render(self):
        pass


class App():
    display = [1280, 720]  # 16:9
    display = [800, 600]

    def __init__(self, auto_create_obj=False):
        self.init_window()
        self.init_opengl()
        self.key_event_stat = {}
        self.camera = Camera()
        self.grid = GroundGrid()
        self.object_list = [
            self.grid,
            self.camera,
        ]
        if auto_create_obj:
            self.cube = CursorCube()
            self.obj_glu = ObjectFromGlu()
            self.object_list += [
                self.cube,
                self.obj_glu,
                CubeFrame(),
            ]

    def init_window(self):
        pygame.init()
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption('PyOpenGL with Pygame Example')

        pygame.key.set_repeat(2000)

    def init_opengl(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.display[0] / self.display[1]), 1, 500.0)
        # gluLookAt(0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        # gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

        # glEnable(GL_LINE_SMOOTH)
        # glShadeModel(GL_SMOOTH)

        # '''Prevents OpenGL from removing faces which face backward'''
        # glDisable( GL_CULL_FACE )
        glClearColor(0.2, 0.3, 0.4, 1)

    def add_object(self, obj):
        self.object_list.append(obj)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get(exclude=pygame.MOUSEBUTTONDOWN):
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    if False:
                        rotation_matrix = apply_trackball(
                            event.pos, last_mouse_pos)
                        last_mouse_pos = event.pos
                elif event.type == pygame.KEYDOWN:
                    self.key_event_stat[event.key] = True
                    print("Key A has been pressed")
                elif event.type == pygame.KEYUP:
                    self.key_event_stat[event.key] = False
                    # if event.key == pygame.K_a:

            self.game_logic()
            self.draw_scene()
            pygame.time.wait(10)

    def draw_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.camera.set_view()

        for k in self.object_list:
            k.render()
        # self.grid.render()
        # self.cube.render()
        # self.obj_glu.render()

        # glFlush()
        pygame.display.flip()

    def game_logic(self):
        for k in self.object_list:
            k.update(self.key_event_stat)
        # self.cube.update(self.key_event_stat)
        # self.camera.update(self.key_event_stat)

    def end(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = App(auto_create_obj=True)
    app.run()
    app.end()


# ++++++++++++++++++++++++++++++++
# exit()
