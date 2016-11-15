import numpy as np
from recordtype import recordtype
from cgkit.bvh import Node
import logging

log = logging.getLogger("converter.joint")


class Joint(Node, object):
    def __init__(self, *args, **kwargs):
        super(Joint, self).__init__(*args, **kwargs)

    @property
    def total_offset(self):
        log.debug("own offset: {}".format(self.offset))
        off = self.offset
        node = self.parent
        while node is not None:
            # We can do this because position will be ZERO for all nodes
            #   except root
            off = np.add(off, np.array(node.position))
            off = np.add(off, np.array(node.offset))
            node = node.parent
        return off


Frame_Joint = recordtype('Frame_Joint', ('name position transformation_matrix'
                                         ' offset total_offset channels parent'
                                         ' children'))
# This is gonna be used as a 'light-weight' data time for per-frame Joint
#   stuff. `transformation_matrix` is going to be cumulative (so we don't)
#   have to recalculate up to the root every time inside one frame.
