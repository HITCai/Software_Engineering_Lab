import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph):
    G = nx.DiGraph()
    for key, value in graph.items():
        key = list(key)
        node1 = key[0]
        node2 = key[1]
        G.add_edge(node1, node2, weight=value)

    return G

class Show_Directed_Graph:
    def __init__(self,file_name):
        self.file_name = file_name

    def showDirectedGraph(self,graph):

        G = nx.DiGraph()
        for key, value in graph.items():
            key = list(key)
            node1 = key[0]
            node2 = key[1]
            G.add_edge(node1, node2, weight=value)

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx(G, pos, node_size=800)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()
