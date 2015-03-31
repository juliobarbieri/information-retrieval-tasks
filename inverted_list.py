#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 2015
@author: Julio Barbieri
"""

import nltk
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer
 
class InvertedList:
 
	def __init__(self, tokenizer, stemmer=None, stopwords=None):
		self.tokenizer = tokenizer
		self.stemmer = stemmer
		self.index = defaultdict(list)
		self.id = 0
		if not stopwords:
			self.stopwords = set()
		else:
			self.stopwords = set(stopwords)
 
	def retrieve(self, word):
		word = word.upper()
		
		return word + ';' + str([id for id in self.index.get(word)]).replace(' ', '').replace('\'', '')
 
	def add(self, identifier, document):
		for token in [t.lower() for t in nltk.word_tokenize(document)]:
			if token in self.stopwords:
				continue
 
			if self.stemmer:
				token = self.stemmer.stem(token)
			
			self.id = identifier
 
			if self.id not in self.index[token.upper()]:
				self.index[token.upper()].append(self.id)
