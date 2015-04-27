#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 2015
@author: Julio Barbieri
"""

import logging
import sys
import re
import os.path

from nltk.stem.porter import PorterStemmer

CONFIG_SEPARATOR		=	'='
CSV_SEPARATOR			=	';'
INDEXER_FILENAME		=	'config/index.cfg'
QP_FILENAME				=	'config/pc.cfg'
SEARCHER_FILENAME		=	'config/busca.cfg'

EVALUATION_FILENAME		=	'config/avaliacao.cfg'

PATH 					=	'files/'

CMD_LEIA				=	'LEIA'
CMD_ESCREVA				=	'ESCREVA'
CMD_CONSULTAS			=	'CONSULTAS'
CMD_RESULTADOS			=	'RESULTADOS'
CMD_MODELO				=	'MODELO'

STEMMER					=	'STEMMER'
NOSTEMMER				=	'NOSTEMMER'

LINE					=	'linha '
EXITED_WITH_ERROR		=	'Programa encerrado com erros, verificar o log de execução.'
FORMAT_ERROR 			=	'Erro na formatação do arquivo inserido, ' + LINE
NE_INSTRUCTION_ERROR	=	'Instrução não existente, ' + LINE
INSTRUCTION_ORDER_ERROR	=	'Instrução de leia após instrução de escreva, ' + LINE + '%d.'
NE_IO_INSTRUCTION_ERROR	=	'Instrução não existente ou ordem de leia e escreva invertidas, ' + LINE + '%d.'
FILE_NOT_FOUND			=	'Arquivo não encontrado, nome: %s.'

NAME_IIG_LOGGER			=	'inverted_index_generator_logger'
NAME_INDEXER_LOGGER		=	'indexer_logger'
NAME_QP_LOGGER			=	'query_processor_logger'
NAME_SEARCHER_LOGGER	=	'searcher_logger'
NAME_EVALUATION_LOGGER	=	'evalutation_looger'

II_GENERATOR_LOG		=	'logs/inverted_index_generator.log'
INDEXER_LOG				=	'logs/indexer.log'
QUERY_PROCESSOR_LOG		=	'logs/query_processor.log'
SEARCHER_LOG			=	'logs/searcher.log'
EVALUATION_LOG			=	'logs/evaluation.log'

CONFIG_READ_HEADER		=	'Leitura do arquivo de configuração para geração da lista invertida'
READ_CONFIG_STARTED		=	'Iniciando leitura do arquivo de configuração: %s.'
TUPLES_READED_FILE		=	'Lidas %d tuplas do arquivo: %s.'
LINES_READED_USED_FILE	=	'Lidas %d linhas (%d aproveitadas) do arquivo: %s.'
LINES_READED_FILE		=	'Lidas %d linhas do arquivo: %s.'
GENERATING_INV_LIST		=	'Gerando a lista invertida com base nos dados lidos.'
WRITING_INVERTED_INDEX	=	'Escrevendo a lista invertida gerada em: %s.'
CONFIG_END_PROCESSING	=	'Finzalizando a leitura do arquivo de configuração: %s.'
LINES_READED_CONFIG		=	'Lidas %d linhas do arquivo de configuração.'
NO_FILE_SPECIFIED		=	'Arquivo não especificado para geração da lista invertida.'
SAVING_STRUCTURE		=	'Salvando estrutura do modelo vetorial no arquivo: %s.'
STRUCTURE_LOADED		=	'Estrutura carregada à partir do arquivo: %s.'
WRITING_QUERIES			=	'Escrevendo as consultas no arquivo: %s.'
WRITING_METRIC			=	'Escrevendo a métrica no arquivo: %s.'
PLOTTING_METRIC			=	'Plotando a métrica em um gráfico: %s.'
WRITING_EXPECTED_RESULTS=	'Escrevendo os resultados esperados das consultas no arquivo: %s.'
WRITING_RESULTS			=	'Escrevendo os resultados das consultas no arquivo: %s.'
READING_QUERIES			=	'Lendo as consultas no arquivo: %s.'
STEMMER_ENABLED			=	'Uso de stemmer ativado.'
STEMMER_DISABLED		=	'Uso de stemmer desativado.'
CALC_METRIC				=	'Calculando métricas.'
SAVING_METRIC			=	'Salvando métricas.'
METRIC_SAVED			=	'As métricas foram salvas em %s segundos.'
METRIC_CALCULATED		=	'As métricas foram calculadas em %s segundos.'
QUERIES_TIME			=	'As consultas requeridas foram processadas e realizadas em %s segundos.'
DOCUMENTS_TIME			=	'Os documentos requeridos foram lidos e processados em %s segundos.'
WORDS_TIME				=	'As palavras requeridas foram lidas e processadas em %s segundos.'
INDEX_TIME				=	'Os documentos foram indexados em %s segundos.'
INDEX_START				=	'Indexação dos documentos solicitados iniciada.'

QUERIES_READ_TIME		=	'As consultas foram lidas e processadas em %s segundos'

def setup_logger(name, filename):
	logger = logging.getLogger(name)
	
	if not len(logger.handlers):
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
	
def verify_stemmer(line, count, log_name, log_file):
	logger =  setup_logger(log_name, log_file)
	
	if line.endswith('\n'):
		line = line[:-1]
	
	if line == STEMMER:
		logger.debug(STEMMER_ENABLED)
		return PorterStemmer()
	elif line == NOSTEMMER:
		logger.debug(STEMMER_DISABLED)
		return None
	else:
		logger.error(NE_INSTRUCTION_ERROR + str(count + 1))
		exit_error(EXITED_WITH_ERROR)

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
	
def valida_termo(termo):
	if len(termo) > 1 and re.match("^[A-Z]*$", termo):
		return termo
	else:
		return None

def format_text(text):
	chars_to_remove = ['.', ',', '!', '?', ';', ':', '(', ')', '\n']
	sc = set(chars_to_remove)
	text = ''.join([c for c in text if c not in sc])

	return text.upper()

def exit_error(message):
	sys.exit(message)
	
def file_exists(filepath):
	return os.path.isfile(filepath)
