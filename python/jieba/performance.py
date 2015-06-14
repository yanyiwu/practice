#encoding=utf-8
import sys
sys.path.append("/Users/yanyiwu/code/jieba/")
import jieba
import random
import datetime

if __name__ == "__main__":
    lines = []
    for line in open("/Users/yanyiwu/code/practice/nodejs/nodejieba/performance/weicheng.utf8"):
        lines.append(line.strip());


    result = [""] * 10;
    result[random.randint(0, 9)] = '/'.join(jieba.cut("南京长江大桥"))
    starttime = datetime.datetime.now()
    print >> sys.stderr, starttime
    for i in xrange(50):
        for line in lines:
            result[random.randint(0, 9)] = '/'.join(jieba.cut(line))
            #result[random.randint(0, 9)] = jieba.cut(line)
    endtime = datetime.datetime.now()
    print endtime
