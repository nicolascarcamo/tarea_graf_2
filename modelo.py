#from nis import maps
import glfw
from OpenGL.GL import *
import numpy as np
import sys, os.path
from modelo import *
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.text_renderer as tx
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.easy_shaders as es
import os.path
from grafica.gpu_shape import GPUShape
from OpenGL.GL import *

from OpenGL.GL import glClearColor, GL_STATIC_DRAW
import random
from typing import List

def create_gpu_ground(shape, pipeline, map):
    gpu = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpu)
    gpu.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
    thisFilePath = os.path.abspath(__file__)
    thisFolderPath = os.path.dirname(thisFilePath)
    assetsDirectory = os.path.join(thisFolderPath, "assets")
    assetPath = os.path.join(assetsDirectory, map)
    gpu.texture = es.textureSimpleSetup(
    assetPath, GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)
    return gpu


def createGPUShape(shape, pipeline):
        gpuShape = es.GPUShape().initBuffers()
        pipeline.setupVAO(gpuShape)
        gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)
        return gpuShape

class EmpireState(object):

    def __init__(self, pipeline):
        #gpuBeigeCube = createGPUShape(bs.createColorCube(0.98, 1, 0.64), pipeline)
        
        gpuRainbowCube = createGPUShape(bs.createRainbowCube(), pipeline)
        gpuRainbowCube1 = createGPUShape(bs.createRainbowCube(), pipeline)
        gpuRainbowCube2 = createGPUShape(bs.createRainbowCube(), pipeline)
        gpuRainbowCube3 = createGPUShape(bs.createRainbowCube(), pipeline)
        gpuRainbowCube4 = createGPUShape(bs.createRainbowCube(), pipeline)
        gpuRainbowCube5 = createGPUShape(bs.createRainbowCube(), pipeline)
        gpuRainbowCube6 = createGPUShape(bs.createRainbowCube(), pipeline)

        #  Base
        body = sg.SceneGraphNode('base')
        body.transform = tr.matmul([tr.translate(0, 0, 0.15),tr.scale(1, 1, 0.3)])
        body.childs += [gpuRainbowCube]

        #  2da Base
        body2 = sg.SceneGraphNode('base2')
        body2.transform = tr.matmul([tr.translate(0, 0, 0.6),tr.scale(0.8, 0.8, 1.2)])
        body2.childs += [gpuRainbowCube1]

        #  Pilar central
        body3 = sg.SceneGraphNode('pilar_cen')
        body3.transform = tr.matmul([tr.translate(0, 0, 1.4),tr.scale(0.4, 0.4, 2.8)])
        body3.childs += [gpuRainbowCube2]

        #  Pilar izq
        body4 = sg.SceneGraphNode('pilar_izq')
        body4.transform = tr.matmul([tr.translate(0.2, 0, 1.3),tr.scale(0.2, 0.5, 2.4)])
        body4.childs += [gpuRainbowCube3]

        #  Pilar der
        body5 = sg.SceneGraphNode('pilar_der')
        body5.transform = tr.matmul([tr.translate(-0.25, 0, 1.3),tr.scale(0.2, 0.5, 2.4)])
        body5.childs += [gpuRainbowCube4]

        #  Pilar final
        body6 = sg.SceneGraphNode('pilar_fin')
        body6.transform = tr.matmul([tr.translate(0.0, 0, 1.8),tr.scale(0.17, 0.17, 3.6)])
        body6.childs += [gpuRainbowCube5]

        #  Antena
        body7 = sg.SceneGraphNode('antena')
        body7.transform = tr.matmul([tr.translate(0.0, 0, 2.1),tr.scale(0.07, 0.07, 4)])
        body7.childs += [gpuRainbowCube6]


        transform_mono = sg.SceneGraphNode('empireStateTR')
        transform_mono.childs += [body, body2, body3, body4, body5, body6, body7]

        self.model = transform_mono


    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "model")



