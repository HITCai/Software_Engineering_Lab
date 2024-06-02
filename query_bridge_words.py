import sys


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

    # def queryBridgeWords(self, word_1, word_2):
    #     bridge_word_list = find_bridge_words(self.graph,word_1,word_2)
    #     if bridge_word_list == 'NOT_IN':
    #         print('No word1 or word2 in the graph!')
    #     else:
    #         self.print_words(word_1,word_2,bridge_word_list)

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


