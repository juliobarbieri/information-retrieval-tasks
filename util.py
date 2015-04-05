#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 2015
@author: Julio Barbieri
"""

import logging
import sys
import os.path

loggers = {}

CONFIG_SEPARATOR		=	'='
CSV_SEPARATOR			=	';'
GENERATOR_FILENAME		=	'gli.cfg'
INDEXER_FILENAME		=	'index.cfg'
QP_FILENAME				=	'pc.cfg'
SEARCH_ENGINE_FILENAME	=	'busca.cfg'

CMD_LEIA				=	'LEIA'
CMD_ESCREVA				=	'ESCREVA'
CMD_CONSULTAS			=	'CONSULTAS'
CMD_RESULTADOS			=	'RESULTADOS'
CMD_MODELO				=	'MODELO'

LINE					=	'linha '
EXITED_WITH_ERROR		=	'Programa encerrado com erros, verificar o log de execução.'
FORMAT_ERROR 			=	'Erro na formatação do arquivo inserido, ' + LINE
NE_INSTRUCTION_ERROR	=	'Instrução não existente, ' + LINE
INSTRUCTION_ORDER_ERROR	=	'Instrução de leia após instrução de escreva, ' + LINE + '%d.'
NE_IO_INSTRUCTION_ERROR	=	'Instrução não existente ou ordem de leia e escreva invertidas, ' + LINE + '%d.'
FILE_NOT_FOUND			=	'Arquivo não encontrado, nome: %s.'

NAME_ILG_LOGGER			=	'inverted_list_generator_logger'
NAME_INDEXER_LOGGER		=	'indexer_logger'
NAME_QP_LOGGER			=	'query_processor_logger'
NAME_SE_LOGGER			=	'search_engine_logger'

IL_GENERATOR_LOG		=	'inverted_list_generator.log'
INDEXER_LOG				=	'indexer.log'
QUERY_PROCESSOR_LOG		=	'query_processor.log'
SEARCH_ENGINE_LOG		=	'search_engine.log'

CONFIG_READ_HEADER		=	'Leitura do arquivo de configuração para geração da lista invertida'
READ_CONFIG_STARTED		=	'Iniciando leitura do arquivo de configuração: %s.'
TUPLES_READED_FILE		=	'Lidas %d tuplas do arquivo: %s.'
LINES_READED_USED_FILE	=	'Lidas %d linhas (%d aproveitadas) do arquivo: %s.'
LINES_READED_FILE		=	'Lidas %d linhas do arquivo: %s.'
GENERATING_INV_LIST		=	'Gerando a lista invertida com base nos dados lidos.'
WRITING_INVERTED_LIST	=	'Escrevendo a lista invertida gerada em: %s.'
CONFIG_END_PROCESSING	=	'Finzalizando a leitura do arquivo de configuração: %s.'
LINES_READED_CONFIG		=	'Lidas %d linhas do arquivo de configuração.'
NO_FILE_SPECIFIED		=	'Arquivo não especificado para geração da lista invertida.'
SAVING_STRUCTURE		=	'Salvando estrutura do modelo vetorial no arquivo: %s.'
STRUCTURE_LOADED		=	'Estrutura carregada à partir do arquivo: %s.'
WRITING_QUERIES			=	'Escrevendo as consultas no arquivo: %s.'
WRITING_EXPECTED_RESULTS=	'Escrevendo os resultados esperados das consultas no arquivo: %s.'
WRITING_RESULTS			=	'Escrevendo os resultados das consultas no arquivo: %s.'
READING_QUERIES			=	'Leando as consultas no arquivo: %s.'
QUERIES_TIME			=	'As consultas requeridas foram processadas e realizadas em %s segundos'
DOCUMENTS_TIME			=	'Os documentos requeridos foram lidos e processados em %s segundos'
WORDS_TIME				=	'As palavras requeridas foram lidas e processadas em %s segundos'

def setup_logger(name, filename):
	global loggers

	if loggers.get(name):
		return loggers.get(name)
	else:
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
		
		loggers.update(dict(name=logger))
	
		return logger
	
def get_values(line, count, separator, log_name, log_file):
	logger =  setup_logger(log_name, log_file)
	
	cmd = line.split(separator)
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
