from ba import BarabasiAlbertGraph

ba_graph = BarabasiAlbertGraph(n=10000, m=5, m0=5)
G = ba_graph.generate()
ba_graph.plot_degree_distribution()
