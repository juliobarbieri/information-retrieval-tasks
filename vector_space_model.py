#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 2015
@author: Julio Barbieri
"""

import numpy as np

class VectorSpaceModel:

	def __init__(self, documents, terms):
		self.name_rows = documents
		self.name_cols = terms
		
		self.termo_documento = np.zeros((len(documents), len(terms)))
	
	def setup_matrix(self, indexes):
		for j in range(len(self.name_cols)):
			for doc in indexes[self.name_cols[j]]:
				idx = self.name_rows.index(doc)
				self.termo_documento[idx,j] = self.termo_documento[idx,j] + 1
