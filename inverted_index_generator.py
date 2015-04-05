#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 2015
@author: Julio Barbieri
"""

import nltk
import logging
import util
import time
from util import file_exists
from util import exit_error
from util import setup_logger
from util import get_values
from util import format_text
from inverted_index import InvertedIndex
from xml.etree.ElementTree import ElementTree
from nltk.stem.snowball import EnglishStemmer

def leia(filename, abstract_list):
	logger = setup_logger(util.NAME_IIG_LOGGER, util.II_GENERATOR_LOG)
	
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
	
def escreva(filename, abstract_list):
	logger = setup_logger(util.NAME_IIG_LOGGER, util.II_GENERATOR_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.GENERATING_INV_LIST)
	
	fw = open(filename, 'w') 
	index = InvertedIndex(nltk.word_tokenize, EnglishStemmer(), nltk.corpus.stopwords.words('english'))
	
	for key in abstract_list:
		index.add(key, abstract_list[key])
	
	logger.debug(util.WRITING_INVERTED_INDEX % filename)
	
	for id in index.index:
		fw.write(index.retrieve(id) + '\n')
	
	fw.close()
	
def parse_command_file():
	logger =  setup_logger(util.NAME_IIG_LOGGER, util.II_GENERATOR_LOG)
	
	abstract_list = {}
	
	read = False
	write = False
	config_file = util.GENERATOR_FILENAME
	
	if not file_exists(config_file):
		logger.error(util.FILE_NOT_FOUND % config_file)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READ_CONFIG_STARTED % config_file)
	
	with open(config_file) as fp:
		count = 0
		for line in fp:
			next_cmd, filename = get_values(line, count, util.CONFIG_SEPARATOR, util.NAME_IIG_LOGGER, util.II_GENERATOR_LOG)
			
			if write == True:
				logger.error(util.INSTRUCTION_ORDER_ERROR % (count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			
			if next_cmd == util.CMD_LEIA:
				read = True
				leia(filename, abstract_list)
			elif next_cmd == util.CMD_ESCREVA and read == True:
				write = True
				escreva(filename, abstract_list)
			else:
				logger.error(util.NE_IO_INSTRUCTION_ERROR % (count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			count = count + 1
			
	logger.debug(util.LINES_READED_CONFIG % count)
	logger.debug(util.CONFIG_END_PROCESSING % config_file)

if __name__ == "__main__":
	parse_command_file()