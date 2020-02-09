import jieba.analyse as analyse
import jieba
import time

start = time.time()
stm = ''
with open('data.txt','r', encoding='utf-8') as f:
    stm += f.read()

analyse.set_stop_words('./stops.txt')
tags = analyse.extract_tags(stm, topK=1000)
print(tags)
end = time.time()
print("cost: {}s".format(end-start))

with open("res-2.txt",'w', encoding='utf-8') as f:
    rtm = '\n'.join(tags)
    f.write(rtm)