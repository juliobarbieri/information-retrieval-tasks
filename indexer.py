#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 2015
@author: Julio Barbieri
"""

import nltk
import logging
import util
import time
import sys
import lucene
from util import file_exists
from util import exit_error
from util import setup_logger
from util import get_values
from util import format_text
from xml.etree.ElementTree import ElementTree
from nltk.stem.porter import PorterStemmer

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

def leia(filename, abstract_list):
	logger =  setup_logger(util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
	
	if not file_exists(filename):
		logger.error(util.FILE_NOT_FOUND % filename)
		exit_error(util.EXITED_WITH_ERROR)
	
	xml = ElementTree().parse(filename)
	
	qntd_dados = 0
	
	start_time = time.time()
	
	for i, record in enumerate(xml.findall('RECORD')):
		key = 0
		text = ''
		for j, recordnum in enumerate(record.findall('RECORDNUM')):
			key = recordnum.text

		for j, abstract in enumerate(record.findall('ABSTRACT')):
			text = abstract.text
		
		if text == '':
			for j, extract in enumerate(record.findall('EXTRACT')):
				text = extract.text
			
		qntd_dados = qntd_dados + 1
		abstract_list[key] = util.format_text(text)
	
	logger.debug(util.DOCUMENTS_TIME % (time.time() - start_time))
	
	logger.debug(util.TUPLES_READED_FILE % (qntd_dados, filename))
	
def index(abstract_list):
	logger =  setup_logger(util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
	
	lucene.initVM()
	indexDir = SimpleFSDirectory(File("index/"))
	writerConfig = IndexWriterConfig(Version.LUCENE_4_9, StandardAnalyzer(Version.LUCENE_4_9))
	writer = IndexWriter(indexDir, writerConfig)
	
	for key in abstract_list:
		stemmer = PorterStemmer()
		stopwords = set(nltk.corpus.stopwords.words('english'))
		words = nltk.word_tokenize(abstract_list[key])
		words = [stemmer.stem(word).upper() for word in words if word not in stopwords]
		prepared_document = ' '.join(words)
		
		doc = Document()
		
		doc.add(Field("key", key, Field.Store.YES, Field.Index.ANALYZED))
		doc.add(Field("content", prepared_document, Field.Store.YES, Field.Index.ANALYZED))
		
		writer.addDocument(doc)
		
	#for n, l in enumerate(sys.stdin):
	#	doc = Document()
	#	doc.add(Field("text", l, Field.Store.YES, Field.Index.ANALYZED))
	#	writer.addDocument(doc)
	#print "Indexed %d lines from stdin (%d docs in index)" % (n, writer.numDocs())
	#print "Closing index of %d docs..." % writer.numDocs()
	writer.close()
	
def parse_command_file():
	logger =  setup_logger(util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
	
	abstract_list = {}
	
	config_file = util.INDEXER_FILENAME
	
	if not file_exists(config_file):
		logger.error(util.FILE_NOT_FOUND % config_file)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READ_CONFIG_STARTED % config_file)
	
	with open(config_file) as fp:
		count = 0
		for line in fp:
			next_cmd, filename = get_values(line, count, util.CONFIG_SEPARATOR, util.NAME_IIG_LOGGER, util.II_GENERATOR_LOG)
			
			if next_cmd == util.CMD_LEIA:
				leia(filename, abstract_list)
			else:
				logger.error(util.NE_IO_INSTRUCTION_ERROR % (count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			count = count + 1
			
	logger.debug(util.LINES_READED_CONFIG % count)
	logger.debug(util.CONFIG_END_PROCESSING % config_file)
	
	index(abstract_list)

if __name__ == "__main__":
	parse_command_file()
