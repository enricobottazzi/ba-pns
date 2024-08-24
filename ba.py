# Patterned after https://github.com/AlxndrMlk/Barabasi-Albert_Network
import networkx as nx
import numpy as np

class BarabasiAlbertGraph:
    def __init__(self, n, m, m0):
        """
        Initialize a Barabási-Albert scale-free graph.
        
        Parameters:
        n (int): Total number of nodes
        m (int): Number of edges to attach from a new node to existing nodes
        m0 (int): Initial number of nodes (must be >= m)
        """
        if m0 < m:
            raise ValueError("m0 must be greater than or equal to m")
        
        self.n = n
        self.m = m
        self.m0 = m0
        self.G = nx.complete_graph(m0)
        self.new_node = m0

    def generate(self):
        """Generate the Barabási-Albert graph."""
        print(f"Graph created. Number of nodes: {len(self.G.nodes())}")
        print("Adding nodes...")

        for count in range(self.n - self.m0):
            print(f"----------> Step {count} <----------")
            self.G.add_node(self.m0 + count)
            print(f"Node added: {self.m0 + count + 1}")
            
            for _ in range(self.m):
                self.add_edge()
            
            self.new_node += 1

        print(f"\nFinal number of nodes ({len(self.G.nodes())}) reached")
        return self.G

    def rand_prob_node(self):
        """Select a random node based on preferential attachment probabilities."""
        degrees = dict(self.G.degree())
        total_degree = sum(degrees.values())
        probabilities = [degree / total_degree for node, degree in degrees.items()]
        return np.random.choice(list(self.G.nodes()), p=probabilities)

    def add_edge(self):
        """Add a new edge using preferential attachment."""
        if len(self.G.edges()) == 0:
            random_proba_node = 0
        else:
            random_proba_node = self.rand_prob_node()
        
        new_edge = (self.new_node, random_proba_node)
        if new_edge in self.G.edges():
            print("Edge already exists. Trying again...")
            self.add_edge()
        else:
            self.G.add_edge(self.new_node, random_proba_node)
            print(f"Edge added: {self.new_node + 1} {random_proba_node + 1}")