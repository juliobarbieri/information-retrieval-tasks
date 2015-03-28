#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 2015
@author: Julio Barbieri
"""

import logging
import util
from util import file_exists
from util import exit_error
from util import setup_logger
from xml.etree.ElementTree import ElementTree

def leia(filename, abstract_list):
	logger = setup_logger('indexer_logger', util.MODULO_1_LOG)
	
	if not file_exists(filename):
		logger.error(util.FILE_NOT_FOUND + filename)
		exit_error(util.EXITED_WITH_ERROR)
	
	xml = ElementTree().parse(filename)

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
			
		abstract_list[key] = format_text(text)
		
	#print(abstract_list)
def escreva(filename, abstract_list):
	print("Escreva")
	'''TODO'''
	
def format_text(text):
	chars_to_remove = ['.', ',', '!', '?', '\n']
	sc = set(chars_to_remove)
	text = ''.join([c for c in text if c not in sc])

	return text.upper()
	
def get_values(line, count):
	logger =  setup_logger('indexer_logger', util.MODULO_1_LOG)
	
	cmd = line.split(util.GENERATOR_SEPARATOR)
	if len(cmd) < 2 or len(cmd) > 2:
		logger.error(util.FORMAT_ERROR + str(count + 1))
		exit_error(util.EXITED_WITH_ERROR)
		
	next_cmd = cmd[0]
	filename = cmd[1]
	
	if filename.endswith('\n'):
		filename = filename[:-1]
	
	return (next_cmd, filename)
	
def parse_command_file():
	logger =  setup_logger('indexer_logger', util.MODULO_1_LOG)
	
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
			next_cmd, filename = get_values(line, count)
			
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

parse_command_file()