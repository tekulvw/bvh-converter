# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is the Python Computer Graphics Kit.
#
# The Initial Developer of the Original Code is Matthias Baas.
# Portions created by the Initial Developer are Copyright (C) 2004
# the Initial Developer. All Rights Reserved.
#
# Minor modifications made to make PEP8 compatible and switch to new-style
# classes by Matt Graham (March 2016).
#
# Contributor(s):
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
# $Id: bvh.py,v 1.1 2005/02/06 22:26:02 mbaas Exp $

# \file bvh.py
# Contains the BVHReader class.

import string


class Node(object):
    """Skeleton hierarchy node."""

    def __init__(self, root=False):
        self.name = None
        self.channels = []
        self.offset = (0, 0, 0)
        self.children = []
        self._is_root = root

    @property
    def is_root(self):
        return self._is_root

    @property
    def is_end_site(self):
        return len(self.children) == 0


class BvhReader(object):
    """BioVision Hierarchical (.bvh) file reader."""

    def __init__(self, filename):

        self.filename = filename
        # A list of unprocessed tokens (strings)
        self._token_list = []
        # The current line number
        self._line_num = 0

        # Root node
        self.root = None
        self._node_stack = []

        # Total number of channels
        self.num_channels = 0

    def on_hierarchy(self, root):
        pass

    def on_motion(self, frames, dt):
        pass

    def on_frame(self, values):
        pass

    def read(self):
        """Read the entire file."""
        with open(self.filename, 'r') as self._file_handle:
            self.read_hierarchy()
            self.on_hierarchy(self.root)
            self.read_motion()

    def read_motion(self):
        """Read the motion samples."""
        # No more tokens (i.e. end of file)? Then just return
        try:
            tok = self.token()
        except StopIteration:
            return

        if tok != "MOTION":
            raise SyntaxError("Syntax error in line %d: 'MOTION' expected, "
                              "got '%s' instead" % (self._line_num, tok))

        # Read the number of frames
        tok = self.token()
        if tok != "Frames:":
            raise SyntaxError("Syntax error in line %d: 'Frames:' expected, "
                              "got '%s' instead" % (self._line_num, tok))

        frames = self.int_token()

        # Read the frame time
        tok = self.token()
        if tok != "Frame":
            raise SyntaxError("Syntax error in line %d: 'Frame Time:' "
                              "expected, got '%s' instead"
                              % (self._line_num, tok))
        tok = self.token()
        if tok != "Time:":
            raise SyntaxError("Syntax error in line %d: 'Frame Time:' "
                              "expected, got 'Frame %s' instead"
                              % (self._line_num, tok))

        dt = self.float_token()

        self.on_motion(frames, dt)

        # Read the channel values
        for i in range(frames):
            s = self.read_line()
            a = s.split()
            if len(a) != self.num_channels:
                raise SyntaxError("Syntax error in line %d: %d float values "
                                  "expected, got %d instead"
                                  % (self._line_num, self.num_channels,
                                     len(a)))
            values = list(map(lambda x: float(x), a))  # In Python 3 map returns map-object, not a list. Can't slice.
            self.on_frame(values)

    def read_hierarchy(self):
        """Read the skeleton hierarchy."""
        tok = self.token()
        if tok != "HIERARCHY":
            raise SyntaxError("Syntax error in line %d: 'HIERARCHY' expected, "
                              "got '%s' instead" % (self._line_num, tok))
        tok = self.token()
        if tok != "ROOT":
            raise SyntaxError("Syntax error in line %d: 'ROOT' expected, "
                              "got '%s' instead" % (self._line_num, tok))

        self.root = Node(root=True)
        self._node_stack.append(self.root)
        self.read_node()

    def read_node(self):
        """Read the data for a node."""

        # Read the node name (or the word 'Site' if it was a 'End Site' node)
        name = self.token()
        self._node_stack[-1].name = name

        tok = self.token()
        if tok != "{":
            raise SyntaxError("Syntax error in line %d: '{' expected, "
                              "got '%s' instead" % (self._line_num, tok))

        while 1:
            tok = self.token()
            if tok == "OFFSET":
                x = self.float_token()
                y = self.float_token()
                z = self.float_token()
                self._node_stack[-1].offset = (x, y, z)
            elif tok == "CHANNELS":
                n = self.int_token()
                channels = []
                for i in range(n):
                    tok = self.token()
                    if tok not in ["Xposition", "Yposition", "Zposition",
                                   "Xrotation", "Yrotation", "Zrotation"]:
                        raise SyntaxError("Syntax error in line %d: Invalid "
                                          "channel name: '%s'"
                                          % (self._line_num, tok))
                    channels.append(tok)
                self.num_channels += len(channels)
                self._node_stack[-1].channels = channels
            elif tok == "JOINT":
                node = Node()
                self._node_stack[-1].children.append(node)
                self._node_stack.append(node)
                self.read_node()
            elif tok == "End":
                node = Node()
                self._node_stack[-1].children.append(node)
                self._node_stack.append(node)
                self.read_node()
            elif tok == "}":
                if self._node_stack[-1].is_end_site:
                    self._node_stack[-1].name = "End Site"
                self._node_stack.pop()
                break
            else:
                raise SyntaxError("Syntax error in line %d: Unknown "
                                  "keyword '%s'" % (self._line_num, tok))

    def int_token(self):
        """Return the next token which must be an int. """
        tok = self.token()
        try:
            return int(tok)
        except ValueError:
            raise SyntaxError("Syntax error in line %d: Integer expected, "
                              "got '%s' instead" % (self._line_num, tok))

    def float_token(self):
        """Return the next token which must be a float."""
        tok = self.token()
        try:
            return float(tok)
        except ValueError:
            raise SyntaxError("Syntax error in line %d: Float expected, "
                              "got '%s' instead" % (self._line_num, tok))

    def token(self):
        """Return the next token."""

        # Are there still some tokens left? then just return the next one
        if self._token_list:
            tok = self._token_list[0]
            self._token_list = self._token_list[1:]
            return tok

        # Read a new line
        s = self.read_line()
        self.create_tokens(s)
        return self.token()

    def read_line(self):
        """Return the next line.

        Empty lines are skipped. If the end of the file has been
        reached, a StopIteration exception is thrown.  The return
        value is the next line containing data (this will never be an
        empty string).
        """
        # Discard any remaining tokens
        self._token_list = []
        # Read the next line
        while 1:
            s = self._file_handle.readline()
            self._line_num += 1
            if s == "":
                raise StopIteration
            return s

    def create_tokens(self, s):
        """Populate the token list from the content of s."""
        s = s.strip()
        a = s.split()
        self._token_list = a
