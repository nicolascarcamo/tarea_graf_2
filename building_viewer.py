# coding=utf-8

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
import grafica.lighting_shaders as ls

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
    lightingPipeline = ls.SimpleGouraudShaderProgram()
    phongPipeline = ls.SimplePhongShaderProgram()
    textureLightShaderProgram = ls.SimpleTextureGouraudShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)
    # Setting up the clear screen color
    glClearColor(0.55, 0.55, 0.55, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
    # Convenience function to ease initialization
    empire = EmpireState(phongPipeline)
    willis = WillisTower(lightingPipeline)
    burj = BurjAlArab(lightingPipeline)

    empireGround = EmpireGround(textureLightShaderProgram)
    willisGround = WillisGround(textureLightShaderProgram)
    burjGround = BurjAlArabGround(textureLightShaderProgram)
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
            glUseProgram(lightingPipeline.shaderProgram) 

            glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "La"), controller.daylightR, controller.daylightG, controller.daylightB)
            glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ld"), 1.0, 1.0, 1.0)
            glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ls"), controller.daylightR, controller.daylightG, controller.daylightB)

            # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
            glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ka"), 0.8, 0.8, 0.8)
            glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Kd"), 0.8, 0.8, 0.8)
            glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

            glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "lightPosition"), -4, -4, 5)
            glUniform3f(glGetUniformLocation(phongPipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1],
                        controller.viewPos[2])
            glUniform1ui(glGetUniformLocation(phongPipeline.shaderProgram, "shininess"), 90)

            glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "constantAttenuation"), 0.0001)
            glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "linearAttenuation"), 0.03)
            glUniform1f(glGetUniformLocation(phongPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

            glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "projection"), 1, GL_TRUE, controller.project_value)
            glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "view"), 1, GL_TRUE, controller.view)
            glUniformMatrix4fv(glGetUniformLocation(phongPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            empire.draw(phongPipeline)

            glUseProgram(textureLightShaderProgram.shaderProgram)
            
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "La"), controller.daylightR, controller.daylightG, controller.daylightB)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Ld"), 0.2, 0.2, 0.2)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Ls"), controller.daylightR, controller.daylightG, controller.daylightB)

            # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Ka"), 0.8, 0.8, 0.8)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Kd"), 0.8, 0.8, 0.8)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "lightPosition"), 4, 4, 5)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1],
                        controller.viewPos[2])
            glUniform1ui(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "shininess"), 90)

            glUniform1f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "constantAttenuation"), 0.0001)
            glUniform1f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "linearAttenuation"), 0.03)
            glUniform1f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "quadraticAttenuation"), 0.01)


            glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "view"), 1, GL_TRUE, controller.view)
            glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, controller.project_value)
            empireGround.draw(textureLightShaderProgram)
        
        elif controller.building == 1:
            glUseProgram(lightingPipeline.shaderProgram)

            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), controller.daylightR, controller.daylightG, controller.daylightB)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 0.7, 0.7, 1.0)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), controller.daylightR, controller.daylightG, controller.daylightB)

            # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.8, 0.8, 0.8)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), -5, -5, 2)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1],
                        controller.viewPos[2])
            glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 80)

            glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
            glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
            glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

            glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, controller.project_value)
            glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, controller.view)
            glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            willis.draw(lightingPipeline)

            
            glUseProgram(textureLightShaderProgram.shaderProgram)
            
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "La"), controller.daylightR, controller.daylightG, controller.daylightB)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Ld"), 0.7, 0.7, 1.0)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Ls"), controller.daylightR, controller.daylightG, controller.daylightB)

            # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Kd"), 0.8, 0.8, 0.8)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "lightPosition"), -5, -5, 2)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1],
                        controller.viewPos[2])
            glUniform1ui(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "shininess"), 80)

            glUniform1f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "constantAttenuation"), 0.0001)
            glUniform1f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "linearAttenuation"), 0.03)
            glUniform1f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "quadraticAttenuation"), 0.01)

            glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "view"), 1, GL_TRUE, controller.view)
            glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, controller.project_value)
            willisGround.draw(textureLightShaderProgram)
        
        elif controller.building == 2:
            glUseProgram(lightingPipeline.shaderProgram)

            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), controller.daylightR, controller.daylightG, controller.daylightB)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), 1.0, 0.9, 0.3)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), controller.daylightR, controller.daylightG, controller.daylightB)

            # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), -5, -5, 2)
            glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1],
                        controller.viewPos[2])
            glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 80)

            glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
            glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
            glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)

            glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, controller.project_value)
            glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, controller.view)
            glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            burj.draw(lightingPipeline)


            glUseProgram(textureLightShaderProgram.shaderProgram)
            
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "La"), controller.daylightR, controller.daylightG, controller.daylightB)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Ld"), 1.0, 0.9, 0.3)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Ls"), controller.daylightR, controller.daylightG, controller.daylightB)

            # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Kd"), 0.5, 0.5, 0.5)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "lightPosition"), -5, -5, 2)
            glUniform3f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "viewPosition"), controller.viewPos[0], controller.viewPos[1],
                        controller.viewPos[2])
            glUniform1ui(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "shininess"), 80)

            glUniform1f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "constantAttenuation"), 0.0001)
            glUniform1f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "linearAttenuation"), 0.03)
            glUniform1f(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "quadraticAttenuation"), 0.01)

            glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "view"), 1, GL_TRUE, controller.view)
            glUniformMatrix4fv(glGetUniformLocation(textureLightShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, controller.project_value)
            burjGround.draw(textureLightShaderProgram)


        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
        #pipeline.drawCall(gpuAxis, GL_LINES)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    # freeing GPU memory
    #gpuAxis.clear()

    #gpuRedCube.clear()

    #gpuRainbowCube.clear()

    glfw.terminate()
