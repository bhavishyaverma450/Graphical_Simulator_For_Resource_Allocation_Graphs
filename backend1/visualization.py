import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(nodes, edges, deadlock):
    G = nx.DiGraph()
    for node in nodes:
        G.add_node(node)
    for from_node, to_node in edges:
        G.add_edge(from_node, to_node)

    pos = nx.spring_layout(G)
    plt.figure()
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
    if deadlock:
        deadlock_nodes = [node for node in nodes if node in deadlock]
        nx.draw_networkx_nodes(G, pos, nodelist=deadlock_nodes, node_color='red')
    plt.show()
