import networkx as nx
import matplotlib.pyplot as plt
from tkinter import messagebox
class Calc_Shortest_Path:
    def __init__(self,graph):
        self.graph = graph


    def draw_graph(self):
        G = nx.DiGraph()
        for key, value in self.graph.items():
            key = list(key)
            node1 = key[0]
            node2 = key[1]
            G.add_edge(node1, node2, weight=value)
        return G

    def calc_shortest_path(self, word_1, word_2):
        key_tuples = list(self.graph.keys())
        word_set = set()
        for key_tuple in key_tuples:
            key_list = list(key_tuple)
            word_set.add(key_list[0])
            word_set.add(key_list[1])

        # word1和word2都为空
        if word_1 == '' and word_2 == '':
            messagebox.showerror("Error", "Both word inputs are empty.")

        # word1不为空且不在图中，word2为空或者在图中
        elif word_1 != '' and word_1 not in word_set and (word_2 in word_set or word_2 == ''):
            messagebox.showerror("Error", f"No '{word_1}' in the graph.")

        # word2不为空且不在图中，word1为空或者在图中
        elif word_2 != '' and word_2 not in word_set and (word_1 in word_set or word_1 == ''):
            messagebox.showerror("Error", f"No '{word_2}' in the graph.")

        # word1和word2都不为空且都不在图中
        elif word_1 not in word_set and word_2 not in word_set:
            messagebox.showerror("Error", f"No '{word_1}' and '{word_2}' in the graph.")

        # 可选功能：只输入了一个单词
        elif (word_1 == '' and word_2 in word_set) or (word_2 == '' and word_1 in word_set):
            # 调用draw_graph绘制图
            G = self.draw_graph()
            word_input = word_1 if word_1 != '' else word_2
            for word in word_set:
                try:
                    # 计算最短路径
                    min_path = nx.dijkstra_path(G, source=word_input, target=word)
                    # 计算最短路径长度
                    min_path_length = nx.dijkstra_path_length(G, source=word_input, target=word)
                    messagebox.showinfo("Shortest Path", f"Shortest path length between '{word_input}' and '{word}': {min_path_length}")

                except nx.NetworkXNoPath:
                    messagebox.showinfo("Shortest Path", f"No path between '{word_input}' and '{word}'.")

        # word1和word2都在图中
        elif word_1 in word_set and word_2 in word_set:
            # 调用draw_graph绘制图
            G = self.draw_graph()
            try:
                # 计算最短路径
                min_path = nx.dijkstra_path(G, source=word_1, target=word_2)
                # 计算最短路径长度
                min_path_length = nx.dijkstra_path_length(G, source=word_1, target=word_2)
                messagebox.showinfo("Shortest Path", f"Shortest path length between '{word_1}' and '{word_2}': {min_path_length}")

                pos = nx.spring_layout(G)
                labels = nx.get_edge_attributes(G, 'weight')
                nx.draw_networkx(G, pos, node_size=800)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

                edge_list = []
                for i in range(len(min_path) - 1):
                    edge_list.append((min_path[i], min_path[i + 1]))
                nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='m', width=4)
                plt.show()

            except nx.NetworkXNoPath:
                messagebox.showinfo("Shortest Path", f"No path between '{word_1}' and '{word_2}'.")