## 
## trigram word frequency
## 
## Copyright 2015 Mostafa Sedaghat Joo
## 
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## 
##     http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## 
##


#!/usr/bin/python
# -*- coding: utf-8 -*-



import os
import glob
import operator
import argparse
from collections import Counter



class WordCounter(object):
    
    def Start(self, dname):
        
        fnames = []
        
        for file in os.listdir(dname):
            if file.endswith(".txt"):
                with open(dname+os.sep+file, 'r', encoding='utf-8') as r:
                    
                    print("normalizing %s" % file)
                    text = self.Normalize( r.read() )
                    
                    dtemp = dname+os.sep+'temp'
                    
                    if not os.path.exists(dtemp):
                        os.makedirs(dtemp)
                        
                    fname = dtemp + os.sep + file
                    
                    fnames.append(fname)
                    
                    with open(fname + '.nrm' , 'w') as w:
                        w.write(text)
        
        for fname in fnames:
            self.Process(fname + '.nrm', 3, fname + '.3grm')
            self.Process(fname + '.nrm', 2, fname + '.2grm')
            self.Process(fname + '.nrm', 1, fname + '.1grm')
        
        print("Dumping result")
        
        freq_1 = Counter()
        freq_2 = Counter()
        freq_3 = Counter()
        
        for fname in fnames:
            freq_3 = freq_3 + self.ReadFreq(fname + '.3grm')
            freq_2 = freq_2 + self.ReadFreq(fname + '.2grm')
            freq_1 = freq_1 + self.ReadFreq(fname + '.1grm')
        
        self.DumpFreq('frquency_1', freq_1)
        self.DumpFreq('frquency_2', freq_2)
        self.DumpFreq('frquency_3', freq_3)
        
        
        for fname in fnames:
            os.remove(fname + '.nrm')
            os.remove(fname + '.3grm')
            os.remove(fname + '.2grm')
            os.remove(fname + '.1grm')
            
    
    
    def Process(self, filename, ngram, result):
        
        print("procesing %s for %d-gram occurannces..." % (os.path.basename(filename) , ngram))
        
        freq = Counter()
        with open(filename, 'r', encoding='utf-8') as r:
            
            words = r.read().split()
            count = len(words) - 2
            index = 0
            while index < count:
                word_1 = words[index]
                word_2 = words[index+1]
                word_3 = words[index+2]
                
                if ngram == 3:
                    token = word_1 + u'\u200c' + word_2 + u'\u200c' + word_3
                elif ngram == 2:
                    token = word_1 + u'\u200c' + word_2
                elif ngram == 1:
                    token = word_1
                    
                if token in freq:
                    freq[token] = freq[token] + 1
                else: 
                    freq[token] = 1
                    
                index = index + 1
        
        
        # remove items with just one occurane
        # reducing dictionary size
        remove = [k for k,v in freq.items() if v < 3]
        for k in remove: del freq[k]
            
        self.DumpFreq(result, freq)
            
    
    def DumpFreq(self, filename, freq):
        with open(filename, 'w', encoding='utf-8') as w:
            freq_s = sorted(freq.items(), key=operator.itemgetter(1))

            for item in reversed(freq_s):
                w.write('%s\t%d\n'% (item[0], item[1]))
                
                
                
    def ReadFreq(self, filename):
        freq = Counter()
        
        with open(filename, 'r', encoding='utf-8') as r:
            for line in r:
                tf = line.split()
                freq[tf[0]] = int(tf[1])
         
        return freq
    
    def Normalize(self, source):
        if source is None:
            return
        
        #replace zwnj
        source = source.replace(u'\u200c', u' ')
        
        #replace arabic ye with persian ye
        source = source.replace(u'\u064a', u'\u06cc')

        #replace arabic k with persian k
        source = source.replace(u'\u0643', u'\u06a9')

        #replace arabic h 
        source = source.replace(u'\u0623', u'\u0627')

        #ignore Irabs
        irabs =  [u'\u064B', u'\u064E', u'\u064F', u'\u0650', u'\u0651', u'\u0652']
        for ch in irabs:
            source = source.replace(ch, '')
        
        
        #replcae punctuations
        puncs = [u'+', u'-', u'_', u':', u'"', u'\'',u'!', u'.', u';', u';', \
                 u'?', u',', u')', u'(', u'؛', u'؛', u'؟', u'،', u'«', u'»', \
                 u'*', u'&', u'[', u']', u'/', u'-', u'o', u'>', u'<', u'_', \
                 u'%', u'&', u'&', u' ', u'@', u'•', u'–', u'\\']
                 
        for ch in puncs:
            source = source.replace(ch, ' ')
        
        
        return source



directory = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="Directory of text files")
args = parser.parse_args()

if args.directory:
    directory = args.directory

wc = WordCounter()
wc.Start(directory)
    
