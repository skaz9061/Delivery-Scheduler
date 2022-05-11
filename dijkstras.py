# Classes and methods necessary to implement Dijkstra's Algorithm


class Node:
    """
    Node in a graph.
    """
    def __init__(self, id):
        # Time complexity O(1)
        self.distance = float('inf')
        self.pred = None
        self.id = id

    def reset(self):
        """
        Resets the Node to its initial state.

        :return:
        """
        # Time complexity O(1)
        self.distance = float('inf')
        self.pred = None

    def __str__(self):
        # Time complexity O(1)
        """
        Convert the Node into a string representation.

        :return: the string representation of the Node
        """
        s = f'Node( {self.id}, distance: {self.distance}, predecessor: {None if self.pred is None else self.pred.id} )'
        return s


class Graph:
    """
    A graph that consists of Nodes and their edge weights.
    """
    def __init__(self):
        # Time complexity O(1)
        self.adjacency_list = {}
        self.edge_weights = {}
        self.dijkstras = False  # A flag to know if Dijkstra's Algorithm has been run on the graph

    def add_node(self, node):
        """
        Adds a node to the graph.

        :param Node node: the Node object to add
        :return:
        """
        # Time complexity O(1)
        self.adjacency_list[node] = set()

    def add_directed_edge(self, from_node, to_node, weight):
        """
        Adds a directed edge to the graph.

        :param Node from_node: the Node object at the tail of the directed edge
        :param Node to_node: the Node object at the head of the directed edge
        :param float weight: the edge weight
        :return:
        """
        # Time complexity O(1)
        self.edge_weights[(from_node, to_node)] = weight
        self.adjacency_list[from_node].add(to_node)

    def add_undirected_edge(self, from_node, to_node, weight):
        """
        Adds an undirected edge to the graph.

        :param Node from_node: the Node object at one end of the edge
        :param Node to_node: the Node object at the other end of the edge
        :param float weight: the edge weight
        :return:
        """
        # Time complexity O(1)
        self.add_directed_edge(from_node, to_node, weight)
        self.add_directed_edge(to_node, from_node, weight)

    def reset(self):
        """
        Resets all the Nodes of the graph to their initial state.

        :return:
        """
        # Time complexity O(n)
        self.dijkstras = False

        for node in self.adjacency_list:  # O(n)
            node.reset()

    def get_node(self, key):
        """
        Get the node object where the id matches the key.

        :param str key: the key to match the Node's id
        :return: the Node object if found, None if not found
        :rtype: Node
        """
        # Time complexity O(n)
        for node in self.adjacency_list:  # O(n)
            if node.id == key:
                return node
        return None


def run_dijkstras(g, start_node):
    """
    Implements Dijkstra's Algorithm on the graph.

    Finds the shortest path from the start node to all other nodes in the graph.

    :param Graph g: the Graph object
    :param Node start_node: the starting node
    :return:
    """
    # Time complexity O(n^2)
    g.dijkstras = True

    unvisited_nodes = list(g.adjacency_list.keys()).copy()

    start_node.distance = 0.0

    while len(unvisited_nodes) > 0:  # O(n)
        smallest_i = 0

        for i in range(1, len(unvisited_nodes)):  # O(n)
            if unvisited_nodes[i].distance < unvisited_nodes[smallest_i].distance:
                smallest_i = i

        current_node = unvisited_nodes.pop(smallest_i)

        for adj_node in g.adjacency_list[current_node]:  # O(n)
            edge_weight = g.edge_weights[(current_node, adj_node)]

            alt_path_distance = current_node.distance + edge_weight
            if alt_path_distance < adj_node.distance:
                adj_node.distance = alt_path_distance
                adj_node.pred = current_node


def get_shortest_path(g, start_node, end_node):
    """
    Gets the shortest path from the start node to the end node using Dijkstra's algorithm.

    :param Graph g: the Graph object
    :param Node start_node: the Start Node
    :param Node end_node: the End Node
    :return: the path as a list in the order of Nodes visited, None if the start node or end node not in the graph
    :rtype: list[Node]
    """
    # Time complexity O(n^2)

    if start_node in g.adjacency_list.keys() and end_node in g.adjacency_list.keys():
        if not g.dijkstras:
            run_dijkstras(g, start_node)  # O(n^2)

        path = [end_node]

        while path[0] != start_node:  # O(n)
            path = [path[0].pred] + path

        return path
    return None


def build_graph(location_hash):
    """
    Builds the graph object from a Chaining Hash Table of Location objects.

    :param ChainingHashTable[str, Location] location_hash: the Chaining Hash Table of Location objects
    :return: the Graph object
    :rtype: Graph
    """
    # Time complexity O(n^3)
    g = Graph()

    # Add all the nodes to the graph
    for bucket in location_hash.table:  # O(n^2)
        for [k, _] in bucket:  # O(n)
            g.add_node(Node(k))

    # Add all the edges to the graph
    for node in list(g.adjacency_list.keys()):  # O(n^3)
        from_location = location_hash.lookup(node.id)  # O(n)
        for key in from_location.destinations:  # O(n^2)
            edge_weight = from_location.get_distance(key)
            to_node = g.get_node(key)  # O(n)
            g.add_undirected_edge(node, to_node, edge_weight)

    return g