class WillisTower(object):

    def __init__(self, pipeline):
        gpuOrangeCube = createGPUShape(bs.createColorCube(1, 0.7, 0.24), pipeline)
        gpuPinkCube = createGPUShape(bs.createColorCube(1, 0.62, 0.76), pipeline)
        gpuGreenCube = createGPUShape(bs.createColorCube(0.619, 1, 0.627), pipeline)
        gpuBlueCube = createGPUShape(bs.createColorCube(0.619, 0.784, 1), pipeline)

        #  Base
        body = sg.SceneGraphNode('base')
        body.transform = tr.matmul([tr.translate(0.0, 0.125, 2),tr.scale(0.25, 0.5, 4)])
        body.childs += [gpuPinkCube]


        #  
        orange = sg.SceneGraphNode('naranjo')
        orange.transform = tr.matmul([tr.translate(0, 0, 1.5),tr.scale(0.25, 0.25, 3)])
        orange.childs += [gpuOrangeCube]

        orange_izq = sg.SceneGraphNode('naranjoLeft')
        orange_izq.transform = tr.translate(-0.25, 0, 0)
        orange_izq.childs += [orange]

        orange_der = sg.SceneGraphNode('naranjoRight')
        orange_der.transform = tr.translate(0.25, 0, 0)
        orange_der.childs += [orange]

        orange_back = sg.SceneGraphNode('naranjoBack')
        orange_back.transform = tr.translate(0, -0.25, 0)
        orange_back.childs += [orange]

        green = sg.SceneGraphNode('verde')
        green.transform = tr.matmul([tr.translate(0.0, 0.0, 1.25),tr.scale(0.25, 0.25, 2.5)])
        green.childs += [gpuGreenCube]

        green_der = sg.SceneGraphNode('verdeLeft')
        green_der.transform = tr.translate(0.25, 0.25, 0)
        green_der.childs += [green]

        green_izq = sg.SceneGraphNode('verdeLeft')
        green_izq.transform = tr.translate(-0.25, -0.25, 0)
        green_izq.childs += [green]


        blue = sg.SceneGraphNode('azul')
        blue.transform = tr.matmul([tr.translate(0.0, 0.0, 0.75),tr.scale(0.25, 0.25, 1.5)])
        blue.childs += [gpuBlueCube]

        blue_der = sg.SceneGraphNode('azulLeft')
        blue_der.transform = tr.translate(-0.25, 0.25, 0)
        blue_der.childs += [blue]

        blue_izq = sg.SceneGraphNode('azulRight')
        blue_izq.transform = tr.translate(0.25, -0.25, 0)
        blue_izq.childs += [blue]

        transform_mono = sg.SceneGraphNode('WillisTowerTR')
        transform_mono.childs += [body, orange_izq, orange_der, orange_back, green_der, green_izq, blue_der, blue_izq]

        self.model = transform_mono

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "model")



