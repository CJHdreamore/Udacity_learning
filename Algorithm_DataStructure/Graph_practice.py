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
        adjacency_list = []
        for node in self.nodes:
            if node.edges:
                for edge in node.edges:
                    edge_list = []
                    if edge.node_from == node:
                        some = (edge.node_to.value, edge.value)
                        edge_list.append(some)

                    else:
                        edge_list = None
                    adjacency_list.append(edge_list)
        return adjacency_list








graph = Graph()
graph.insert_edge(100, 1, 2)
graph.insert_edge(101, 1, 3)
graph.insert_edge(102, 1, 4)
graph.insert_edge(103, 3, 4)

#print graph.get_edge_list()
print graph.get_adjacency_list()