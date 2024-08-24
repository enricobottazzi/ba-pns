from ba_pns import PaymentNetworkSimulated

payment_network_graph = PaymentNetworkSimulated(n=1000, m_in=5, m_out=5, m0=5)
payment_network_graph.generate()
payment_network_graph.plot_degree_distribution()
payment_network_graph.plot_amount_distribution()