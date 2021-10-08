# Copyright 2021 Peter Zick

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import bpy


def zero_shader_node_locations(nodes):
    max_width = 0
    for node in nodes:
        node.location = 0, 0
        if node.width > max_width:
            max_width = node.width
    return max_width


def arrange_shader_nodes():
    # Get the active material
    mat = bpy.context.active_object.active_material
    mat_nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Set all nodes to location (0,0)
    max_width = zero_shader_node_locations(mat_nodes)

    node_map = {}
    in_only = []
    
    # Map the node links
    for node in mat_nodes:
        node_map[node.name] = {'in': [], 'out': []}
        index = 0
        # Get the node inputs in array order (top to bottom)
        for input in node.inputs:
            if len(input.links) > 0:
                node_map[node.name]['in'].append((index, input.links[0].from_node.name))
            index += 1
        index = 0
        # Get the node outputs in array order (top to bottom)
        for output in node.outputs:
            if len(output.links) > 0:
                node_map[node.name]['out'].append((index, output.links[0].to_node.name))
            index += 1
            
        # Register input-only nodes
        if node_map[node.name]['out'] == []:
            in_only.append(node.name)

    queue = in_only
    # Position all nodes from the input only end, using the input ordering to help alignment
    while len(queue) > 0:
        node = queue[0]
        if len(queue) > 1:
            queue = queue[1:]
        else:
            queue = []
        index = -1
        for input in node_map[node]['in']:
            index += 1
            input = input[1]
            queue.append(input)
            if mat_nodes[input].location[0] > mat_nodes[node].location[0] - 100 - max_width:
                mat_nodes[input].location[0] = mat_nodes[node].location[0] - 100 - max_width
            if mat_nodes[input].location[1] > mat_nodes[node].location[1] - max_width * index:
                mat_nodes[input].location[1] = mat_nodes[node].location[1] - max_width * index
        

#zero_shader_node_locations(bpy.context.active_object.active_material.node_tree.nodes)
arrange_shader_nodes()
