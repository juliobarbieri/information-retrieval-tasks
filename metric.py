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

class Metric:
	
	def __init__(self, vector_space_model):
		self.vector_space_model = vector_space_model
		
	
	def prepare_data(self, query_list):
		query_results = {}
		stopwords = nltk.corpus.stopwords.words('english')
		for key in query_list:
			query = query_list[key]
			words_array = self.pre_process(query)
			relevances = []
			for word in words_array:
				if word in stopwords: #or word not in self.vector_space_model.name_cols:
					continue
				relevance = self.calc_relevance(word)
				if len(relevances) == 0:
					relevances = relevance
				else:
					for i in range(len(relevance)):
						relevances[i] = relevances[i] + relevance[i]
					
			relevances_documents = {}
		
			for element_key, element in zip(self.vector_space_model.name_rows, relevances):
				if element > 0:
					relevances_documents[element_key] = element
		
			relevances_documents = sorted(relevances_documents.items(), key=lambda x: x[1], reverse=True)
			query_results[key] = relevances_documents
		
		return query_results
		
	def pre_process(self, query):
		query = query.replace('/', ' ')
		query = re.sub(' +',' ',query)
		words_array = query.split(' ')
	
		return words_array
	
	def calc_relevance(self, word):
		stemmer = EnglishStemmer()
		word = stemmer.stem(word).upper()
		N = self.vector_space_model.qntd_documentos()
		n = self.vector_space_model.qntd_documentos_dado_termo(word)
		total_oc_termo = self.vector_space_model.ocorrencia_total_termo(word)
	
		if n != None and total_oc_termo != None:
			tf = self.vector_space_model.return_term_column(word) 
			return self.tf_idf(tf, max(tf), N, n)
		else:
			return np.zeros(N)
	
	def tf_idf(self, tf, max_tf, total_documentos, n):
		tf_idfs = []
		for i in range(len(tf)):
			tf_idf = self.term_frquency(tf[i], max_tf) * self.idf(total_documentos, n)
			tf_idfs.append(tf_idf)
		return tf_idfs
	
	def term_frquency(self, tf, max_tf):
		#return 0.5 + ((0.5 * tf)/max_tf)
		return tf/max_tf
	
	def idf(self, total_documentos, n):
		return log(total_documentos/n)
