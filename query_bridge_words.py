import sys


class Query_Bridge_Words:
    def __init__(self, graph):
        self.graph = graph

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


