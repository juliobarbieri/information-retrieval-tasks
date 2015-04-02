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

def leia(filename, abstract_list):
	logger = setup_logger(util.NAME_ILG_LOGGER, util.IL_GENERATOR_LOG)
	
	if not file_exists(filename):
		logger.error(util.FILE_NOT_FOUND + filename)
		exit_error(util.EXITED_WITH_ERROR)
	
	xml = ElementTree().parse(filename)
	
	qntd_dados = 0

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
		abstract_list[key] = format_text(text)
	
	logger.debug(util.TUPLES_READED_FILE.replace('x', str(qntd_dados)) + filename)
	
def escreva(filename, abstract_list):
	logger = setup_logger(util.NAME_ILG_LOGGER, util.IL_GENERATOR_LOG)
	
	if filename == '':
		logger.error(util.NO_FILE_SPECIFIED)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.GENERATING_INV_LIST)
	
	fw = open(filename, 'w') 
	index = InvertedList(nltk.word_tokenize, EnglishStemmer(), nltk.corpus.stopwords.words('english'))
	
	for key in abstract_list:
		index.add(key, abstract_list[key])
	
	logger.debug(util.WRITING_INVERTED_LIST + filename)
	
	for id in index.index:
		fw.write(index.retrieve(id) + '\n')
	
def format_text(text):
	chars_to_remove = ['.', ',', '!', '?', ';', ':', '(', ')', '\n']
	sc = set(chars_to_remove)
	text = ''.join([c for c in text if c not in sc])

	return text.upper()
	
def parse_command_file():
	logger =  setup_logger(util.NAME_ILG_LOGGER, util.IL_GENERATOR_LOG)
	
	abstract_list = {}
	
	write = False
	fname = util.GENERATOR_FILENAME
	
	if not file_exists(fname):
		logger.error(util.FILE_NOT_FOUND + fname)
		exit_error(util.EXITED_WITH_ERROR)
	
	logger.debug(util.READ_CONFIG_STARTED + fname)
	
	with open(fname) as fp:
		count = 0
		for line in fp:
			next_cmd, filename = get_values(line, count, util.NAME_ILG_LOGGER, util.IL_GENERATOR_LOG)
			
			if write == True:
				logger.error(util.INSTRUCTION_ORDER_ERROR + str(count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			
			if next_cmd == util.CMD_LEIA:
				leia(filename, abstract_list)
			elif next_cmd == util.CMD_ESCREVA:
				write = True
				escreva(filename, abstract_list)
			else:
				logger.error(util.NE_INSTRUCTION_ERROR + str(count + 1))
				exit_error(util.EXITED_WITH_ERROR)
			count = count + 1
			
	logger.debug(util.LINES_READED_CONFIG.replace('x', str(count)))
	logger.debug(util.CONFIG_END_PROCESSING)

parse_command_file()
