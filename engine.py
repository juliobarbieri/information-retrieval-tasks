#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 3 2015
@author: Julio Barbieri
"""

import re
import numpy as np
import nltk
from vector_space_model import VectorSpaceModel
from xml.etree.ElementTree import ElementTree

class Engine:
	
	def __init__(self, metric, vector_space_model):
		self.vector_space_model = vector_space_model
		self.metric = metric
		
	def search(self, query_list):
		query_results = {}
		stopwords = nltk.corpus.stopwords.words('english')
		for key in query_list:
			words_array = query_list[key]
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
					relevances = [1/(x + y) for x, y in zip(relevance, relevances)]
					
			relevances_documents = []
			
			for element_key, element in zip(self.vector_space_model.name_rows, relevances):
				if element < 1 and element != 0:
					relevances_documents.append([element_key, element])
		
			relevances_documents = sorted(relevances_documents, key=lambda x: x[1])
			relevances_documents = [[x + 1] + relevances_documents[x] for x in range(len(relevances_documents))]
			query_results[key] = relevances_documents
		
		return query_results
	
	def index(self):
		for word in self.vector_space_model.name_cols:
			weights = self.metric.calculate_weights(self.vector_space_model, word)
			index = self.vector_space_model.return_index_by_term(word)
			for i in range(self.vector_space_model.qntd_documentos()):
				self.vector_space_model.matriz_pesos[i][index] = weights[i]
		
		return self.vector_space_model
