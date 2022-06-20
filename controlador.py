import glfw
from OpenGL.GL import *
import numpy as np
import sys, os.path
from modelo import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es

PROJECTION_ORTHOGRAPHIC = 0
PROJECTION_FRUSTUM = 1
PROJECTION_PERSPECTIVE = 2

class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.projection = 0
        self.project_value = 0
        #Empire State = 0 // Willis Tower = 1 // Burj Al Arab = 2
        self.building = 0
        self.view = 0


        self.theta = np.pi / 4

        #Definir luego una funcion set_building y set_view

    #Funcion para hacer mas claro el codigo en lectura
    #Asigna el edificio activo
    def set_building(self, building):
        if building == "Empire State":
            self.building = 0
        elif building == "Willis Tower":
            self.building = 1
        elif building == "Burj Al Arab":
            self.building = 2


    def on_key(self, window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return

        if key == glfw.KEY_SPACE:
            self.fillPolygon = not self.fillPolygon

        elif key == glfw.KEY_1:
            print('Orthographic projection')
            self.projection = PROJECTION_ORTHOGRAPHIC

        elif key == glfw.KEY_2:
            print('Frustum projection')
            self.projection = PROJECTION_FRUSTUM

        elif key == glfw.KEY_3:
            print('Perspective projection')
            self.projection = PROJECTION_PERSPECTIVE
        
        elif key == glfw.KEY_E:
            self.set_building("Empire State")

        elif key == glfw.KEY_W:
            self.set_building("Willis Tower")

        elif key == glfw.KEY_B:
            self.set_building("Burj Al Arab")

        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

    def update(self, pipeline, window, dt):

        
        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            self.theta -= 2 * dt

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            self.theta += 2 * dt

        # Setting up the view transform

        camX = 10 * np.sin(self.theta)
        camY = 10 * np.cos(self.theta)

        viewPos = np.array([camX, camY, 10])

        self.view = tr.lookAt(
            viewPos,
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )

        if (self.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)



    def project(self, width, height):
        if self.projection == PROJECTION_ORTHOGRAPHIC:
            self.project_value = tr.ortho(-8, 8, -8, 8, 0.1, 100)

        elif self.projection == PROJECTION_FRUSTUM:
            self.project_value = tr.frustum(-5, 5, -5, 5, 9, 100)

        elif self.projection == PROJECTION_PERSPECTIVE:
            self.project_value = tr.perspective(60, float(width) / float(height), 0.1, 100)

        else:
            raise Exception()


