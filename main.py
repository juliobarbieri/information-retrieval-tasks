#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 4 2015
@author: Julio Barbieri
"""

import inverted_list_generator
import indexer
import query_processor
import search_engine

if __name__ == "__main__":
	inverted_list_generator.parse_command_file()
	indexer.parse_command_file()
	query_processor.parse_command_file()
	search_engine.parse_command_file()
