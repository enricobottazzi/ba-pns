from ba import BarabasiAlbertGraph

ba_graph = BarabasiAlbertGraph(n=1000, m=5, m0=5)
G = ba_graph.generate()
alpha = ba_graph.measure_alpha()
print(f"Alpha: {alpha}")
ba_graph.plot_degree_distribution()
