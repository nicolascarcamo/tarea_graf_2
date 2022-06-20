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

        body = sg.SceneGraphNode('body')
        body.transform = tr.scale(1,1,4)
        body.childs += [gpuRainbowCube]

        transform_mono = sg.SceneGraphNode('empireStateTR')
        transform_mono.transform = tr.identity()
        transform_mono.childs += [body]

        self.model = transform_mono
        self.gpu = gpuRainbowCube
        self.gpu1 = gpuRainbowCube1
        

    def draw(self, pipeline):
        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0, 0, 0.6), tr.scale(1, 1, 0.6)]))
        #pipeline.drawCall(self.gpu)
        #glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0, 0, 1.2),tr.scale(0.8, 0.8, 1.2)]))
        #pipeline.drawCall(self.gpu1)
        sg.drawSceneGraphNode(self.model, pipeline, "model")



class WillisTower(object):

    def __init__(self, pipeline):
        gpuRainbowCube = createGPUShape(bs.createRainbowCube(), pipeline)

    def draw(self, pipeline):
        return


class BurjAlArab(object):

    def __init__(self, pipeline):
        gpuRainbowCube = createGPUShape(bs.createRainbowCube(), pipeline)

    def draw(self, pipeline):
        return

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
        #self.model.transform = tr.translate(0, 0, 0)
        #sg.drawSceneGraphNode(self.model, pipeline, "transform")
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.matmul([tr.translate(0, 0, 0),tr.scale(5, 5, 0)]))
        pipeline.drawCall(self.gpu)