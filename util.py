#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 2015
@author: Julio Barbieri
"""

import sys
import os.path

GENERATOR_SEPARATOR		=	'='
GENERATOR_FILENAME		=	'gli.cfg'

CMD_LEIA				=	'LEIA'
CMD_ESCREVA				=	'ESCREVA'

LINE					=	'linha '
FORMAT_ERROR 			=	'Erro na formatação do arquivo inserido, ' + LINE
NE_INSTRUCTION_ERROR	=	'Instrução não existente, ' + LINE
INSTRUCTION_ORDER_ERROR	=	'Instrução de leia após instrução de escreva, ' + LINE
FILE_NOT_FOUND			=	'Arquivo não encontrado, nome: '

def show_error(message):
	print >> sys.stderr, (message)
	sys.exit(1)
	
def file_exists(filepath):
	return os.path.isfile(filepath)
