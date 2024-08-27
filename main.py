from ba_pns.ba_pns import PaymentNetworkSimulated

payment_network_graph = PaymentNetworkSimulated(n=6000, m_in=4, m_out=3, m0=4, swap_m_in_and_m_out=True)
payment_network_graph.generate()
payment_network_graph.plot_degree_distribution()
payment_network_graph.plot_amount_distribution()