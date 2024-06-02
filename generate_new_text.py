from tkinter import messagebox
import random
from query_bridge_words import Query_Bridge_Words


class Generate_New_Text:
    def __init__(self,graph):
        self.graph = graph

    def generate_new_text(self, input_text):
        text_list = input_text.split(' ')
        text_lower = input_text.lower()
        text_lower_list = text_lower.split(' ')
        idx = 0  # 每向文本中加入一个桥接词之后，文本列表中后面的词的序号都增加了1，这时候需要在下次加入桥接词时向后移动序号
        for i in range(len(text_lower_list) - 1):
            word_1 = text_lower_list[i]
            word_2 = text_lower_list[i + 1]

            query_words = Query_Bridge_Words(graph=self.graph)
            bridge_word_list = query_words.query_bridge_words(word_1=word_1, word_2=word_2)
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




