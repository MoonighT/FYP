import os
import re
import sys
import ast
from nltk.tag.stanford import POSTagger
from nltk.stem.wordnet import WordNetLemmatizer


address = []
name = []
with open('hgw_crawl.out', 'r') as f:
    for line in f:
        result = ast.literal_eval(line)
        address.append(result.values()[0])
        name.append(result.values()[2])




def conllSeqGenerator(input_file):
    """ return an instance generator for a filename

    The generator yields lists of words and tags.  For test data, the tags
    may be unknown.  For usage, see trainClassifier and applyClassifier below.

    """
    cur_words = []
    cur_tags = []
    with open(input_file) as instances:
        for line in instances:
            if len(line.rstrip()) == 0:
                if len(cur_words) > 0:
                    yield cur_words,cur_tags
                    cur_words = []
                    cur_tags = []
            else:
                parts = line.rstrip().split()
                cur_words.append(parts[0])
                if len(parts)>1:
                    cur_tags.append(parts[1])
                else: cur_tags.append(unk)
        if len(cur_words)>0: yield cur_words,cur_tags

def getSentenceFeature(words, tags):
	"""
	purpose:get features for training from manually labelled data: pos tag, capital, number
	input: 
		words: array of words
		tags : array of tags
	output:
		two d array
		[
			[word(wordnet stem), feature1, feature2, ..., tag]
			[word(wordnet stem), feature1, feature2, ..., tag]
			...
		]
		feature list:
		word blackCase stemword capitalize isdigit score +65 inName inAddress
	"""
	print '...'
	st = POSTagger('stanford-postagger/models/english-bidirectional-distsim.tagger',
				   'stanford-postagger/stanford-postagger.jar')
	lmtzr = WordNetLemmatizer()
	#posTags = st.tag(words)
	features = []
	Black = False
	#for word,pos,tag in zip(words,posTags,tags):
	pos = 0
	for word,tag in zip(words,tags):

		word = word.strip()
		#feature list:
		feature = []
		#word itself
		feature.append(word)

		#black case
		if word == 'bbbbbb':
			Black = True
			continue
		if word == '/bbbbbb':
			Black = False
			continue
		feature.append(Black)
		feature.append(lmtzr.lemmatize(word).encode("utf-8"))
		#stanford pos tag
		#feature.append(pos[1])
		#check if a word is capitalize    used for Restaurant
		feature.append(word[0].isupper())
		#check if a word is all number    used for postal code and price
		feature.append(word.isdigit())
		#check if word is a score
		score = False
		if re.match(r"\d+\.*\d*/\d+", word):
			score = True
		feature.append(score)
        #+65
		phone = False
		if word == '+65':
			phone = True
		feature.append(phone)
		inName = False
		inAddress = False
		if any(word in n for n in name):
			inName = True
		if any(word in a for a in address):
			inAddress = True
		feature.append(inName)
		feature.append(inAddress)
		if word == 'at' or word == 'At':
			feature.append(True)
		else:
			feature.append(False)
		
		feature.append(pos)
		pos += 1
		feature.append(tag)
		features.append(feature)
	return features



def getTrainFile(inputfile='0-9.out',outfile='sgfood_dev_data'):
    """ train a classifier for all instances in a file

    """
    f = open(outfile,'w+')
    for words,tags in conllSeqGenerator(inputfile):
        features = getSentenceFeature(words,tags)
        for feature in features:
	        for val in feature:
	        	f.write(str(val))
	        	f.write(' ')
        	f.write('\n')
    	f.write('\n')
   	
   	
def activeUpdate(target, train_directory='/Users/moonlight/CRF/python/train.data'):
	seq = target.split()
	words = []
	tags = []
	for item in seq:
		word, tag = item.split('\\')[0], item.split('\\')[1] 
		words.append(word)
		tags.append(tag)

	f = open(train_directory,'a')
	features = getSentenceFeature(words, tags)
	f.write('\n')
	for feature in features:
		for val in feature:
			f.write(str(val))
			f.write(' ')
		f.write('\n')
	f.write('\n')

#target = 'Capri\O by\O Fraser\O Changi\I-LOC City\I-LOC Singapore\I-LOC 3\I-LOC Changi\I-LOC Business\I-LOC Park\I-LOC Central\I-LOC 1\I-LOC Singapore\I-LOC 486037\I-LOC Tel\O :\O +65\B-HP 69339833\I-HP Reservation\O :\O +65\O 63380800\O or\O 1800\O 63380800\O Email\O :\O singapore\O @\O capribyfraser.com\O Website\O :\O http\O :\O //singapore.capribyfraser.com/\O '

if __name__ == "__main__":
	getTrainFile()
	#activeUpdate(target)
