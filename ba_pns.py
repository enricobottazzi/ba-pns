# Patterned after https://github.com/AlxndrMlk/Barabasi-Albert_Network
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import powerlaw
from math import exp

class PaymentNetworkSimulated:
    def __init__(self, n, m_in, m_out, m0, variable_edges=False):
        """        
        Initialize a Simulated Payment Network based on Barabási-Albert scale-free algorithm
        
        Parameters:
        n (int): Total number of nodes in the network
        m_in (int): Number of incoming edges to attach from a new node to existing nodes
        m_out (int): Number of outgoing edges to attach from a new node to existing nodes
        m0 (int): Initial number of nodes (must be >= max(m_in, m_out))
        variable_edges (bool): If True, at each step, m_in and m_out are randomly shuffled
        """
        if m0 < max(m_in, m_out):
            raise ValueError("m0 must be greater than or equal to max(m_in, m_out)")
        
        self.n = n
        self.m_in = m_in
        self.m_out = m_out
        self.m0 = m0
        self.variable_edges = variable_edges
        self.G = nx.complete_graph(m0, create_using=nx.DiGraph())
        self.new_node = m0
        self.amount_matrix = np.zeros((n, n))

    def generate(self):
        """Generate the Barabási-Albert directed graph."""
        print(f"Graph created. Number of nodes: {len(self.G.nodes())}")
        print("Adding nodes...")


        for count in range(self.n - self.m0):
            print(f"----------> Step {count} <----------")
            self.G.add_node(self.m0 + count)
            print(f"Node added: {self.m0 + count + 1}")

            m_in_step = self.m_in
            m_out_step = self.m_out

            if self.variable_edges:
                if np.random.rand() < 0.5:
                    m_in_step, m_out_step = m_out_step, m_in_step
            
            for _ in range(m_in_step):
                self.add_edge(incoming=True)
                
            for _ in range(m_out_step):
                self.add_edge(incoming=False)
            
            self.new_node += 1

        print(f"\nFinal number of nodes ({len(self.G.nodes())}) reached")
        print(f"Final number of edges is ({len(self.G.edges())})")

    def rand_prob_node(self, incoming=True):
        """
        Select a random node based on preferential attachment probabilities.
        
        Parameters:
        incoming (bool): If True, select node based on in-degree. If False, based on out-degree.
        """
        if incoming:
            degrees = dict(self.G.in_degree())
        else:
            degrees = dict(self.G.out_degree())

        total_degree = sum(degrees.values())
        if total_degree == 0:
            probabilities = [1 / len(degrees) for _ in degrees]
        else:
            probabilities = [degree / total_degree for node, degree in degrees.items()]
        
        return np.random.choice(list(self.G.nodes()), p=probabilities)

    def add_edge(self, incoming=True):
        """
        Add a new edge using preferential attachment.
        
        Parameters:
        incoming (bool): If True, add an incoming edge to the new node. If False, add an outgoing edge.
        """
        if incoming:
            random_proba_node = self.rand_prob_node(incoming=False)
            new_edge = (random_proba_node, self.new_node)
        else:
            random_proba_node = self.rand_prob_node(incoming=True)
            new_edge = (self.new_node, random_proba_node)
        
        if new_edge in self.G.edges():
            print("Edge already exists. Trying again...")
            self.add_edge(incoming)
        else:
            self.G.add_edge(*new_edge)
            amount = self.sample_amount(new_edge)
            self.amount_matrix[new_edge[0], new_edge[1]] = amount
            print(f"Edge added: {new_edge[0] + 1} -> {new_edge[1] + 1}, with amount: {amount}")

    def sample_amount(self, edge):
        """
        Sample the amount of an `edge` based on simulator of [SC13]
        """
        source, target = edge
        d = min(self.G.out_degree(source), self.G.in_degree(target))
        v = np.random.normal(1, 0.2)
        c = d * exp(v)
        return c

    def calculate_node_total_amounts(self):
        """
        Calculate the total amount of incoming and outgoing edges for each node.
        
        Returns:
        dict: A dictionary where keys are node indices and values are tuples (incoming_amount, outgoing_amount)
        """
        node_amounts = {}
        for node in self.G.nodes():
            incoming_amount = sum(self.amount_matrix[:, node])
            outgoing_amount = sum(self.amount_matrix[node, :])
            node_amounts[node] = (incoming_amount, outgoing_amount)
        
        return node_amounts
    
    def measure_alpha(self, distribution):
        """
        Measure the alpha value of the given distribution.
        
        Parameters:
        distribution (list): A list of values representing the distribution to analyze
        
        Returns:
        float: The alpha value of the power law fit
        """
        results = powerlaw.Fit(distribution)
        return results.power_law.alpha
        

    def plot_degree_distribution(self):
        """Plot the in-degree and out-degree distributions on a log-log scale."""
        in_degrees = [degree for node, degree in self.G.in_degree()]
        out_degrees = [degree for node, degree in self.G.out_degree()]
        
        alpha_in = self.measure_alpha(in_degrees)
        alpha_out = self.measure_alpha(out_degrees)
        
        plt.figure(figsize=(10, 6))
        plt.hist(in_degrees, bins=np.logspace(np.log10(1), np.log10(max(in_degrees)), num=50), 
                 density=True, alpha=0.5, label=f'In-degree (α = {alpha_in:.2f})')
        plt.hist(out_degrees, bins=np.logspace(np.log10(1), np.log10(max(out_degrees)), num=50), 
                 density=True, alpha=0.5, label=f'Out-degree (α = {alpha_out:.2f})')
        
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Degree')
        plt.ylabel('Frequency')
        plt.title('In-degree and Out-degree Distributions (Log-Log Scale)')
        plt.legend()
        plt.grid(True, which="both", ls="-", alpha=0.2)
        plt.savefig('degree_distribution.png')
        plt.close()

    def plot_amount_distribution(self):
        """Plot the total incoming and outgoing amount distributions on a log-log scale."""
        node_amounts = self.calculate_node_total_amounts()
        incoming_amounts = [cap[0] for cap in node_amounts.values()]
        outgoing_amounts = [cap[1] for cap in node_amounts.values()]

        alpha_incoming = self.measure_alpha(incoming_amounts)
        alpha_outgoing = self.measure_alpha(outgoing_amounts)

        plt.figure(figsize=(10, 6))
        
        plt.hist(incoming_amounts, bins=np.logspace(np.log10(min(incoming_amounts)), np.log10(max(incoming_amounts)), num=50), 
                 density=True, alpha=0.5, label=f'Incoming amount (α = {alpha_incoming:.2f})')
        plt.hist(outgoing_amounts, bins=np.logspace(np.log10(min(outgoing_amounts)), np.log10(max(outgoing_amounts)), num=50), 
                 density=True, alpha=0.5, label=f'Outgoing amount (α = {alpha_outgoing:.2f})')
        
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Total amount')
        plt.ylabel('Frequency')
        plt.title('Incoming and Outgoing Amount Distributions (Log-Log Scale)')
        plt.legend()
        plt.grid(True, which="both", ls="-", alpha=0.2)
        plt.savefig('amount_distribution.png')
        plt.close()