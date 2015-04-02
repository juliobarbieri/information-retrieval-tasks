#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 2015
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

def leia(filename, query_list, query_results):
	logger = setup_logger(util.NAME_QP_LOGGER, util.QUERY_PROCESSOR_LOG)
	
	if not file_exists(filename):
		logger.error(util.FILE_NOT_FOUND + filename)
		exit_error(util.EXITED_WITH_ERROR)
	
	xml = ElementTree().parse(filename)
	
	qntd_dados = 0

	for i, query in enumerate(xml.findall('QUERY')):
		key = 0
		text = ''
		records = ''
		for j, query_number in enumerate(query.findall('QueryNumber')):
			key = query_number.text

		for j, query_text in enumerate(query.findall('QueryText')):
			text = query_text.text
			
		for j, records in enumerate(query.findall('Records')):
			itens = {}
			for k, item in enumerate(records.findall('Item')):
				score = item.get('score')
				document = item.text
				itens[int(document)] = int(score)
		
		qntd_dados = qntd_dados + 1
		query_results[key] = itens
		query_list[key] = format_text(text)
	
	logger.debug(util.TUPLES_READED_FILE.replace('x', str(qntd_dados)) + filename)
	
def consultas(filename, query_list):
	logger = setup_logger(util.NAME_QP_LOGGER, util.QUERY_PROCESSOR_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.WRITING_QUERIES + filename)
	
	fw = open(filename, 'w') 
	
	for key in query_list:
		fw.write(key + ';' + query_list[key] + '\n')
	
def resultados(filename, query_results):
	logger = setup_logger(util.NAME_QP_LOGGER, util.QUERY_PROCESSOR_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.WRITING_EXPECTED_RESULTS + filename)
	
	fw = open(filename, 'w') 
	
	for key in query_results:
		fw.write(key + ';' + str(query_results[key]) + '\n')
	
def format_text(text):
	chars_to_remove = ['.', ',', '!', '?', ';', ':', '(', ')', '\n']
	sc = set(chars_to_remove)
	text = ''.join([c for c in text if c not in sc])

	return text.upper()
	
def parse_command_file():
	logger =  setup_logger(util.NAME_QP_LOGGER, util.QUERY_PROCESSOR_LOG)
	
	query_list = {}
	query_results = {}
	
	query = False
	results = False
	fname = util.QP_FILENAME
	
	if not file_exists(fname):
		logger.error(util.FILE_NOT_FOUND + fname)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READ_CONFIG_STARTED + fname)
	
	with open(fname) as fp:
		count = 0
		for line in fp:
			next_cmd, filename = get_values(line, count, util.NAME_QP_LOGGER, util.QUERY_PROCESSOR_LOG)
			
			if query == False and results == True:
				logger.error(util.INSTRUCTION_ORDER_ERROR + str(count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			
			if next_cmd == util.CMD_LEIA:
				leia(filename, query_list, query_results)
			elif next_cmd == util.CMD_CONSULTAS:
				query = True
				consultas(filename, query_list)
			elif next_cmd == util.CMD_RESULTADOS and query == True:
				results = True
				resultados(filename, query_results)
			else:
				logger.error(util.NE_INSTRUCTION_ERROR + str(count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			count = count + 1
			
	logger.debug(util.LINES_READED_CONFIG.replace('x', str(count)))
	logger.debug(util.CONFIG_END_PROCESSING)

parse_command_file()
