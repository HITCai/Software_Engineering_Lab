import sys
import string
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

class Create_Directed_Graph:
    def __init__(self,file_name):
        self.file_name = file_name

    def createDirectedGraph(self):
        # 文本预处理
        with open(self.file_name,'r') as f:
            text = f.read()

            # 将换行和回车符替换为空格
            text = text.replace('\n',' ').replace('\r',' ')

            # 将标点符号替换为空格
            punctuations = string.punctuation # 获取所有标点符号
            for punctuation in punctuations:
                text = text.replace(punctuation,' ')

            # 忽略非字母字符
            text = ''.join(word for word in text if word.isalpha() or word.isspace())

            # 转换成小写字母
            text = text.lower()

        text = [s for s in text.split(' ') if len(s) != 0] # 获得单词列表

        # 生成有向图
        # 创建字典保存两点之间的权值 键：(word1,word2) 值：word1和word2相邻次数
        graph = {}
        for i in range(len(text) - 1):
            word1 = text[i]
            word2 = text[i + 1]

            # 如果这两个单词之前不在边权字典里，那就将它俩加入
            if (word1,word2) not in graph.keys():
                graph[(word1,word2)] = 1
            else:
                graph[(word1, word2)] = graph[(word1,word2)] + 1

        return graph


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
        G = draw_graph(graph=graph)

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx(G,pos,node_size=800)
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        plt.savefig('directed_graph/graph_' + self.file_name + '_.png')
        plt.show()

def find_bridge_words(graph, word_1, word_2):
    key_tuples = list(graph.keys())
    word_set = set()
    for key_tuple in key_tuples:
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
            if (word_1, word) in key_tuples and (word, word_2) in key_tuples:
                bridge_word_list.append(word)

        return bridge_word_list

class Query_Bridge_Words:
    def __init__(self, graph):
        self.graph = graph



    def print_words(self,word_1,word_2,bridge_word_list):
        num = len(bridge_word_list)

        if num == 0:
            print('No bridge words from word1 to word2!')

        elif num == 1:
            print('The bridge word from "', word_1, '" to "', word_2, '" is:', bridge_word_list[0])
        else:
            sys.stdout.write('The bridge words from "')
            sys.stdout.write(word_1)
            sys.stdout.write('" to "')
            sys.stdout.write(word_2)
            sys.stdout.write('" are:')
            for i in range(num - 1):
                sys.stdout.write(bridge_word_list[i])
                sys.stdout.write(',')
            sys.stdout.write('and ')
            sys.stdout.write(bridge_word_list[-1])
            sys.stdout.write('.')

    def queryBridgeWords(self, word_1, word_2):
        bridge_word_list = find_bridge_words(self.graph,word_1,word_2)
        if bridge_word_list == 'NOT_IN':
            print('No word1 or word2 in the graph!')
        else:
            self.print_words(word_1,word_2,bridge_word_list)

class Generate_New_Text:
    def __init__(self,graph):
        self.graph = graph

    def generateNewText(self,inputText):
        text_list = inputText.split(' ')
        text_lower = inputText.lower()
        text_lower_list = text_lower.split(' ')
        idx = 0  # 每向文本中加入一个桥接词之后，文本列表中后面的词的序号都增加了1，这时候需要在下次加入桥接词时向后移动序号
        for i in range(len(text_lower_list) - 1):
            word_1 = text_lower_list[i]
            word_2 = text_lower_list[i + 1]
            bridge_word_list = find_bridge_words(self.graph,word_1,word_2)
            if bridge_word_list == 'NOT_IN':
                text_list = text_list
            elif len(bridge_word_list) == 1:
                text_list.insert(i + 1 + idx,bridge_word_list[0])
                idx = idx + 1
            elif len(bridge_word_list) > 1:
                bridge_word_index = random.randint(0,len(bridge_word_list) - 1)
                text_list.insert(i + 1 + idx, bridge_word_list[bridge_word_index])
                idx = idx + 1

        new_Text = ' '.join(word for word in text_list)
        print('生成的文本为：')
        print(new_Text)

