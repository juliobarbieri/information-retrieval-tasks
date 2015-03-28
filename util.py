#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 2015
@author: Julio Barbieri
"""

import logging
import sys
import os.path

GENERATOR_SEPARATOR		=	'='
GENERATOR_FILENAME		=	'gli.cfg'

CMD_LEIA				=	'LEIA'
CMD_ESCREVA				=	'ESCREVA'

LINE					=	'linha '
EXITED_WITH_ERROR		=	'Programa encerrado com erros, verificar o log de execução.'
FORMAT_ERROR 			=	'Erro na formatação do arquivo inserido, ' + LINE
NE_INSTRUCTION_ERROR	=	'Instrução não existente, ' + LINE
INSTRUCTION_ORDER_ERROR	=	'Instrução de leia após instrução de escreva, ' + LINE
FILE_NOT_FOUND			=	'Arquivo não encontrado, nome: '

MODULO_1_LOG			=	'lista_invertida.log'
CONFIG_READ_HEADER		=	'Leitura do arquivo de configuração'
READ_CONFIG_STARTED		=	'Iniciando leitura do arquivo de configuração: '
LINES_READED_CONFIG		=	'Lidas x linhas do arquivo de configuração.'

def setup_logger(name, filename):
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)
	
	file_handler = logging.FileHandler(filename)
	file_handler.setLevel(logging.DEBUG)
	
	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.ERROR)
	
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
	console_handler.setFormatter(formatter)
	file_handler.setFormatter(formatter)
	
	logger.addHandler(console_handler)
	logger.addHandler(file_handler)
	
	return logger

def exit_error(message):
	sys.exit(message)
	
def file_exists(filepath):
	return os.path.isfile(filepath)
