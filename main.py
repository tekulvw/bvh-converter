from __future__ import print_function, division
import sys
import numpy as np
import csv

from cgkit.bvh import BVHReader
import cgkit.bvh
from joint import Joint

cgkit.bvh.Node = Joint

"""
Based on: http://www.dcs.shef.ac.uk/intranet/research/public/resmes/CS0111.pdf

Notes:
 - For each frame we have to recalculate from root
 - End sites are semi important (used to calculate length of the toe? vectors)
"""


def rotationXMat(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([1, 0, 0,
                     0, c, -s,
                     0, s, c])


def rotationYMat(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([c, 0, s,
                     0, 1, 0,
                     -s, 0, c])


def rotationZMat(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([c, -s, 0,
                     s, c, 0,
                     0, 0, 1])


def rotationMat(x=None, y=None, z=None, order='zxy'):
    if x is None or y is None or z is None:
        raise ValueError("x, y, and z must be defined.")
    x_mat = rotationXMat(x)
    y_mat = rotationYMat(y)
    z_mat = rotationZMat(z)
    loc = locals()
    first = np.cross(loc[order[0] + "_mat"], loc[order[1] + "_mat"])
    second = np.cross(first, loc[order[2] + "_mat"])
    return second


def transform_matrix(total_offset, parent_rot_matrix=None):
    ret = np.zeros((4, 4))
    ret[:3, :3] = parent_rot_matrix
    ret[3, :3] = total_offset
    ret[3, 3] = 1
    return ret


class Converter(BVHReader, object):
    def __init__(self, *args, **kwargs):
        super(Converter, self).__init__(*args, **kwargs)
        self.depth_first_channels = []
        self.depth_first_nodes = []
        self.root_node = None
        self.frames = []
        self.offsets = {}
        self.frame_count = 0
        self.dt = 0

    def generate_frame_key_order(self, node):
        if not node.isEndSite():
            attrs = [node.name + "." + chan for chan in node.channels]
            self.depth_first_channels.extend(attrs)
            for child in node.children:
                self.generate_frame_key_order(child)

    def generate_nodes(self, parent, node):
        if not node.isEndSite():
            node.parent = parent
            """if node.parent is None:
                node.transform_matrix = transform_matrix()
            else:
                node.transform_matrix = \
                    transform_matrix(parent.transform_matrix)"""
            setattr(self, node.name, node)
            self.depth_first_nodes.append(node)
            self.offsets[node.name] = node.offset
            map(lambda kid: self.generate_nodes(node, kid), node.children)

    def onHierarchy(self, root):
        self.root_node = root
        self.generate_nodes(None, root)
        self.generate_frame_key_order(root)

    def onFrame(self, values):
        for attr, val in zip(self.depth_first_channels, values):
            setattr(self, attr, val)
        self.frames.append(values)

    def onMotion(self, frames, dt):
        self.frame_count = frames
        self.dt = dt

    def dump_frames(self, output="output.csv"):
        header = self.depth_first_channels
        with open('test.csv', 'w') as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(header)
            for frame in self.frames:
                writer.writerow(frame)


if __name__ == "__main__":
    fname = sys.argv[1]
    print("Input filename: {}".format(fname))
    c = Converter(fname)
    c.read()
    print(c.depth_first_channels)
    c.dump_frames()
