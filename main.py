import tkinter as tk
from tkinter import messagebox
import sys
from create_directed_graph import Create_Directed_Graph
from show_directed_graph import Show_Directed_Graph
from query_bridge_words import Query_Bridge_Words
from generate_new_text import Generate_New_Text
from calc_shortest_path import Calc_Shortest_Path
from random_walk import Random_Walk

def main():
    # graph = None
    G = None
    def create_directed_graph_button_click():
        global graph
        file_name = file_name_entry.get()
        create_graph = Create_Directed_Graph(file_name=file_name)
        graph = create_graph.create_directed_graph()

    def show_directed_graph_button_click():
        global G
        file_name = file_name_entry.get()
        show_graph = Show_Directed_Graph(file_name=file_name)
        G = show_graph.showDirectedGraph(graph)

    def query_bridge_words_button_click():
        word_1 = word1_entry.get()
        word_2 = word2_entry.get()
        query_words = Query_Bridge_Words(graph=graph)
        bridge_word_list = query_words.query_bridge_words(word_1=word_1, word_2=word_2)
        if bridge_word_list == 'NOT_IN':
            messagebox.showinfo("Bridge Words", "No word1 or word2 in the graph.")
        else:
            bridge_words_str = ', '.join(bridge_word_list)
            messagebox.showinfo("Bridge Words", f"Bridge words from '{word_1}' to '{word_2}': {bridge_words_str}")

    def generate_new_text_button_click():
        input_text = input_text_entry.get()
        generate_text = Generate_New_Text(graph=graph)
        generate_text.generate_new_text(input_text)

    def calc_shortest_path_button_click():
        word_1 = word1_entry.get()
        word_2 = word2_entry.get()
        calc_path = Calc_Shortest_Path(graph=graph)
        calc_path.calc_shortest_path(word_1, word_2)

    def random_walk_button_click():
        randomwalk = Random_Walk(graph=graph)
        randomwalk.random_walk()

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