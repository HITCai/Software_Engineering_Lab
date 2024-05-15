import sys
from create_directed_graph import Create_Directed_Graph
from show_directed_graph import Show_Directed_Graph
from query_bridge_words import Query_Bridge_Words
from generate_new_text import Generate_New_Text
from calc_shortest_path import Calc_Shortest_Path
from random_walk import Random_Walk

def main():
    # 获取文本文件名
    args = sys.argv
    file_name = args[1]
    # file_name = '1.txt'

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