class BurjAlArab(object):

    def __init__(self, pipeline):
        gpuWhiteCube = createGPUShape(bs.createColorCube(0.95, 0.95, 0.95), pipeline)
        gpuLightBlueCube = createGPUShape(bs.createColorCube(0.28, 0.87, 0.92), pipeline)

        body = sg.SceneGraphNode('base')
        body.transform = tr.matmul([tr.translate(0.0, 0.3, 1.25),tr.scale(0.4, 0.2, 2.5)])
        body.childs += [gpuWhiteCube]
        
        pilar = sg.SceneGraphNode('pilar')
        pilar.transform = tr.matmul([tr.translate(0.0, 0.3, 1.6375),tr.scale(0.1, 0.1, 3.25)])
        pilar.childs += [gpuWhiteCube]
        
        delimitador = sg.SceneGraphNode('base')
        delimitador.transform = tr.matmul([tr.translate(0.0, -0.5, 2),tr.scale(1, 0.1, 4)])
        delimitador.childs += [gpuWhiteCube]

        delimitador2 = sg.SceneGraphNode('base')
        delimitador2.transform = tr.matmul([tr.translate(0.0, 0.5, 1.5),tr.scale(1, 0.1, 3)])
        delimitador2.childs += [gpuWhiteCube]


        alero = sg.SceneGraphNode('alero')
        alero.transform = tr.matmul([tr.translate(0.0, 0.35, 1.7),tr.scale(0.7, 0.2, 0.25)])
        alero.childs += [gpuWhiteCube]

        ventana1 = sg.SceneGraphNode('ventana1')
        ventana1.transform = tr.matmul([tr.translate(0.0, 0.025, 0.25),tr.scale(0.8, 0.35, 0.5)])
        ventana1.childs += [gpuLightBlueCube]

        ventana2 = sg.SceneGraphNode('ventana2')
        ventana2.transform = tr.matmul([tr.translate(0.0, -0.125, 0.5),tr.scale(0.8, 0.45, 0.5)])
        ventana2.childs += [gpuLightBlueCube]

        ventana3 = sg.SceneGraphNode('ventana3')
        ventana3.transform = tr.matmul([tr.translate(0.0, -0.125, 0.75),tr.scale(0.8, 0.65, 0.5)])
        ventana3.childs += [gpuLightBlueCube]

        ventana4 = sg.SceneGraphNode('ventana4')
        ventana4.transform = tr.matmul([tr.translate(0.0, -0.125, 1),tr.scale(0.8, 0.45, 0.5)])
        ventana4.childs += [gpuLightBlueCube]

        ventana5 = sg.SceneGraphNode('ventana5')
        ventana5.transform = tr.matmul([tr.translate(0.0, 0.025, 1.25),tr.scale(0.8, 0.35, 0.5)])
        ventana5.childs += [gpuLightBlueCube]

        ventana6 = sg.SceneGraphNode('ventana6')
        ventana6.transform = tr.matmul([tr.translate(0.0, 0.05, 1.5),tr.scale(0.8, 0.3, 0.5)])
        ventana6.childs += [gpuLightBlueCube]



        transform_mono = sg.SceneGraphNode('BurjAlArabTR')
        transform_mono.childs += [body, pilar, alero, ventana1, ventana2, ventana3, ventana4, ventana5, ventana6]

        self.model = transform_mono

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, "model")

class EmpireGround(object):

    def __init__(self, pipeline):
        gpu_ground = create_gpu_ground(bs.createTextureCube(), pipeline, "EmpireStateMaps.png")

        ground = sg.SceneGraphNode("ground")
        ground.transform = tr.scale(2, 2, 1)
        ground.childs += [gpu_ground]

        ground_tr = sg.SceneGraphNode('groundTR')
        ground_tr.childs += [ground]

        self.model = ground_tr
        self.gpu = gpu_ground

    def draw(self, pipeline):

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0, 0, 0),tr.scale(5, 5, 0)]))
        pipeline.drawCall(self.gpu)

class WillisGround(object):

    def __init__(self, pipeline):
        gpu_ground = create_gpu_ground(bs.createTextureCube(), pipeline, "WillisTowerMaps.png")

        ground = sg.SceneGraphNode("ground")
        ground.transform = tr.scale(2, 2, 1)
        ground.childs += [gpu_ground]

        ground_tr = sg.SceneGraphNode('groundTR')
        ground_tr.childs += [ground]

        self.model = ground_tr
        self.gpu = gpu_ground

    def draw(self, pipeline):
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0, 0, 0),tr.scale(5, 5, 0)]))
        pipeline.drawCall(self.gpu)

class BurjAlArabGround(object):

    def __init__(self, pipeline):
        gpu_ground = create_gpu_ground(bs.createTextureCube(), pipeline, "BurjAlArabMaps.png")

        ground = sg.SceneGraphNode("ground")
        ground.transform = tr.scale(2, 2, 1)
        ground.childs += [gpu_ground]

        ground_tr = sg.SceneGraphNode('groundTR')
        ground_tr.childs += [ground]

        self.model = ground_tr
        self.gpu = gpu_ground

    def draw(self, pipeline):
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0, 0, 0),tr.scale(5, 5, 0)]))
        pipeline.drawCall(self.gpu)