import tkinter as tk
from tkinter import messagebox
import string
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np


class DirectedGraphProcessor:
    def __init__(self):
        self.graph = {}

    def create_directed_graph(self, file_name):
        # 文本预处理
        with open(file_name, 'r') as f:
            text = f.read()

            # 将换行和回车符替换为空格
            text = text.replace('\n', ' ').replace('\r', ' ')

            # 将标点符号替换为空格
            punctuations = string.punctuation  # 获取所有标点符号
            for punctuation in punctuations:
                text = text.replace(punctuation, ' ')

            # 忽略非字母字符
            text = ''.join(word for word in text if word.isalpha() or word.isspace())

            # 转换成小写字母
            text = text.lower()

        text = [s for s in text.split(' ') if len(s) != 0]  # 获得单词列表

        # 生成有向图
        # 创建字典保存两点之间的权值 键：(word1,word2) 值：word1和word2相邻次数
        self.graph = {}
        for i in range(len(text) - 1):
            word1 = text[i]
            word2 = text[i + 1]

            # 如果这两个单词之前不在边权字典里，那就将它俩加入
            if (word1, word2) not in self.graph.keys():
                self.graph[(word1, word2)] = 1
            else:
                self.graph[(word1, word2)] += 1

        messagebox.showinfo("Success", "成功生成有向图.")

    def show_directed_graph(self):
        G = nx.DiGraph()
        for key, value in self.graph.items():
            key = list(key)
            node1 = key[0]
            node2 = key[1]
            G.add_edge(node1, node2, weight=value)

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx(G, pos, node_size=800)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()

    def query_bridge_words(self, word_1, word_2):
        word_set = set()
        for key_tuple in self.graph.keys():
            key_list = list(key_tuple)
            word_set.add(key_list[0])
            word_set.add(key_list[1])

        # 如果word1或word2不在图中
        if word_1 not in word_set or word_2 not in word_set:
            return 'NOT_IN'

        # 如果word1和word2都在图中
        else:
            bridge_word_list = []  # 保存桥接词的列表
            # 遍历单词集合，寻找符合桥接条件的单词
            for word in word_set:
                if (word_1, word) in self.graph.keys() and (word, word_2) in self.graph.keys():
                    bridge_word_list.append(word)

            return bridge_word_list

    def generate_new_text(self, input_text):
        text_list = input_text.split(' ')
        text_lower = input_text.lower()
        text_lower_list = text_lower.split(' ')
        idx = 0  # 每向文本中加入一个桥接词之后，文本列表中后面的词的序号都增加了1，这时候需要在下次加入桥接词时向后移动序号
        for i in range(len(text_lower_list) - 1):
            word_1 = text_lower_list[i]
            word_2 = text_lower_list[i + 1]
            bridge_word_list = self.query_bridge_words(word_1, word_2)
            if bridge_word_list == 'NOT_IN':
                text_list = text_list
            elif len(bridge_word_list) == 1:
                text_list.insert(i + 1 + idx, bridge_word_list[0])
                idx += 1
            elif len(bridge_word_list) > 1:
                bridge_word_index = random.randint(0, len(bridge_word_list) - 1)
                text_list.insert(i + 1 + idx, bridge_word_list[bridge_word_index])
                idx += 1

        new_text = ' '.join(word for word in text_list)
        messagebox.showinfo("Generated Text", f"Generated text: {new_text}")

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

    def draw_graph(self):
        G = nx.DiGraph()
        for key, value in self.graph.items():
            key = list(key)
            node1 = key[0]
            node2 = key[1]
            G.add_edge(node1, node2, weight=value)
        return G

    def random_walk(self):
        key_tuples = list(self.graph.keys())
        word_set = set()
        for key_tuple in key_tuples:
            key_list = list(key_tuple)
            word_set.add(key_list[0])
            word_set.add(key_list[1])
        word_list = list(word_set)

        # 把字典存储的图转换成邻接矩阵形式
        matrix = np.zeros([len(word_list), len(word_list)])
        for tuple in key_tuples:
            word_1_index = word_list.index(tuple[0])
            word_2_index = word_list.index(tuple[1])
            matrix[word_1_index, word_2_index] = self.graph[tuple]

        # 保存游走结果
        random_walk_list = []
        # 保存游走的边
        random_walk_edges = []
        # 随机选择起点
        random_word = random.choice(word_list)
        random_walk_list.append(random_word)
        while 1:
            random_walk_edge, random_word = self.random_walk_process(matrix=matrix, word_list=word_list,
                                                                     random_word=random_word)
            # 如果不存在出边
            if random_walk_edge is None:
                break
            # 如果出现重复的边
            elif random_walk_edge in random_walk_edges:
                random_walk_list.append(random_word)
                break
            else:
                random_walk_list.append(random_word)
                random_walk_edges.append(random_walk_edge)

        output = ' '.join(word for word in random_walk_list)
        messagebox.showinfo("Random Walk Result", f"Random walk result: {output}")

        # 写入输出文件
        output_file = './output_file/output.txt'
        with open(output_file, 'w') as f:
            f.write(output)

    @staticmethod
    def random_walk_process(matrix, word_list, random_word):
        # 获取出边到达的节点
        out_edge = [i for i in range(len(word_list)) if matrix[word_list.index(random_word)][i] != 0]
        # 如果不存在出边
        if len(out_edge) == 0:
            return None, None
        else:
            random_out_word = word_list[random.choice(out_edge)]
            return (random_word, random_out_word), random_out_word  # 返回随机游走的边和游走到的节点

