import CRFPP
import copy
import sys
import math
from collections import defaultdict

TAGS = ['B-ORG', 'I-ORG', 'B-F', 'I-F', 'B-LOC', 'I-LOC','B-HP','I-HP','S','O']
stat = defaultdict(int) 

class Feature:
    def __init__(self, feature):
        list = feature.split(' ')
        self.attr = list[:-1]
        self.tag = list[-1]

class Word:
    def __init__(self, type):
        self.type = type
        self.words = []
    def toStr(self):
        return " ".join(self.words)

def cal_evaluation(stat):
    #Evaluation matrix
    for i in TAGS:
        #Recall
        #Precision
        recall = 0.0
        precision = 0.0
        f_score = 0.0
        tp = 0
        p = 0
        f = 0
        for k,v in stat.items():
            if k[0] == i:
                p += v
            if k[1] == i:
                f += v
            if k[0] == i and k[1] == i:
                tp += v
        recall = tp*1.0/p if p > 0 else 0.0
        print "%0s %20s %.3f" %(i, "recall = " ,recall), 
        
        precision = tp*1.0/f if f > 0 else 0.0
        print " precision= %.3f" %precision,
        
        f_score = 2 * precision * recall / ( precision + recall) if (recall + precision) > 0 else 0.0
        print " f_score= %.3f" %f_score


def runDemo(demofile):
    blog = []
    sent = []
    with open(demofile) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                blog.append(sent)
                sent = []
            else:
                x = Feature(line)
                sent.append(x)
    x_list = []
    y_list = []
    tag_list = []
    myDict = defaultdict(list)
    for sent in blog:
        tagger = CRFPP.Tagger("-m model")
        for word in sent:
            tagger.add(" ".join(word.attr))

        tagger.parse()

        size = tagger.size()
        xsize = tagger.xsize()
        
        for i in range(0, (size - 1)):
            x_list.append(tagger.x(i,0))
            y_list.append(tagger.y2(i))
            tag_list.append(sent[i].tag)

    for x,y in zip(x_list,y_list):
        if y.startswith("B-"):
            word = Word(y)
            word.words.append(x)
            myDict[y].append(word)
        elif y.startswith("I-"):
            y = "B" + y[1:]
            myDict[y][-1].words.append(x)

    for k,v in myDict.items():
        print k
        print "============"
        for i in v:
            print i.toStr()

def runActiveLearning(test_file, testing=True):
    stat.clear()
    try:
        tagger = CRFPP.Tagger("-m model -n5")
        #read test data
        
        least_con = 10000000.0
        least_tag = {}

        min_margin = 10000000.0
        min_margin_tag = {}

        max_entropy = 0
        max_entropy_tag = {}

        blog = []
        sent = []
        with open(test_file) as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    blog.append(sent)
                    sent = []
                else:
                    x = Feature(line)
                    sent.append(x)
               
        for sent in blog:
            tagger = CRFPP.Tagger("-m model -n5")
            for word in sent:
                tagger.add(" ".join(word.attr))
        
            # print "column size: " , tagger.xsize()
            # print "taken size: ", tagger.size()
            # print "tag size: ", tagger.ysize()
            
            tagger.parse()
            # #print "conditional prob=" , tagger.prob()," log(Z)=" , tagger.Z()
            if not testing:
                #development
                #least confidence ===============method=========================
                # if len(sent):
                #    if tagger.prob() < least_con:
                #         #least_con = tagger.prob() * len(sent)
                #         least_con = tagger.prob()
                #         least_tag = tagger
                #===============================================================
                #max margin======================method=========================
                # if len(sent):
                #     for n in range(0, 2):
                #         if (not tagger.next()):
                #             continue
                #         if n == 0:
                #             p1 = tagger.prob()
                #         if n == 1:
                #             p2 = tagger.prob()
                #         #print "nbest n=" , n , "\tconditional prob=" , tagger.prob()
                #     if p1 - p2 < min_margin:
                #         min_margin = p1 - p2
                #         min_margin_tag = tagger
                #===============================================================
                #n best max entropy
                if len(sent):
                    #n best
                    entropy = 0.0
                    for n in range(0, 5):
                        if (not tagger.next()):
                            continue
                        #print "nbest n=" , n , "\tconditional prob=" , tagger.prob()
                        #normalized version
                        entropy += tagger.prob() *len(sent) * math.log(tagger.prob()*len(sent))
                        #entropy += tagger.prob() * math.log(tagger.prob())                   
                    entropy = -entropy
                    #print entropy
                    if entropy > max_entropy:
                        max_entropy = entropy
                        max_entropy_tag = tagger
            else:
                for i, word in enumerate(sent):
                    stat[(word.tag,tagger.y2(i))] += 1
            
            size = tagger.size()
            xsize = tagger.xsize()
            for i in range(0, (size - 1)):
                for j in range(0, xsize):  #source code got problem:  xsize-1 => xsize
                    print tagger.x(i, j) , "\t",
                print tagger.y2(i), "\t",
                print sent[i].tag
            print
        
        if testing:
            cal_evaluation(stat)
        else:
            #least confidence
            #selected = least_tag
            #max margin
            #selected = min_margin_tag
            #max entropy
            #print max_entropy
            selected = max_entropy_tag
            result = {}
            result['content'] = []
            
            for x_index in xrange(selected.size()):
                result['content'].append((selected.x(x_index,0),selected.y2(x_index)))
            result['prob'] = selected.prob()
            #print result
            return result
    except RuntimeError, e:
        print "Run time Error: ", e,

if __name__ == '__main__':
    runDemo('sgfood_test_data')