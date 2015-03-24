import jieba
from WikiPOSTagger import pos_tag

# 妈蛋这里一定要回来用正则重写！！！
class WikiEntityRecognizer:

    def recognize(self, token_list):
        token_list = self.join_entity(token_list, "'", "'", 3)
        token_list = self.join_entity(token_list, "[", "]", 2)
        return token_list

    def join_entity(self, token_list, left_del, right_del, repeat_count):
        left_count = 0
        right_count = 0
        inside = False
        new_token_list = []

        for i, token in enumerate(token_list):
            if token.word == left_del:
                left_count += 1
            elif token.word == right_del:
                right_count += 1
            else:
                if left_count == repeat_count:
                    inside = True
                    begin_index = i
                elif right_count == repeat_count:
                    inside = False
                    end_index = i - 2
                    entity = "".join([token.word for token in token_list[begin_index:end_index]])
                    print(entity)
                    new_token = jieba.posseg.pair(entity, 'NE')
                left_count = right_count = 0
                new_token_list.append(token)
        return new_token_list

"""
    def recognize(self, token_list):
        quote_count = 0
        quote_hit = False
        new_token_list = []

        for i, token in enumerate(token_list):
            if token.word == "'":
                if quote_hit == True:
                    quote_count -= 1
                else:
                    quote_count += 1
            elif quote_hit == False:
                new_token_list.append(token)
            if quote_count == 3 and quote_hit == False:
                quote_hit = True
                begin_index = i + 1
            elif quote_count == 0 and quote_hit == True:
                quote_hit = False
                end_index = i - 2
                entity = ''.join([token.word for token in token_list[begin_index : end_index]])
                new_token = jieba.posseg.pair(entity, 'NE')
                new_token_list.append(new_token)

        return new_token_list
"""

def entity_recognize():
    entity_recognizer = WikiEntityRecognizer()
    for token_list in pos_tag():
        yield entity_recognizer.recognize(token_list)
        break

if __name__ == "__main__":
    for token_list in entity_recognize():
        for token in token_list:
            print(token, end = ' ')
        print("\n====================================")
