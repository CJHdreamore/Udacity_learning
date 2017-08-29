class Node(object):
    def __init__(self,value):
        self.value = value
        self.edges = []
        self.visited = False

class Edge(object):
    def __init__(self,value,node_from,node_to):
        self.value = value
        self.node_from = node_from
        self.node_to = node_to


class Graph(object):
    def __init__(self,nodes = None,edges = None):
        self.nodes = nodes or []
        self.edges = nodes or []
        self.node_names = []
        self._node_map = {}


    def set_node_names(self,names):
        '''The Nth name in names should correspond to
        node Number N. Node numbers are starting at 0'''
        self.node_names = list(names)

    def insert_node(self,new_node_val):
        'Insert a new node with value new_node_val'
        new_node = Node(new_node_val)
        self.nodes.append(new_node)
        self._node_map[new_node_val] = new_node
        return new_node

    def insert_edge(self,new_edge_val,node_from_val,node_to_val):
        'Insert a new edge, creating new nodes if necessary'
        nodes = {node_from_val:None,node_to_val:None}
        for node in self.nodes:
            if node.value in nodes:
                nodes[node.value] = node
                if all(nodes.values()):
                    break
        for node_val in nodes:
            nodes[node_val] = nodes[node_val] or self.insert_node(node_val)
        node_from = nodes[node_from_val]
        node_to = nodes[node_to_val]
        new_edge = Edge(new_edge_val,node_from,node_to)
        node_from.edges.append(new_edge)
        node_to.edges.append(new_edge)
        self.edges.append(new_edge)


    def get_edge_list(self):
        '''Return a list of triples that looks like:
        (Edge Value,From Node,To Node)'''
        return [(e.value,e.node_from.value,e.node_to.value)
                 for e in self.edges]

    def get_edge_list_names(self):
        '''Return a list of tirples that looks like this:
        (Edge Value,From Node name, To node name)'''
        return [(edge.value,
                 self.node_names[edge.node_from.value],
                 self.node_names[edge.node_to.value])
                for edge in self.edges]

    def get_adjacency_list(self):
        '''Return a list of lists.
        Each section in the list will store a list of tuples
        (To Node,Edge Value)'''
        max_index = self.find_max_index()
        adjacency_list = [[] for _ in range(max_index)]
        for edge in self.edges:
            from_value,to_value = edge.node_from.value,edge.node_to.value
            adjacency_list[from_value].append((to_value,edge.value))
        return [a or None for a in adjacency_list] # replace []'s with None

    def get_adjacency_list_names(self):
        '''(To Node Name,Edge Value)
        Node names should come from the names set with set_node_names'''
        adjacency_list = self.get_adjacency_list()
        def convert_to_names(pair,graph=self):
            node_number,value = pair
            return (graph.node_names[node_number],value)
        def map_conversion(adjacency_list_for_node):
            if adjacency_list_for_node is None:
                return None
            return map(convert_to_names,adjacency_list_for_node)
        return [map_conversion(adjacency_list_for_node)for adjacency_list_for_node in adjacency_list]

    def get_adjacency_matix(self):
        '''Return  a matrix,Row numbers represent from nodes,
        column numbers represent to nodes.
        Store the edge values in each spot and a 0 if no edge'''
        max_index = self.find_max_index()
        adjacency_matrix =[ [0] *(max_index) for _ in range (max_index)]
        for edge in self.edges:
            from_index,to_index = edge.node_from.value,edge.node_to.value
            adjacency_matrix[from_index][to_index] =edge.value
        return adjacency_matrix

    def find_max_index(self):
        '''Return the highest found node number
        or the length of the node names if se with set_node_names()'''

        if len(self.node_names) > 0:
            return len(self.node_names)
        max_index = -1
        if len(self.nodes):
            for node in self.nodes:
                if node.value > max_index:
                    max_index = node.value
        return max_index

    def find_node(self,node_number):
        '''Return the node with value node_number or None'''
        return self._node_map.get(node_number)

    def _clear_visited(self):
        for node in self.nodes:
            node.visited = False
































graph = Graph()
graph.set_node_names(('Mountain View',   # 0
                      'San Francisco',   # 1
                      'London',          # 2
                      'Shanghai',        # 3
                      'Berlin',          # 4
                      'Sao Paolo',       # 5
                      'Bangalore'))      # 6
#print graph.node_names
graph.insert_edge(51, 0, 1)     # MV <-> SF
graph.insert_edge(51, 1, 0)     # SF <-> MV
graph.insert_edge(9950, 0, 3)   # MV <-> Shanghai
graph.insert_edge(9950, 3, 0)   # Shanghai <-> MV
graph.insert_edge(10375, 0, 5)  # MV <-> Sao Paolo
graph.insert_edge(10375, 5, 0)  # Sao Paolo <-> MV
graph.insert_edge(9900, 1, 3)   # SF <-> Shanghai
graph.insert_edge(9900, 3, 1)   # Shanghai <-> SF
graph.insert_edge(9130, 1, 4)   # SF <-> Berlin
graph.insert_edge(9130, 4, 1)   # Berlin <-> SF
graph.insert_edge(9217, 2, 3)   # London <-> Shanghai
graph.insert_edge(9217, 3, 2)   # Shanghai <-> London
graph.insert_edge(932, 2, 4)    # London <-> Berlin
graph.insert_edge(932, 4, 2)    # Berlin <-> London
graph.insert_edge(9471, 2, 5)   # London <-> Sao Paolo
graph.insert_edge(9471, 5, 2)   # Sao Paolo <-> London

import pprint
pp = pprint.PrettyPrinter(indent = 2)

print 'Edge List'
pp.pprint(graph.get_edge_list_names())

print '\nAdjacency List'
pp.pprint(graph.get_adjacency_list_names())

print "\nAdjacency Matrix"
pp.pprint(graph.get_adjacency_matix())

print"\nDepth First Search"
pp.pprint(graph.dfs_names(2))