class Calc_Shortest_Path:
    def __init__(self,graph):
        self.graph = graph

    def calcShortestPath(self,word_1,word_2):
        key_tuples = list(self.graph.keys())
        word_set = set()
        for key_tuple in key_tuples:
            key_list = list(key_tuple)
            word_set.add(key_list[0])
            word_set.add(key_list[1])

        # word1和word2都为空
        if word_1 == '' and word_2 == '':
            print('两次输入均为空')

        # word1不为空且不在图中，word2为空或者在图中
        elif word_1 != '' and word_1 not in word_set and (word_2 in word_set or word_2 == ''):
            print('No',word_1,'in the graph!')

        # word2不为空且不在图中，word1为空或者在图中
        elif word_2 != '' and word_2 not in word_set and (word_1 in word_set or word_1 == ''):
            print('No',word_2,'in the graph!')

        # word1和word2都不为空且都不在图中
        elif word_1 not in word_set and word_2 not in word_set:
            print('No',word_1,'and',word_2,'in the graph!')

        # 可选功能：只输入了一个单词
        elif (word_1 == '' and word_2 in word_set) or (word_2 == '' and word_1 in word_set):
            # 调用draw_graph绘制图
            G = draw_graph(self.graph)
            word_input = word_1 if word_1 != '' else word_2
            for word in word_set:
                try:
                    # 计算最短路径
                    min_path = nx.dijkstra_path(G, source=word_input, target=word)
                    # 计算最短路径长度
                    min_path_lenth = nx.dijkstra_path_length(G, source=word_input, target=word)
                    print(word_input,'和',word,'最短路径长度为：', min_path_lenth)

                except nx.NetworkXNoPath:
                    print(word_input, '和', word, '不可达')

        # word1和word2都在图中
        elif word_1 in word_set and word_2 in word_set:
            # 调用draw_graph绘制图
            G = draw_graph(self.graph)
            try:
                # 计算最短路径
                min_path = nx.dijkstra_path(G, source=word_1, target=word_2)
                # 计算最短路径长度
                min_path_lenth = nx.dijkstra_path_length(G, source=word_1, target=word_2)
                print('最短路径长度为：', min_path_lenth)

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
                print(word_1,'和',word_2,'不可达')

class Random_Walk:
    def __init__(self,graph):
        self.graph = graph

    # 随机游走过程
    @staticmethod
    def random_walk_process(matrix,word_list,random_word):
        # 获取出边到达的节点
        out_edge = [i for i in range(len(word_list)) if matrix[word_list.index(random_word)][i] != 0]
        # 如果不存在出边
        if len(out_edge) == 0:
            return None,None
        else:
            random_out_word = word_list[random.choice(out_edge)]
            return (random_word,random_out_word),random_out_word # 返回随机游走的边和游走到的节点

    def randomWalk(self):
        key_tuples = list(self.graph.keys())
        word_set = set()
        for key_tuple in key_tuples:
            key_list = list(key_tuple)
            word_set.add(key_list[0])
            word_set.add(key_list[1])
        word_list = list(word_set)

        # 把字典存储的图转换成邻接矩阵形式
        matrix = np.zeros([len(word_list),len(word_list)])
        for tuple in key_tuples:
            word_1_index = word_list.index(tuple[0])
            word_2_index = word_list.index(tuple[1])
            matrix[word_1_index,word_2_index] = self.graph[tuple]

        # 保存游走结果
        random_walk_list = []
        # 保存游走的边
        random_walk_edges = []
        # 随机选择起点
        random_word = random.choice(word_list)
        random_walk_list.append(random_word)
        while 1:
            random_walk_edge, random_word = Random_Walk.random_walk_process(matrix=matrix, word_list=word_list,
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
        print('随机游走结果为：',output)

        # 写入输出文件
        output_file = './output_file/output.txt'
        with open(output_file,'w') as f:
            f.write(output)

def main():
    # 获取文本文件名
    args = sys.argv
    # file_name = args[1]
    file_name = '1.txt'

    # 生成有向图
    create_graph = Create_Directed_Graph(file_name=file_name)
    graph = create_graph.createDirectedGraph()

    # 功能选择
    print('请选择功能：')
    print('1--展示有向图')
    print('2--查询桥接词')
    print('3--根据bridge word生成新文本')
    print('4--计算两个单词之间的最短路径')
    print('5--随机游走')
    print('请输入功能序号(1～5)：')
    index = input()
    index = int(index)

    # 展示有向图
    if index == 1:
        show_graph = Show_Directed_Graph(file_name=file_name)
        G = show_graph.showDirectedGraph(graph)

    # 查询桥接词
    elif index == 2:
        print('请输入单词1:')
        word_1 = input()
        print('请输入单词2：')
        word_2 = input()

        query_words = Query_Bridge_Words(graph=graph)
        query_words.queryBridgeWords(word_1=word_1,word_2=word_2)


    # 根据bridge word生成新文本
    elif index == 3:
        print('请输入新文本：')
        inputText = input()
        generate_text = Generate_New_Text(graph=graph)
        generate_text.generateNewText(inputText=inputText)


    # 计算两个单词之间的最短路径
    elif index == 4:
        print('请输入单词1:')
        word_1 = input()
        print('请输入单词2：')
        word_2 = input()

        calc_path = Calc_Shortest_Path(graph=graph)
        calc_path.calcShortestPath(word_1=word_1, word_2=word_2)

    # 随机游走
    elif index == 5:
        randomwalk = Random_Walk(graph=graph)
        randomwalk.randomWalk()
if __name__ == "__main__":
    main()