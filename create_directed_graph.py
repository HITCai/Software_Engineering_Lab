import string

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

# x = Create_Directed_Graph('1.txt')
# x.createDirectedGraph()