def main():
    processor = DirectedGraphProcessor()

    def create_directed_graph_button_click():
        file_name = file_name_entry.get()
        processor.create_directed_graph(file_name)

    def show_directed_graph_button_click():
        processor.show_directed_graph()

    def query_bridge_words_button_click():
        word_1 = word1_entry.get()
        word_2 = word2_entry.get()
        bridge_word_list = processor.query_bridge_words(word_1, word_2)
        if bridge_word_list == 'NOT_IN':
            messagebox.showinfo("Bridge Words", "No word1 or word2 in the graph.")
        else:
            bridge_words_str = ', '.join(bridge_word_list)
            messagebox.showinfo("Bridge Words", f"Bridge words from '{word_1}' to '{word_2}': {bridge_words_str}")

    def generate_new_text_button_click():
        input_text = input_text_entry.get()
        processor.generate_new_text(input_text)

    def calc_shortest_path_button_click():
        word_1 = word1_entry.get()
        word_2 = word2_entry.get()
        processor.calc_shortest_path(word_1, word_2)

    def random_walk_button_click():
        processor.random_walk()

    # 创建主窗口
    root = tk.Tk()
    root.title("Directed Graph Processor")

    # 创建标签和输入框
    file_name_label = tk.Label(root, text="文件名称:")
    file_name_label.grid(row=0, column=0)

    file_name_entry = tk.Entry(root, width=50)
    file_name_entry.grid(row=0, column=1)

    word1_label = tk.Label(root, text="单词1:")
    word1_label.grid(row=1, column=0)

    word1_entry = tk.Entry(root, width=50)
    word1_entry.grid(row=1, column=1)

    word2_label = tk.Label(root, text="单词2:")
    word2_label.grid(row=2, column=0)

    word2_entry = tk.Entry(root, width=50)
    word2_entry.grid(row=2, column=1)

    input_text_label = tk.Label(root, text="输入文本:")
    input_text_label.grid(row=3, column=0)

    input_text_entry = tk.Entry(root, width=50)
    input_text_entry.grid(row=3, column=1)

    # 创建按钮
    create_directed_graph_button = tk.Button(root, text="生成有向图",
                                             command=create_directed_graph_button_click)
    create_directed_graph_button.grid(row=4, column=0, columnspan=2, pady=5)

    show_directed_graph_button = tk.Button(root, text="展示有向图", command=show_directed_graph_button_click)
    show_directed_graph_button.grid(row=5, column=0, columnspan=2, pady=5)

    query_bridge_words_button = tk.Button(root, text="查询桥接词", command=query_bridge_words_button_click)
    query_bridge_words_button.grid(row=6, column=0, columnspan=2, pady=5)

    generate_new_text_button = tk.Button(root, text="生成新文本", command=generate_new_text_button_click)
    generate_new_text_button.grid(row=7, column=0, columnspan=2, pady=5)

    calc_shortest_path_button = tk.Button(root, text="计算最短路径", command=calc_shortest_path_button_click)
    calc_shortest_path_button.grid(row=8, column=0, columnspan=2, pady=5)

    random_walk_button = tk.Button(root, text="随机游走", command=random_walk_button_click)
    random_walk_button.grid(row=9, column=0, columnspan=2, pady=5)

    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()
