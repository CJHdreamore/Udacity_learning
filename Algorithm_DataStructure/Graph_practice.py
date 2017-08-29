class Node(object):
    def __init__(self,value):
        self.value = value
        self.edges = []


class Edge(object):
    def __init__(self,value,node_from,node_to):
        self.value = value
        self.node_from = node_from
        self.node_to = node_to

class Graph(object):
    def __init__(self,nodes = [],edges = []):
        self.nodes = nodes
        self.edges = edges

    def insert_node(self,new_node_val):
        new_node = Node(new_node_val)
        self.nodes.append(new_node)

    def insert_edge(self,new_edge_val,node_from_val,node_to_val):
        from_found = None
        to_found = None
        for node in self.nodes:
            if node_from_val == node.value:
                from_found = node
            if node_to_val == node.value:
                to_found = node
        if from_found == None:
            from_found = Node(node_from_val)
            self.nodes.append(from_found)
        if to_found == None:
            to_found = Node(node_to_val)
            self.nodes.append(to_found)
        new_edge = Edge(new_edge_val,from_found,to_found)
        from_found.edges.append(new_edge)
        to_found.edges.append(new_edge)
        self.edges.append(new_edge)

    def get_edge_list(self):
        '''Dont' return a list of edge objects
        Return a list of triples that looks like:
        (Edge Value,From Node Value,To Node Value)'''
        edge_list =[]
        for edge in self.edges:
            result = (edge.value,edge.node_from.value,edge.node_to.value)
            edge_list.append(result)
        return edge_list

    def get_adjacency_list(self):
        '''Return a list of lists.
        The indecies of the outer list represent "from" nodes.
        Each section in the list will stroe a list of tuples like
        (To Node,Edge Values)'''
        #[None, [(2, 100), (3, 101), (4, 102)], None, [(4, 103)], None]

        node_value = []
        for node in self.nodes:
            node_value.append(node.value)
        max_node_value = max(node_value)       # the max id of node in graph
        adjacency_list = [None] * (max_node_value + 1)   #initialize
        nodes = [None] * (max_node_value + 1)
        for node in self.nodes:
            nodes[node.value] = node          # set up a list which the index is the id of the node,the value is the object ot the associated node
        #print nodes

        for node in nodes:
            if node:
                edge_list = []
                for edge in node.edges:
                    if edge.node_from == node:
                        tuple = (edge.node_to.value,edge.value)
                        edge_list.append(tuple)
                if edge_list:
                   adjacency_list[node.value] = edge_list
        return adjacency_list

    def get_adjacency_matrix(self):
        '''Return a 2D list,Row numbers represent from nodes,
        column numbers represent to nodes.Store the edge values
        in each spot,and a 0 if no edge exists'''

        #looks like [[0,0,0,0,0],[0,0,100,101,102],[0,0,0,0,0],
        #            [0,0,0,0,103],[0,0,0,0,0] ]

        node_value = []
        for node in self.nodes:
            node_value.append(node.value)
        max_node_value = max(node_value)  # the max id of node in graph
        row_copy = [0] * (max_node_value+1)
        matrix = []
        for each_row in range(0,max_node_value + 1):
            matrix.append(row_copy)
        # finished initialization

        for node in self.nodes:
            row = [0] * (max_node_value + 1)
            if node.edges:
               for edge in node.edges:
                   if edge.node_from == node and edge.node_to:

                       row[edge.node_to.value] = edge.value
                       matrix[node.value] = row
                    # it's really troublesome for variables in python!!!!!

        return matrix

    # solution by Udacity
    def get_adj_list(self):
        max_index = self.find_max_index()
        adjacency_list = [None] * (max_index + 1)
        for edge in self.edges:
            if adjacency_list[edge.node_from.value]:
                adjacency_list[edge.node_from.value].append((edge.node_to.value,edge.value))
            else:
                adjacency_list[edge.node_from.value] = [(edge.node_to.value,edge.value)]
        return adjacency_list

    def get_adj_matrix(self):
        max_index = self.find_max_index()
        adjacency_matrix = [[0 for i in range(max_index + 1)] for j in range(max_index + 1)]

        for edge in self.edges:
            adjacency_matrix[edge.node_from.value][edge.node_to.value] = edge.value
        return adjacency_matrix

    def find_max_index(self):
        max_index = -1
        if len(self.nodes):
            for node in self.nodes:
                if node.value > max_index:
                    max_index = node.value
        return max_index








graph = Graph()
graph.insert_edge(100, 1, 2)
graph.insert_edge(101, 1, 3)
graph.insert_edge(102, 1, 4)
graph.insert_edge(103, 3, 4)

#print graph.get_edge_list()
#print graph.get_adjacency_list()

#print graph.get_adjacency_matrix()

print graph.get_adj_list()
print graph.get_adj_matrix()

############## Inspiring!!!!!#######################
# This practice gives me a big big big warning : in python, the same varible name will cause some unexpected
# results. if you change a varible,then every place that varible exsists will change at the same time!!!
# That's to say, we should really take care of the temporary viarble and global varible.
# Sometimes, it's smarter to replace creating new variables by using some longer phrases,just as the official Udacity solution tells us.

####################################################