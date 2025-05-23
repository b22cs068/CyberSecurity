import glfw
from OpenGL.GL import *
from pyrr import Matrix44
import numpy as np

def initialize_window(width, height, title):
    if not glfw.init():
        raise Exception("GLFW could not be initialized!")

    # Create a window
    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window could not be created!")

    # Make the context current
    glfw.make_context_current(window)
    return window

def main():
    # Initialize GLFW window
    window = initialize_window(800, 600, "OpenGL with Python")

    # Set up OpenGL settings
    glClearColor(0.2, 0.3, 0.3, 1.0)

    while not glfw.window_should_close(window):
        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT)

        # Swap buffers and poll events
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Terminate GLFW when done
    glfw.terminate()

if __name__ == "__main__":
    main()
