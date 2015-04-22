from collections import defaultdict

pos_file  = open('/Users/warbean/filespace/data/pos_sentences.txt' , 'r', 1000)
dpt_file  = open('/Users/warbean/filespace/data/dpt_sentences.txt' , 'r', 1000)
verb_noun_dict = defaultdict(lambda: defaultdict(lambda: 0))
lino = -1
while True:
    lino += 1
    pos_sent = pos_file.readline().strip()
    dpt_sent = dpt_file.readline().strip()
    if pos_sent == '' or dpt_sent == '': break
    if pos_sent == "### can't get url!!!" or dpt_sent == "### can't get url!!!": continue
#    pos_list, dpt_list = process_sent(pos_sent, dpt_sent, verb_noun_dict)
#def process_sent(pos_sent, dpt_sent, verb_noun_dict):
    pos_sent = ' '.join(pos_sent.split('###'))
    pos_list = [token.rsplit('_', 1) for token in pos_sent.split(' ')]
    dpt_list = [dp.split(' ') for dp in dpt_sent.split('###') if dp != '']
    for dp in dpt_list:
        assert len(dp) == 3
        dp[0] = dp[0].rsplit('_', 1)
        if dp[1] == '-1': dp[1] = ['', '-1']
        else: dp[1] = dp[1].rsplit('_', 1)
        assert len(dp[0]) == len(dp[1]) == 2
        dp[0][1] = int(dp[0][1])
        dp[1][1] = int(dp[1][1])
    for dp in dpt_list:
        assert len(dp) == 3
        assert len(dp[0]) == 2
        assert len(dp[1]) == 2
        assert type(dp[2]) == str

    for dp in dpt_list:
        [dpt_word1, index1] = dp[0]
        [dpt_word2, index2] = dp[1]
        dependency = dp[2]
        [pos_word1, pos1] = pos_list[index1]
        [pos_word2, pos2] = pos_list[index2]
        try:
            assert dpt_word1 == pos_word1
            assert dpt_word2 == pos_word2
        except:
            continue

        if pos1 == 'v' and pos2[0] == 'n':
            verb_noun_dict[(dpt_word1, dpt_word2)][dependency] += 1
            verb_noun_dict[(dpt_word1, dpt_word2)]['all'] += 1

