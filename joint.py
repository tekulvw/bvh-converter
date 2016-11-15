import numpy as np
from collections import namedtuple
from cgkit.bvh import Node


class Joint(Node, object):
    def __init__(self, *args, **kwargs):
        super(Joint, self).__init__(*args, **kwargs)

    @property
    def total_offset(self):
        off = np.ndarray(self.offset)
        node = self.parent
        while node is not None:
            # We can do this because position will be ZERO for all nodes
            #   except root
            off = np.add(off, np.ndarray(node.position))
            off = np.add(off, np.ndarray(node.offset))
            node = node.parent
        return off


Frame_Joint = namedtuple('Frame_Joint', ('name position transformation_matrix'
                                         ' offset channels parent children'))
# This is gonna be used as a 'light-weight' data time for per-frame Joint
#   stuff. `transformation_matrix` is going to be cumulative (so we don't)
#   have to recalculate up to the root every time inside one frame.
