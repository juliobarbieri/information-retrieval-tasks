#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 4 2015
@author: Julio Barbieri
"""

import inverted_index_generator
import indexer
import query_processor
import searcher
import evaluation

if __name__ == "__main__":
	inverted_index_generator.parse_command_file()
	indexer.parse_command_file()
	query_processor.parse_command_file()
	searcher.parse_command_file()
	#evaluation.parse_command_file()
