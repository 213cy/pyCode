import glfw
import glfw.GLFW as GLFW_CONSTANTS
from OpenGL.GL import *


SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100


def test():
# -------------------------------------------------
# GL_INVALID_OPERATION, 0x0502, 1282
# b'\xce\xde\xd0\xa7\xb2\xd9\xd7\xf7'.decode('gb2312')
# = '无效操作'
    print( bool(glGetString) )

    print( "Some Descriptions about the current GL connection")
    restr=glGetString(GL_VENDOR)
    print(f"GL_VENDOR : {restr.decode()}")
    restr=glGetString(GL_RENDERER)
    print(f"GL_RENDERER : {restr.decode()}")
    restr=glGetString(GL_VERSION)
    print(f"GL_VERSION : {restr.decode()}")
    restr=glGetString(GL_SHADING_LANGUAGE_VERSION)
    print(f"GL_SHADING_LANGUAGE_VERSION : {restr.decode()}")
    print(55*"-")


    print( f"Support GL4.5 function 'glCreateTextures' ? : {bool(glCreateTextures)}" )
    try:
        id = ctypes.c_uint()
        glCreateTextures(GL_TEXTURE_2D_ARRAY, 1, ctypes.byref(id))
    except Exception as e:
        print(e)

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D_ARRAY, texture)
    print( f"Support GL4.5 function 'glTextureStorage3D' ? : {bool(glTextureStorage3D)}" )
    try:
        glTextureStorage3D(texture, 4, GL_RGB8, 16, 16, 16 )
    except Exception as e:
        print(e)

    print( f"Support GL4.2 function 'glTexStorage3D' ? : {bool(glTexStorage3D)}" )
    try:
        glTexStorage3D(GL_TEXTURE_2D_ARRAY, 4, GL_RGB8, 16, 16, 16 )
    except Exception as e:
        print(e)

    print(55*"=")
    print()

glfw.init()

# glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
# glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
# glfw.window_hint(
#     GLFW_CONSTANTS.GLFW_OPENGL_PROFILE,
#     GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
# glfw.window_hint(
#     GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE)
# for uncapped framerate
# glfw.window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER, GL_FALSE)

window = glfw.create_window(
            SCREEN_WIDTH, SCREEN_HEIGHT, "Title", None, None)
glfw.make_context_current(window)


test()

glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 5)
test()

glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)

test()

glfw.destroy_window(window)
glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)
window = glfw.create_window(
            SCREEN_WIDTH, SCREEN_HEIGHT, "Title", None, None)
glfw.make_context_current(window)
test()

glfw.destroy_window(window)
glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 5)
window = glfw.create_window(
            SCREEN_WIDTH, SCREEN_HEIGHT, "Title", None, None)
glfw.make_context_current(window)
test()
print('done!')