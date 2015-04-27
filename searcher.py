#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 2015
@author: Julio Barbieri
"""

import numpy as np
import nltk
import logging
import time
import re
import util
import sys
import lucene
from util import file_exists
from util import exit_error
from util import setup_logger
from util import get_values
from util import valida_termo
from xml.etree.ElementTree import ElementTree
from nltk.stem.porter import PorterStemmer
from math import log

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

def consultas(filename, struct):
	logger = setup_logger(util.NAME_SEARCHER_LOGGER, util.SEARCHER_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READING_QUERIES % filename)
	
	query_list = {}
	
	with open(filename) as fp:
		count = 0
		for line in fp:
			key, query = trata_query(line)
			query_list[key] = query
			count = count + 1
			
	lucene.initVM()
	analyzer = StandardAnalyzer(Version.LUCENE_4_9)
	reader = IndexReader.open(SimpleFSDirectory(File("index/")))
	searcher = IndexSearcher(reader)
	
	logger.debug(util.LINES_READED_FILE % (count, filename))
	
	start_time = time.time()
	
	query_results = {}
	
	for key in query_list:
		queryParser = QueryParser(Version.LUCENE_4_9, "content", analyzer)
		query = queryParser.parse(queryParser.escape(query_list[key]))
		MAX = 1000
		hits = searcher.search(query, MAX)
	
		rank = []
		i = 1
		for hit in hits.scoreDocs:
			doc = searcher.doc(hit.doc)
			document_key = doc.get("key").encode("utf-8")
			element = [i, int(document_key), hit.score]
			rank.append(element)
			i = i + 1
		query_results[key] = rank
	
	logger.debug(util.QUERIES_TIME % (time.time() - start_time))
	
	return query_results
	
def resultados(filename, query_results):
	logger = setup_logger(util.NAME_SEARCHER_LOGGER, util.SEARCHER_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.WRITING_RESULTS % filename)
	
	fw = open(filename, 'w') 
	
	for key in query_results:
		fw.write(str(key) + ';' + str(query_results[key]) + '\n')
		
	fw.close()
	
def trata_query(line):
	stemmer = PorterStemmer()
	
	line = line[:-1]
	vet_line = line.split(util.CSV_SEPARATOR)
	
	identifier = vet_line[0]
	query = vet_line[1]
	
	query = re.sub(' +',' ',query)
	words_array = nltk.word_tokenize(query)
	
	for word in words_array:
		if valida_termo(word) == None:
			words_array.remove(word)
	
	words_array = [stemmer.stem(word).upper() for word in words_array]
	
	return (identifier, ' '.join(words_array))
	
def parse_command_file():
	logger =  setup_logger(util.NAME_SEARCHER_LOGGER, util.SEARCHER_LOG)
	
	query_results = {}
	
	query = False
	results = False
	config_file = util.SEARCHER_FILENAME
	
	struct = None
	
	if not file_exists(config_file):
		logger.error(util.FILE_NOT_FOUND % config_file)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READ_CONFIG_STARTED % config_file)
	
	with open(config_file) as fp:
		count = 0
		for line in fp:
			
			next_cmd, filename = get_values(line, count, util.CONFIG_SEPARATOR, util.NAME_SEARCHER_LOGGER, util.SEARCHER_LOG)
			
			if next_cmd == util.CMD_CONSULTAS and results == False:
				query = True
				query_results = consultas(filename, struct)
			elif next_cmd == util.CMD_RESULTADOS and query == True and results == False:
				results = True
				resultados(filename, query_results)
			else:
				logger.error(util.NE_IO_INSTRUCTION_ERROR % (count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			count = count + 1
			
	logger.debug(util.LINES_READED_CONFIG % count)
	logger.debug(util.CONFIG_END_PROCESSING % config_file)

if __name__ == "__main__":
	parse_command_file()
