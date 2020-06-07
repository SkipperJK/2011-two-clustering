from pymongo import MongoClient
from core.model.Triple import Triple

conn = MongoClient('10.132.141.255', 27017)
db = conn['SinaNews']
collet = db['result_20191121']


corsor = collet.find({})
print(corsor.count())
# corsor.skip().limit()

'''语料问题：
    1. 包含很多日文     -》 如何过滤日文
'''

'''
问题一： 就是这里的主谓关系可能主语大多数时名词，但是动宾关系的话宾语可能时动词，这怎么处理
    1. 只提取主语和宾语都是名词的三元组   -》 目前使用这种方法
    2. 其他处理方法
    
问题二： 提取的主语和宾语有可能时代词，就是需要使用代指消解。
    1. 找中文相关方面的实现。

问题三： 三元组是否要完整的三元组
    1. 完整三元组，有主语和宾语  -》目前使用这种方法
    2. 有主语或者宾语其中至少一个
    3. 两个都没有也可以
'''
def find_sub_obj(trigger, words):
    sub = None
    obj = None
    trigger_id = trigger['id']
    for i, word in enumerate(words):
        if i+1 == trigger_id:
            continue
        if word['head_id'] == trigger_id:
            if word['dependency'] == '主谓关系' and word['postag'][0] == 'n':
                sub = word
            elif word['dependency'] == '动宾关系' and word['postag'][0] == 'n':
                obj = word
    return sub, obj
'''
Algorithm:
    1. find all trigger along with triple 
    2. construct the trigger vocabulary
    3. calculate C(w1,w2) for all pairs of trigger in the vocab
    4. calculate pmi(w1,w2) for all pairs of trigger in the vocab

没有考虑trigger顺序信息。
'''
# triples = []  # 不应该这样，应该使用一个二维list来统计，这样每个list中的triple就是同一篇文章中的triple，也不需要定义一个文档类
doc_triples = []
empty_count = 0
triple_count = 0
# trigger_vocab = set()
trigger_vocab = []
trigger_count_dict = {}


for i, article in enumerate(corsor):
    if len(article['sentences'])==1 and article['sentences'][0]['sentence'] == '':
        # print(i)
        empty_count += 1
        continue

    triples = []
    for j, sent in enumerate(article['sentences']):
        for k, word in enumerate(sent['words']):
            '''
            if word is trigger:
                find sub, obj of trgger
                triggers.append(Trigger())

            # consider the empty article result
            version-1: all articles have the sentence filed in mongo even if is empty.
            '''
            if word['postag'][0] != 'v':
                continue
            # print(word['lemma'])
            sub, obj = find_sub_obj(word, sent['words'])
            if sub==None or obj==None:
                continue
            triple = Triple(i, j, word['lemma'], sub['lemma'], obj['lemma'])
            trigger_count_dict[triple.word] = trigger_count_dict.get(triple.word, 0) + 1
            # triple_count += 1
            print(triple)
            # trigger_vocab.add(word['lemma'])
            trigger_vocab.append(word['lemma'])
            triples.append(triple)
    doc_triples.append(triples)

    # if i > 2 :
    #     break

# output test the result
for i, triples in enumerate(doc_triples):
    print(i, len(triples))
    for j, triple in enumerate(triples):
        print(triple)

# exit(0)


triple_count = sum(trigger_count_dict.values())
print(empty_count)
print(triple_count)

# exit(0)

triggerPair_weight = {}
# trigger_pairs = []
trigger_vocab = list(set(trigger_vocab))

# 1. initial the triggerPair weight to zero
for i, w1 in enumerate(trigger_vocab):
    for j, w2 in enumerate(trigger_vocab[i:]):
        # trigger_pairs.append((w1,w2))
        triggerPair_weight[(w1,w2)] = 0

import pickle
import math
# math.log(x, base)


def calculate_distance_weight(triggerPair_weight, doc_triples):
    '''
    calculate the C(w1,w2) of trigger1 and trigger2
    C(w1, w2): 1-log(g(w1,w2)  # for all trigger pair in same doc of all corpus
        g=1 -> C=1
        g=2 -> C=0.5

    g(w1,w2): represent distance of two triggers in the same doc.
        1: in the same sentence
        2: in neighboring

    :return:  trigger pair weight dict
    '''
    for i, triples in enumerate(doc_triples):
        num = len(triples)
        for i in range(num):
            for j in range(i+1, num):
                g = 1 if triples[i].sent_num == triples[j].sent_num else 2
                trg1 = triples[i].word
                trg2 = triples[j].word

                if (trg1, trg2) in triggerPair_weight.keys():
                    triggerPair_weight[(trg1, trg2)] += 1-math.log(g, 4)
                elif (trg2, trg1) in triggerPair_weight.keys():
                    triggerPair_weight[(trg2, trg1)] += 1-math.log(g, 4)

    return triggerPair_weight

# 2. calc the triggerPair weight
triggerPair_weight = calculate_distance_weight(triggerPair_weight, doc_triples)
# for pair, weight in triggerPair_weight.items():
#     print(pair, weight)
print('-'*20)
# exit(0)



# 计算pmi的时候再进行计算
def trigger_prob(trigger_count_dict):
    all_count = sum(trigger_count_dict.values())
    pass
def triggerPair_prob(triggerPair_weight):
    pass



def pmi(triggerPair_weight, trigger_count_dict):
    '''
    calculate pmi of two triggers
    pmi(w1, w2) = P_dist(w1, w2) / P(w1)P(w2)
        P_dist(w1, w2) =
        P(w1) =
    :return:
    '''
    pmi_of_triggerPair = {}

    trigger_count = sum(trigger_count_dict.values())
    sumOf_pair_weight = sum(triggerPair_weight.values())

    for triggerPair in triggerPair_weight.keys():
        p_dist = triggerPair_weight[triggerPair] / float(sumOf_pair_weight)
        p_t1 = trigger_count_dict[triggerPair[0]] / float(trigger_count)
        p_t2 = trigger_count_dict[triggerPair[1]] / float(trigger_count)

        pmi_of_triggerPair[triggerPair] = p_dist / p_t1*p_t2
        # 1. tuple as the dict key cannot json serialize  2. list unhashable
        # pmi_of_triggerPair[' '.join(triggerPair)] = p_dist / p_t1*p_t2
        # Solved: 在序列化的时候做处理

    return pmi_of_triggerPair


#3. calc triggerPair Weight
triggerPair_pmi = pmi(triggerPair_weight, trigger_count_dict)
for pair, weight in triggerPair_pmi.items():
    print(pair, weight)
    break

print(sorted(list(triggerPair_pmi.values()), reverse=True))

import json
ret = sorted(triggerPair_pmi.items(), key=lambda x:x[1], reverse=True)
with open("pmi.json", 'w') as fw:
    json.dump(ret, fw)

with open('pmi.txt', 'w') as fw:
    fw.write(json.dumps(ret, indent=4, ensure_ascii=False))