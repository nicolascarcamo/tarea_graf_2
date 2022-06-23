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

        elif key == glfw.KEY_W:
            self.set_building("Willis Tower")

        elif key == glfw.KEY_B:
            self.set_building("Burj Al Arab")

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

            

        viewPos = np.array([camX, camY, camZ])

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

'''
class CameraR(_Camera):
    """
    Camera in spheric coordinates.
    """

    def __init__(self, r=1.0, phi=45, theta=45, center=_Point3(), up=_Vector3(0, 0, 1)):
        """
        Constructor.

        :param r: Radius
        :param phi: Phi angle
        :param theta: Theta angle
        :param center: Center point
        :param up: Up vector
        :type r: float, int
        :type phi: float, int
        :type theta: float, int
        :type center: Point3
        :type up: Point3
        """
        _Camera.__init__(self)
        if isinstance(center, _Point3):
            if isinstance(up, _Vector3):
                if r > 0:
                    if 0 <= phi <= 360 and 0 <= theta <= 90:
                        self._center = center
                        self._name = 'unnamed'
                        self._phi = phi
                        self._r = r
                        self._rvel = _CAMERA_DEFAULT_RVEL
                        self._theta = theta
                        self._up = up
                    else:
                        raise Exception('Phi angle must be between 0 and 360 degrees, theta must be between 0 and 180')
                else:
                    raise Exception('Radius must be greater than zero')
            else:
                raise Exception('up_vector must be Vector3 type')
        else:
            raise Exception('center_point must be Point3 type')

    def set_r_vel(self, vel):
        """
        Defines radial velocity.

        :param vel: Velocity
        :type vel: float, int
        """
        if vel > 0:
            self._rvel = vel
        else:
            raise Exception('Velocity must be greater than zero')

    def place(self):
        """
        Place camera in world.
        """
        _glLoadIdentity()
        _gluLookAt(self._r * _cos(self._phi),
                   self._r * _sin(self._phi),
                   self._r ,
                   self._center.get_x(), self._center.get_y(), self._center.get_z(),
                   self._up.get_x(), self._up.get_y(),
                   self._up.get_z())

    def get_view(self):
        """
        Get view matrix.

        :return:
        """
        return _tr2.lookAt(
            _np.array([self._r  * _cos(self._phi),
                       self._r  * _sin(self._phi),
                       self._r ]),
            _np.array([self._center.get_x(), self._center.get_y(), self._center.get_z()]),
            _np.array([self._up.get_x(), self._up.get_y(), self._up.get_z()])
        )

    def get_pos_x(self):
        """
        Return x position.

        :return:
        """
        return self._r * _cos(self._phi)

    def get_pos_y(self):
        """
        Return y position.

        :return:
        """
        return self._r * _sin(self._phi)

    def get_pos_z(self):
        """
        Return z position.

        :return:
        """
        return self._r

    def get_center_x(self):
        """
        Return center x position.

        :return:
        """
        return self._center.get_x()

    def get_center_y(self):
        """
        Return center y position.

        :return:
        """
        return self._center.get_y()

    def get_center_z(self):
        """
        Return center x position.

        :return:
        """
        return self._center.get_z()

    def __str__(self):
        """
        Returns camera status.

        :return: Camera status
        :rtype: basestring
        """
        x, y, z = self.convert_to_xyz()
        r = _CAMERA_ROUNDED
        msg = 'Camera: {12}\nRadius: {0}\nPhi angle: {1}, Theta angle: {2}\nXYZ eye pos: ({3},{4},{5})\nXYZ center ' \
              'pos: ({6},{7},{8})\nXYZ up vector: ({9},{10},{11})'
        return msg.format(round(self._r, r), round(self._phi, r),
                          round(self._theta, r), round(x, r), round(y, r),
                          round(z, r), round(self._center.get_x(), r),
                          round(self._center.get_y(), r),
                          round(self._center.get_z(), r),
                          round(self._up.get_x(), r), round(self._up.get_y(), r),
                          round(self._up.get_z(), r), self.get_name())

    def far(self):
        """
        Camera zoom-out.
        """
        self._r += self._rvel

    def close(self):
        """
        Camera zoom-in.
        """
        r = self._r - self._rvel
        if r < 0:  # Radius cannot be less than zero
            return
        self._r = r

    def rotate_phi(self, angle):
        """
        Rotate phi angle.

        :param angle: Rotation angle
        :type angle: float, int
        """
        self._phi = (self._phi + angle) % 360

    def rotate_theta(self, angle):
        """
        Rotate theta angle.

        :param angle: Rotation angle
        :type angle: float, int
        """
        self._theta = min(max(self._theta + angle, _CAMERA_MIN_THETA_VALUE), 180)

    def convert_to_xyz(self):
        """
        Convert spheric to cartesian.

        :return: Cartesian coodinates
        :rtype: tuple
        """
        return _spr_to_xyz(self._r, self._phi, self._theta)

    def convert_to_spr(self):
        """
        Convert to spheric.

        :return: Coordinates
        :rtype: tuple
        """
        return self._r, self._phi, self._theta

    def move_center_x(self, dist):
        """
        Moves center x coordinate.

        :param dist: X-distance
        :type dist: float, int
        """
        self._center.set_x(self._center.get_x() + dist)

    def move_center_y(self, dist):
        """
        Moves center y coordinate.

        :param dist: Y-distance
        :type dist: float, int
        """
        self._center.set_y(self._center.get_y() + dist)

    def move_center_z(self, dist):
        """
        Moves center z coordinate.

        :param dist: Z-distance
        :type dist: float, int
        """
        if (_CAMERA_CENTER_LIMIT_Z_DOWN <= self._center.get_z() and dist < 0) or \
                (self._center.get_z() <= _CAMERA_CENTER_LIMIT_Z_UP and dist > 0):
            self._center.set_z(self._center.get_z() + dist)

    def get_name(self):
        """
        Returns camera name.

        :return: Camera name
        :rtype: basestring
        """
        return self._name

    def set_name(self, n):
        """
        Set camera name.

        :param n: Camera name
        :type n: basestring
        """
        self._name = n

    def get_radius(self):
        """
        Get camera radius.

        :return: Camera radius
        :rtype: float, int
        """
        return self._r

    def set_radius(self, r):
        """
        Set camera radius.

        :param r: Camera radius
        :type r: float, int
        """
        self._r = r

    def get_phi(self):
        """
        Get camera phi angle.

        :return: Phi angle
        :rtype: float, int
        """
        return self._phi

    def set_phi(self, phi):
        """
        Set camera phi.

        :param phi: Phi angle
        :type phi: float, int
        """
        self._phi = phi

    def get_theta(self):
        """
        Returns theta angle.

        :return: Theta angle
        :rtype: float, int
        """
        return self._theta

    def set_theta(self, theta):
        """
        Set theta angle.

        :param theta: Theta angle
        :type theta: float, int
        """
        self._theta = theta
        '''