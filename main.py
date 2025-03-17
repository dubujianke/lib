# https://github.khronos.org/glTF-Tutorials/gltfTutorial/gltfTutorial_020_Skins.html
import pygltflib
import pathlib
import struct
import pygltflib
import numpy as np
import struct

buffer = struct.pack("ihb", 1, 2, 3)
print(repr(buffer))
print(struct.unpack( "ihb" ,  buffer ))
buffer = struct.pack("!ihb", 1, 2, 3)
print(repr(buffer))
print(struct.unpack( "!ihb" ,  buffer ))

from pygltflib import (
    ARRAY_BUFFER,
    ELEMENT_ARRAY_BUFFER,
    FLOAT,
    SCALAR,
    UNSIGNED_BYTE,
    UNSIGNED_INT,
    UNSIGNED_SHORT,
    VEC3,
    Accessor,
    AccessorSparseIndices,
    Attributes,
    Buffer,
    BufferFormat,
    BufferView,
    GLTF2,
    Image,
    ImageFormat,
    Mesh,
    Material,
    Node,
    PbrMetallicRoughness,
    Primitive,
    Property,
    Scene,
    Sparse,
)

fname = pathlib.Path("./2.gltf")
gltf = pygltflib.GLTF2().load(fname)
mesh = gltf.meshes[0]


def printPoint(primitive):
    accessor = gltf.accessors[primitive.attributes.POSITION]
    bufferView = gltf.bufferViews[accessor.bufferView]
    buffer = gltf.buffers[bufferView.buffer]
    data = gltf.get_data_from_buffer_uri(buffer.uri)
    vertices = []
    for i in range(accessor.count):
        byteStride = 12
        if bufferView.byteStride != None:
            byteStride = bufferView.byteStride
        index = bufferView.byteOffset + accessor.byteOffset + i * byteStride  # the location in the buffer of this vertex
        d = data[index:index + byteStride]  # the vertex data
        v = struct.unpack("<fff", d)  # convert from base64 to three floats
        vertices.append(v)
    print(len(vertices))


def printIndice(primitive):
    accessor = gltf.accessors[primitive.indices]
    bufferView = gltf.bufferViews[accessor.bufferView]
    buffer = gltf.buffers[bufferView.buffer]
    data = gltf.get_data_from_buffer_uri(buffer.uri)
    vertices = []
    for i in range(accessor.count):
        byteStride = 2
        if bufferView.byteStride != None:
            byteStride = bufferView.byteStride
        index = bufferView.byteOffset + accessor.byteOffset + i * byteStride  # the location in the buffer of this vertex
        d = data[index:index + byteStride]
        v = struct.unpack("<H", d)  # convert from base64 to three floats
        vertices.append(v[0])

    vertices = np.asarray(vertices)
    vertices = vertices.reshape(-1, 3)
    print(len(vertices))


def printJoint(primitive):
    accessor = gltf.accessors[primitive.attributes.JOINTS_0]
    bufferView = gltf.bufferViews[accessor.bufferView]
    buffer = gltf.buffers[bufferView.buffer]
    data = gltf.get_data_from_buffer_uri(buffer.uri)
    vertices = []
    for i in range(accessor.count):
        byteStride = 2
        if bufferView.byteStride != None:
            byteStride = bufferView.byteStride
        index = bufferView.byteOffset + accessor.byteOffset + i * byteStride  # the location in the buffer of this vertex
        d = data[index:index + byteStride]
        v = struct.unpack("<HHHH", d)  # convert from base64 to three floats
        vertices.append(v)
    vertices = np.asarray(vertices)
    vertices = vertices.reshape(-1, 4)
    print(len(vertices))
    vecJoints = vertices
    return vecJoints

def printWeight(primitive):
    accessor = gltf.accessors[primitive.attributes.WEIGHTS_0]
    bufferView = gltf.bufferViews[accessor.bufferView]
    buffer = gltf.buffers[bufferView.buffer]
    data = gltf.get_data_from_buffer_uri(buffer.uri)
    vertices = []
    for i in range(accessor.count):
        byteStride = 0
        if bufferView.byteStride != None:
            byteStride = bufferView.byteStride
        index = bufferView.byteOffset + accessor.byteOffset + i * byteStride  # the location in the buffer of this vertex
        d = data[index:index + byteStride]
        v = struct.unpack("<ffff", d)  # convert from base64 to three floats
        vertices.append(v)
    vertices = np.asarray(vertices)
    vertices = vertices.reshape(-1, 4)
    print(len(vertices))
    vecJointWight = vertices
    return vecJointWight

def printJointInverse(invIdx):
    accessor = gltf.accessors[invIdx]
    bufferView = gltf.bufferViews[accessor.bufferView]
    buffer = gltf.buffers[bufferView.buffer]
    data = gltf.get_data_from_buffer_uri(buffer.uri)
    vertices = []
    for i in range(accessor.count):
        byteStride = 64
        if bufferView.byteStride != None:
            byteStride = bufferView.byteStride
        index = bufferView.byteOffset + accessor.byteOffset + i * byteStride  # the location in the buffer of this vertex
        d = data[index:index + byteStride]
        v = struct.unpack("<ffffffffffffffff", d)  # convert from base64 to three floats
        vertices.append(v)
        print(v)
    vertices = np.asarray(vertices)
    vertices = vertices.reshape(-1, 4, 4)

    inverseMatrix = vertices
    return inverseMatrix

for primitive in mesh.primitives:
    printPoint(primitive)
    printIndice(primitive)
    vecJoints = printJoint(primitive)
    vecJointWight = printWeight(primitive)
    nodes = gltf.nodes
    joints = gltf.skins[0].joints
    allNodes = []
    for i, node in enumerate(nodes):
        name = node.name
        extras = node.extras
        children = node.children
        matrix = node.matrix
        # print(i, name, matrix, '\n', children)
        print(i, name, children)
        allNodes.append([i, name, children])
    jointNodes = []
    jointIdxs = gltf.skins[0].joints
    print(jointIdxs)
    print(gltf.skins[0].skeleton)
    jointNodes = list(filter(lambda x: x[0] in jointIdxs, allNodes))
    # for node in jointNodes:
    #     print(node)

    skin = gltf.skins[0]
    # inverseMatrix = skin.inverseBindMatrices
    # inverseMatrix = printJointInverse(inverseMatrix)

    # print(joints)
    # for i in range(0, len(inverseMatrix)):
    #     print(i, '\n', inverseMatrix[i])
