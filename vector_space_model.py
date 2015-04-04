#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 2015
@author: Julio Barbieri
"""

import numpy as np

class VectorSpaceModel:

	def __init__(self, documents = [], terms = []):
		self.name_rows = documents
		self.name_cols = terms
		
		self.termo_documento = np.zeros((len(documents), len(terms)))
	
	def setup_matrix(self, indexes):
		for j in range(len(self.name_cols)):
			for doc in indexes[self.name_cols[j]]:
				idx = self.name_rows.index(doc)
				self.termo_documento[idx,j] = self.termo_documento[idx,j] + 1
				
	def qntd_documentos(self):
		return len(self.name_rows)
		
	def qntd_termos(self):
		return len(self.name_cols)
		
	def qntd_documentos_dado_termo(self, term):
		index = self.return_index_by_term(term)
		
		if index == -1:
			return None
		else:
			quantidade = 0
			column = self.termo_documento[:,index]
			for qntd_documento in column:
				if qntd_documento > 0:
					quantidade = quantidade + 1
					
			return quantidade
			
	def ocorrencia_total_termo(self, term):
		index = self.return_index_by_term(term)
		
		if index == -1:
			return None
		else:
			quantidade = 0
			column = self.termo_documento[:,index]
			for qntd_documento in column:
				quantidade = qntd_documento + 1
					
			return quantidade
	
	def return_index_by_term(self, term):
		for i in range(len(self.name_cols)):
			if self.name_cols[i] == term:
				return i
		return -1
		
	def return_term_column(self, term):
		index = self.return_index_by_term(term)
		if index == -1:
			return None
		else:
			return self.termo_documento[:,index]
