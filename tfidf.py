#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 5 2015
@author: Julio Barbieri
"""
from math import log

class TfIdf:
	def calculate_weights(self, vector_space_model, word):
		N = vector_space_model.qntd_documentos()
		n = vector_space_model.qntd_documentos_dado_termo(word)
		tf = vector_space_model.return_term_column(word)
		return self.tf_idf(tf, max(tf), N, n)
	
	def tf_idf(self, tf, max_tf, total_documentos, n):
		weights = []
		for i in range(len(tf)):
			tf_idf = self.term_frquency(tf[i], max_tf) * self.idf(total_documentos, n)
			#print(str(tf[i]) + '/' + str(max_tf) + ' * log(' + str(total_documentos) + '/' + str(n) + ')')
			weights.append(tf_idf)
		return weights
	
	def term_frquency(self, tf, max_tf):
		#return tf/max_tf
		#return 0.5 + ((0.5 * tf)/max_tf)
		if tf != 0:
			return 1 + log(tf, 10)
		else:
			return 0
	
	def idf(self, total_documentos, n):
		#return log(total_documentos/n)
		return log(total_documentos/n, 10)
		
