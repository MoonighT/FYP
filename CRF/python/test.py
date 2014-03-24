#!/usr/bin/ruby

import CRFPP
import sys

TEST_FILE = "test.data"

try:
    # -v 3: access deep information like alpha,beta,prob
    # -nN: enable nbest output. N should be >= 2
    tagger = CRFPP.Tagger("-m ../example/sgfood/model -n2")

    # read test data 

    with open(TEST_FILE) as f:
        for line in f:
            print line

    # clear internal context
    tagger.clear()

    # add context
    tagger.add("Eatzi True NNP False")
    tagger.add("Gourmet True NNP False") 
    tagger.add("Bakery True NNP False")
    tagger.add("by False IN False")
    tagger.add("JP True NNP False")
    tagger.add("Pepperdine True NNP False")
    tagger.add(", False , False")
    tagger.add("the False DT False")
    tagger.add("same False JJ False")
    tagger.add("folk False NNS False")
    tagger.add("that False WDT False")
    tagger.add("bring False VBP False")
    tagger.add("you False PRP False")
    tagger.add("Jacks True NNP False")
    tagger.add("Place True NNP False")
    tagger.add("ha False VBZ False")
    tagger.add("specially False RB False")
    tagger.add("created False VBN False")
    tagger.add("a False DT False")
    tagger.add("selection False NN False")
    tagger.add("of False IN False")
    tagger.add("baked False JJ False")
    tagger.add("and False CC False")
    tagger.add("snowskin False JJ False")
    tagger.add("mooncakes False NNS False")
    tagger.add("for False IN False")
    tagger.add("the False DT False")
    tagger.add("Mid-Autumn True NNP False")
    tagger.add("Festival True NNP False")
    tagger.add(". False . False O")


    print "column size: " , tagger.xsize()
    print "token size: " , tagger.size()
    print "tag size: " , tagger.ysize()

    print "tagset information:"
    ysize = tagger.ysize()
    for i in range(0, ysize-1):
        print "tag " , i , " " , tagger.yname(i)

    # parse and change internal stated as 'parsed'
    tagger.parse()

    print "conditional prob=" , tagger.prob(), " log(Z)=" , tagger.Z()

    size = tagger.size()
    xsize = tagger.xsize()
    for i in range(0, (size - 1)):
       for j in range(0, xsize):  #source code got problem:  xsize-1 => xsize
          print tagger.x(i, j) , "\t",
       print tagger.y2(i) , "\t",
       print "Details",
       for j in range(0, (ysize-1)):
          print "\t" , tagger.yname(j) , "/prob=" , tagger.prob(i,j),
       print "\n",

    # print "nbest outputs:"
    # for n in range(0, 9):
    #     if (not tagger.next()):
    #         continue
    #     print "nbest n=" , n , "\tconditional prob=" , tagger.prob()
    #     # you can access any information using tagger.y()...

    print "Done"

except RuntimeError, e:
    print "RuntimeError: ", e,
