# Patterned after https://github.com/AlxndrMlk/Barabasi-Albert_Network
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

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

    def plot_degree_distribution(self):
        """Plot the degree distribution P(k) on a log-log scale and fit a power law."""
        degree_counts = nx.degree_histogram(self.G)
        degree_probabilities = [count / sum(degree_counts) for count in degree_counts]
        
        # Prepare data for plotting
        x = np.array(range(1, len(degree_probabilities) + 1))
        y = np.array(degree_probabilities)
        
        # Remove zeros for log-log plot
        nonzero_mask = y > 0
        x_nonzero = x[nonzero_mask]
        y_nonzero = y[nonzero_mask]
        
        # Fit a power law using linear regression on log-log scale
        log_x = np.log(x_nonzero)
        log_y = np.log(y_nonzero)
        slope, intercept, r_value, _, _ = stats.linregress(log_x, log_y)
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.loglog(x_nonzero, y_nonzero, 'bo', alpha=0.6, label='Observed data')
        plt.loglog(x_nonzero, np.exp(intercept) * x_nonzero**slope, 'r-', 
                   label=f'Fitted power law (γ = {-slope:.2f})')
        
        plt.title('Degree Distribution P(k) - Log-Log Scale with Power Law Fit')
        plt.xlabel('Degree k')
        plt.ylabel('Probability P(k)')
        plt.legend()
        
        # Add text box with fit information
        fit_info = (f"Power law fit:\n"
                    f"P(k) ∝ k^(-γ)\n"
                    f"γ = {-slope:.2f}\n"
                    f"R² = {r_value**2:.3f}")
        plt.text(0.95, 0.95, fit_info, transform=plt.gca().transAxes, 
                 verticalalignment='top', horizontalalignment='right',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        # save to a file
        plt.savefig("degree_distribution.png")
        print(f"Estimated power law exponent (γ): {-slope:.2f}")
        print(f"R² value: {r_value**2:.3f}")
