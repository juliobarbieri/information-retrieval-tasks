#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 4 2015
@author: Julio Barbieri
"""

import indexer
import query_processor
import searcher
import evaluator

if __name__ == "__main__":
	indexer.parse_command_file()
	query_processor.parse_command_file()
	searcher.parse_command_file()
	#evaluator.parse_command_file()
