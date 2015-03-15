import jieba
from WikiPOSTagger import pos_tag

class WikiEntityRecognizer:

    # 妈蛋这里一定要回来用正则重写！！！
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
