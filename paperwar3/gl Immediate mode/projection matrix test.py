from OpenGL.GL import *
from OpenGL.GLU import *

import glfw
import glfw.GLFW as GLFW_CONSTANTS

import pyrr

def display():
    cubeVertices = ((1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1),
                    (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1))
    cubeEdges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5),
                 (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))
    cubeQuads = ((0, 3, 6, 4), (2, 5, 6, 3), (1, 2, 5, 7),
                 (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))

    glColor3f(0, 1, 1)
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

    glColor3f(1, 0, 1)
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()


if __name__ == "__main__":
    print(20 * "-")

    glfw.init()
    # glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
    # glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
    # glfw.window_hint(
    #     GLFW_CONSTANTS.GLFW_OPENGL_PROFILE,
    #     GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
    # glfw.window_hint(
    #     GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)
    # # for uncapped framerate
    # glfw.window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER, GL_FALSE)

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    window = glfw.create_window(
        SCREEN_WIDTH, SCREEN_HEIGHT, "for test", None, None)
    glfw.make_context_current(window)

    ###############################################################

    #  init_opengl
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # glEnable(GL_LINE_SMOOTH)
    # glShadeModel(GL_SMOOTH)

    # '''Prevents OpenGL from removing faces which face backward'''
    # glDisable( GL_CULL_FACE )
    glClearColor(0.2, 0.3, 0.4, 1)

    ###############################################################

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    fovy, aspect, near, far = 70, 1, 1, 5000
    gluPerspective(fovy, aspect, near, far)
    # print(glGetDoublev(GL_PROJECTION_MATRIX))
    print(glGetFloatv(GL_PROJECTION_MATRIX))

    mat = pyrr.matrix44.create_perspective_projection(
        fovy, aspect, near, far, dtype=None)
    print(mat)

    #####################################

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (SCREEN_WIDTH / SCREEN_HEIGHT), 1, 999.0)
    gluLookAt(0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    # gluOrtho2D(-10.0, 10.0, -10.0, 10.0)

    glMatrixMode(GL_MODELVIEW)

    start_frame_time = glfw.get_time()
    running = True
    while (running):
        if glfw.window_should_close(window):
            running = False
        # check events
        glfw.poll_events()

        # current_frame_time = glfw.get_time()
        # d_frame_time = current_frame_time - last_frame_time
        # last_frame_time = current_frame_time
        elapse_time = glfw.get_time() - start_frame_time
        # print(d_frame_time)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        glTranslatef(0, 0, -20)
        # tim = 20
        # print(tim)
        glRotatef(20, 1, 0, 0)
        glRotatef(20*elapse_time, 0, 1, 0)

        display()

        glFlush()
        glfw.swap_buffers(window)

    glfw.terminate()

# ++++++++++++++++++++++++++++++++
# exit()
