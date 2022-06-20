# coding=utf-8
"""
Projections example.
"""

import glfw
from OpenGL.GL import *
import numpy as np
import sys, os.path
from modelo import *
from controlador import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es

__author__ = "Nicolas Carcamo"
__license__ = "MIT"


# We will use the global controller as communication with the callback function

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Buildings Viewer", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    controller = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)

    # Assembling the shader program
    pipeline = es.SimpleModelViewProjectionShaderProgram()
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)
    # Setting up the clear screen color
    glClearColor(0.55, 0.55, 0.55, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
    # Convenience function to ease initialization
    empire = EmpireState(pipeline)
    willis = WillisTower(pipeline)

    empireGround = EmpireGround(textureShaderProgram)
    willisGround = WillisGround(textureShaderProgram)
    burjGround = BurjAlArabGround(textureShaderProgram)
    # Creating shapes on GPU memory

    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()


        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Movimiento de camara, relleno o no de las figuras dependiendo del estado del controlador
        controller.update(pipeline, window, dt)
        
        # Setting up the projection transform
        controller.project(width, height)

        # Clearing the screen in both, color and depth


        # Drawing shapes with different model transformations
        if controller.building == 0:
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, controller.project_value)    
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, controller.view)
            empire.draw(pipeline)

            glUseProgram(textureShaderProgram.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, controller.project_value)  
            glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, controller.view)
            empireGround.draw(textureShaderProgram)
        
        elif controller.building == 1:
            glUseProgram(pipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "projection"), 1, GL_TRUE, controller.project_value)    
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "view"), 1, GL_TRUE, controller.view)
            willis.draw(pipeline)

            glUseProgram(textureShaderProgram.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, controller.project_value)  
            glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, controller.view)
            willisGround.draw(textureShaderProgram)
        
        elif controller.building == 2:

            glUseProgram(textureShaderProgram.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, controller.project_value)  
            glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, controller.view)
            burjGround.draw(textureShaderProgram)

        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        #pipeline.drawCall(gpuAxis, GL_LINES)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    #gpuAxis.clear()

    #gpuRedCube.clear()

    #gpuRainbowCube.clear()

    glfw.terminate()
