SISTEMA DE RECUPERAÇÃO EM MEMÓRIA SEGUNDO O MODELO VETORIAL

Para utilização do sistema em questão, é necessária a instalação do Python3, juntamente com a biblioteca NLTK.

Formas de utilização

É possível utilizar o sistema por meio da execução de todos os módulos de uma vez, ou, por meio da execução individual de cada módulo, desde que o usuário tenha posse dos arquivos gerados pelos módulos anteriores.

Devem ser seguidos os seguintes passos para sua execução.
- Abrir o terminal em sistemas GNU/Linux ou Prompt de Comando (Windows PowerShell ou similar) em sistemas Windows.
- Navegar até a pasta onde está contido o código fonte do sistema.
- Executar o comando python3 main.py ou python main.py, dependendo da versão principal do python em seu sistema.
- Em sistemas Windows pode ser necessária a utilização do caminho completo para o interpretador Python.
	Exemplo: C:\Python34\python.exe main.py

Para execução de um módulo separadamente, ao invés de main.py, deve-se escolher o arquivo do módulo correspondente.

Gerador Lista Invertida: inverted_index_generator.py
Indexador: indexer.py
Processador de Consultas: query_processor.py
Buscador: searcher.py
Avaliador: evaluator.py

OBS: O módulo Avaliador não é executado automaticamente quando se executa o sistema inteiro, sendo necessária sua execução separada. Para a sua execução é necessário que o usuário tenha dois arquivos de resultados de uma mesma base válidos, além de um arquivo de resultados esperados.
