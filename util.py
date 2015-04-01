#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 2015
@author: Julio Barbieri
"""

import logging
import sys
import os.path

SEPARATOR				=	'='
INVERTED_LIST_SEPARATOR	=	';'
GENERATOR_FILENAME		=	'gli.cfg'
INDEXER_FILENAME		=	'index.cfg'

CMD_LEIA				=	'LEIA'
CMD_ESCREVA				=	'ESCREVA'

LINE					=	'linha '
EXITED_WITH_ERROR		=	'Programa encerrado com erros, verificar o log de execução.'
FORMAT_ERROR 			=	'Erro na formatação do arquivo inserido, ' + LINE
NE_INSTRUCTION_ERROR	=	'Instrução não existente, ' + LINE
INSTRUCTION_ORDER_ERROR	=	'Instrução de leia após instrução de escreva, ' + LINE
NE_IO_INSTRUCTION_ERROR	=	'Instrução não existente ou ordem de leia e escreva invertidas, ' + LINE
FILE_NOT_FOUND			=	'Arquivo não encontrado, nome: '

NAME_ILG_LOGGER			=	'inverted_list_generator_logger'
NAME_INDEXER_LOGGER		=	'indexer_logger'

IL_GENERATOR_LOG		=	'inverted_list_generator.log'
INDEXER_LOG				=	'indexer.log'
CONFIG_READ_HEADER		=	'Leitura do arquivo de configuração para geração da lista invertida'
READ_CONFIG_STARTED		=	'Iniciando leitura do arquivo de configuração: '
TUPLES_READED_FILE		=	'Lidas x tuplas do arquivo: '
LINES_READED_USED_FILE	=	'Lidas x linhas (y aproveitadas) do arquivo: '
GENERATING_INV_LIST		=	'Gerando a lista invertida com base nos dados lidos.'
WRITING_INVERTED_LIST	=	'Escrevendo a lista invertida gerada em: '
CONFIG_END_PROCESSING	=	'Finzalizando a etapa de geração de uma lista invertida'
LINES_READED_CONFIG		=	'Lidas x linhas do arquivo de configuração.'
NO_FILE_SPECIFIED		=	'Arquivo não especificado para geração da lista invertida.'
SAVING_STRUCTURE		=	'Salvando estrutura do modelo vetorial no arquivo: '

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
	
def get_values(line, count, log_name, log_file):
	logger =  setup_logger(log_name, log_file)
	
	cmd = line.split(SEPARATOR)
	if len(cmd) < 2 or len(cmd) > 2:
		logger.error(FORMAT_ERROR + str(count + 1))
		exit_error(EXITED_WITH_ERROR)
		
	next_cmd = cmd[0]
	filename = cmd[1]
	
	if filename.endswith('\n'):
		filename = filename[:-1]
	
	return (next_cmd, filename)

def exit_error(message):
	sys.exit(message)
	
def file_exists(filepath):
	return os.path.isfile(filepath)
