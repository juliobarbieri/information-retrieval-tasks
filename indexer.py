#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 2015
@author: Julio Barbieri
"""

import nltk
import logging
import util
from util import file_exists
from util import exit_error
from util import setup_logger
from util import get_values
from inverted_list import InvertedList
from xml.etree.ElementTree import ElementTree
from nltk.stem.snowball import EnglishStemmer

def leia(filename, abstract_list):
	logger =  setup_logger(util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
	
	if not file_exists(filename):
		logger.error(util.FILE_NOT_FOUND + filename)
		exit_error(util.EXITED_WITH_ERROR)
	
	indexes = {}
	
	with open(filename) as fp:
		count = 0
		for line in fp:
			termo, documentos = trata_lista(line)
			indexes[termo] = documentos
	
	unique_ids = []
	
	for i in indexes:
		unique_ids.extend(indexes[i])
	
	# Teste
	print(set(unique_ids))
	
def escreva(filename, abstract_list):
	logger =  setup_logger(util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
	print('Escreva')
	
def trata_lista(line):
	line = line[:-1]
	vet_line = line.split(';')
	
	termo = vet_line[0]
	documentos = vet_line[1]
	
	documentos = documentos[:-1]
	documentos = documentos[1:]
	
	vet_docs = documentos.split(',')
	vet_docs = list(map(int, vet_docs)) #[int(i) for i in vet_docs]
	
	return (termo, vet_docs)
	
def parse_command_file():
	logger =  setup_logger(util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
	
	abstract_list = {}
	
	fname = util.INDEXER_FILENAME
	
	if not file_exists(fname):
		logger.error(util.FILE_NOT_FOUND + fname)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READ_CONFIG_STARTED + fname)
	
	with open(fname) as fp:
		count = 0
		for line in fp:
			next_cmd, filename = get_values(line, count, util.NAME_INDEXER_LOGGER, util.INDEXER_LOG)
			
			if next_cmd == util.CMD_LEIA and count == 0:
				leia(filename, abstract_list)
			elif next_cmd == util.CMD_ESCREVA and count == 1:
				escreva(filename, abstract_list)
			else:
				logger.error(util.NE_IO_INSTRUCTION_ERROR + str(count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			count = count + 1
			
	logger.debug(util.LINES_READED_CONFIG.replace('x', str(count)))
	logger.debug(util.CONFIG_END_PROCESSING)

parse_command_file()
