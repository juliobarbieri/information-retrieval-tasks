#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 3 2015
@author: Julio Barbieri
"""

import re
import numpy as np
import nltk
from vector_space_model import VectorSpaceModel
from xml.etree.ElementTree import ElementTree
from nltk.stem.snowball import EnglishStemmer
from math import log

class Engine:
	
	def __init__(self, vector_space_model):
		self.vector_space_model = vector_space_model
		
	def search(self, query_list):
		query_results = {}
		stopwords = nltk.corpus.stopwords.words('english')
		for key in query_list:
			query = query_list[key]
			words_array = self.pre_process(query)
			relevances = []
			for word in words_array:
				if word in stopwords or word not in self.vector_space_model.name_cols:
					continue
				word_weight = 1
				weight_column = self.vector_space_model.return_term_weights_column(word)
				relevance = [n * word_weight for n in weight_column]
				if len(relevances) == 0:
					relevances = relevance
				else:
					relevances = [x + y for x, y in zip(relevance, relevances)]
					
			relevances_documents = {}
			
			for element_key, element in zip(self.vector_space_model.name_rows, relevances):
				if element > 0:
					relevances_documents[element_key] = element
		
			relevances_documents = sorted(relevances_documents.items(), key=lambda x: x[1], reverse=True)
			query_results[key] = relevances_documents
		
		return query_results
	
	def index(self):
		for word in self.vector_space_model.name_cols:
			weights = self.calculate_weights(word)
			index = self.vector_space_model.return_index_by_term(word)
			for i in range(len(self.vector_space_model.return_term_column(word))):
				self.vector_space_model.matriz_pesos[i][index] = weights[i]
		
		return self.vector_space_model
	
	def pre_process(self, query):
		query = query.replace('/', ' ')
		query = re.sub(' +',' ',query)
		words_array = query.split(' ')
	
		return words_array
	
	def calculate_weights(self, word):
		N = self.vector_space_model.qntd_documentos()
		n = self.vector_space_model.qntd_documentos_dado_termo(word)
		tf = self.vector_space_model.return_term_column(word)
		return self.tf_idf(tf, max(tf), N, n)
	
	def tf_idf(self, tf, max_tf, total_documentos, n):
		weights = []
		for i in range(len(tf)):
			tf_idf = self.term_frquency(tf[i], max_tf) * self.idf(total_documentos, n)
			weights.append(tf_idf)
		return weights
	
	def term_frquency(self, tf, max_tf):
		#return 0.5 + ((0.5 * tf)/max_tf)
		return tf/max_tf
	
	def idf(self, total_documentos, n):
		return log(total_documentos/n)
