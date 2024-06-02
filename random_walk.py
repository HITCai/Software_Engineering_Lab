import numpy as np
import random
import tkinter as tk
from tkinter import messagebox

class Random_Walk:
    def __init__(self,graph):
        self.graph = graph



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

    # @staticmethod
    # def random_walk_process(matrix, word_list, random_word):
    #     # 获取出边到达的节点
    #     out_edge = [i for i in range(len(word_list)) if matrix[word_list.index(random_word)][i] != 0]
    #     # 如果不存在出边
    #     if len(out_edge) == 0:
    #         return None, None
    #     else:
    #         random_out_word = word_list[random.choice(out_edge)]
    #         return (random_word, random_out_word), random_out_word  # 返回随机游走的边和游走到的节点

