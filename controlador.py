import glfw
from OpenGL.GL import *
import numpy as np
import sys, os.path
from modelo import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es

from OpenGL.GLU import gluLookAt as _gluLookAt
from grafica.mathlib import _cos, _sin, _xyz_to_spr, _spr_to_xyz
from grafica.mathlib import Point3 as _Point3
from grafica.mathlib import Vector3 as _Vector3
import math as _math


PROJECTION_ORTHOGRAPHIC = 0
PROJECTION_FRUSTUM = 1
PROJECTION_PERSPECTIVE = 2
PROJECTION_ALT_ORTHOGRAPHIC = 3
PROJECTION_CYLINDRICAL = 4

class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.projection = PROJECTION_ORTHOGRAPHIC
        self.project_value = 0

        #Empire State = 0 // Willis Tower = 1 // Burj Al Arab = 2
        self.building = 0
        self.view = 0
        self.viewPos = 0

        self.daylightR = 1.0
        self.daylightG = 1.0
        self.daylightB = 1.0
        
        self.daymode = 2



        self.theta = np.pi / 4
        self.updown = np.pi / 4

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
        
        elif key == glfw.KEY_4:
            print('Alternative Orthographic projection')
            self.projection = PROJECTION_ALT_ORTHOGRAPHIC

        elif key == glfw.KEY_5:
            print('Alternative Orthographic projection')
            self.projection = PROJECTION_CYLINDRICAL

        elif key == glfw.KEY_E:
            self.set_building("Empire State")
            if self.daymode == 1 or self.daymode == 2:
                self.daylightR = 1.0
                self.daylightG = 1.0
                self.daylightB = 1.0
            else:
                self.daylightR = 0.1
                self.daylightG = 0.1
                self.daylightB = 0.1

        elif key == glfw.KEY_W:
            self.set_building("Willis Tower")
            if self.daymode == 1 or self.daymode == 2:
                self.daylightR = 0.7
                self.daylightG = 0.7
                self.daylightB = 1.0
            else:
                self.daylightR = 0.1
                self.daylightG = 0.1
                self.daylightB = 0.1

        elif key == glfw.KEY_B:
            self.set_building("Burj Al Arab")
            if self.daymode == 1 or self.daymode == 2:
                self.daylightR = 1.0
                self.daylightG = 0.9
                self.daylightB = 0.3
            else:
                self.daylightR = 0.1
                self.daylightG = 0.1
                self.daylightB = 0.1
        
        elif key == glfw.KEY_L:
            if self.daymode == 0:
                self.daymode = 1
            elif self.daymode == 1:
                self.daymode = 0
            elif self.daymode == 2:
                self.daymode = 0

        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

    def update(self, pipeline, window, dt):

        
        if (glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS):
            
            if self.projection in (PROJECTION_ORTHOGRAPHIC, PROJECTION_FRUSTUM, PROJECTION_PERSPECTIVE, PROJECTION_ALT_ORTHOGRAPHIC) :
                self.theta = 0
            else:
                self.theta -= 2 * dt
            

        if (glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS):
            if self.projection in (PROJECTION_ORTHOGRAPHIC, PROJECTION_FRUSTUM, PROJECTION_PERSPECTIVE, PROJECTION_ALT_ORTHOGRAPHIC):
                self.theta = 0
            else:
                self.theta += 2 * dt

        if (glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS):
            if self.projection in (PROJECTION_ORTHOGRAPHIC, PROJECTION_FRUSTUM, PROJECTION_PERSPECTIVE, PROJECTION_ALT_ORTHOGRAPHIC):
                self.updown = 1
            else:
                self.updown += 2 * dt

        if (glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS):
            if self.projection in (PROJECTION_ORTHOGRAPHIC, PROJECTION_FRUSTUM, PROJECTION_PERSPECTIVE, PROJECTION_ALT_ORTHOGRAPHIC):
                self.updown = 1
            else:
                self.updown -= 2 * dt        
        

        # Setting up the view transform
        if self.projection == PROJECTION_ORTHOGRAPHIC:
            camX = 5
            camY = 5
            camZ = 10
        elif self.projection == PROJECTION_FRUSTUM:
            camX = -5
            camY = -5
            camZ = 10
        elif self.projection == PROJECTION_PERSPECTIVE:
            camX = -5
            camY = 5
            camZ = 10
        elif self.projection == PROJECTION_ALT_ORTHOGRAPHIC:
            camX = 5
            camY = -5
            camZ = 10
        else:
            camX = 10 * np.sin(self.theta)
            camY = 10 * np.cos(self.theta)
            camZ = 10 * self.updown
            if camZ < 0:
                camZ = 0.2
            elif camZ > 20:
                camZ = 19.8

            

        self.viewPos = np.array([camX, camY, camZ])

        self.view = tr.lookAt(
            self.viewPos,
            np.array([0, 0, 0]),
            np.array([0, 0, 1])
        )

        if (self.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        if self.building == 0:
            if self.daymode == 0:
                if self.daylightR >= 0.1:
                    self.daylightR -= dt 
                if self.daylightG >= 0.1:
                    self.daylightG -= dt 
                if self.daylightB >= 0.1:
                    self.daylightB -= dt 
            elif self.daymode == 1:
                if self.daylightR <= 1.0:
                    self.daylightR += dt 
                if self.daylightG <= 1.0:
                    self.daylightG += dt 
                if self.daylightB <= 1.0:
                    self.daylightB += dt 
        elif self.building == 1:
            if self.daymode == 0:
                if self.daylightR >= 0.1:
                    self.daylightR -= dt 
                if self.daylightG >= 0.1:
                    self.daylightG -= dt 
                if self.daylightB >= 0.1:
                    self.daylightB -= dt 
            elif self.daymode == 1:
                if self.daylightR <= 0.7:
                    self.daylightR += dt 
                if self.daylightG <= 0.7:
                    self.daylightG += dt 
                if self.daylightB <= 1.0:
                    self.daylightB += dt
        elif self.building == 2:
            if self.daymode == 0:
                if self.daylightR >= 0.1:
                    self.daylightR -= dt 
                if self.daylightG >= 0.1:
                    self.daylightG -= dt 
                if self.daylightB >= 0.1:
                    self.daylightB -= dt 
            elif self.daymode == 1:
                if self.daylightR <= 1.0:
                    self.daylightR += dt 
                if self.daylightG <= 0.9:
                    self.daylightG += dt 
                if self.daylightB <= 0.2:
                    self.daylightB += dt

    def project(self, width, height):
        if self.projection == PROJECTION_ORTHOGRAPHIC:
            self.project_value = tr.ortho(-5, 5, -5, 5, 0.1, 100)

        elif self.projection == PROJECTION_FRUSTUM:
            self.project_value = tr.frustum(-3, 3, -3, 3, 9, 100)

        elif self.projection == PROJECTION_PERSPECTIVE:
            self.project_value = tr.perspective(50, float(width) / float(height), 0.1, 100)

        elif self.projection == PROJECTION_ALT_ORTHOGRAPHIC:
            self.project_value = tr.ortho(-4.5, 4.5, -4.5, 4.5, 0.1, 100)

        elif self.projection == PROJECTION_CYLINDRICAL:
            self.project_value = tr.frustum(-4, 4, -4, 4, 9, 100)

        else:
            raise Exception()

