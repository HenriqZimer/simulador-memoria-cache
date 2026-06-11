PYTHON := python3
SCRIPT := simulator.py

.PHONY: help run verbose fifo test clean

help:
	@echo "Alvos disponíveis:"
	@echo "  make run      - executa exemplo básico"
	@echo "  make verbose  - executa exemplo com saída detalhada"
	@echo "  make fifo     - executa exemplo usando política FIFO"
	@echo "  make test     - compila os arquivos Python e roda exemplos do enunciado"
	@echo "  make clean    - remove arquivos temporários do Python"

run:
	$(PYTHON) $(SCRIPT) --cache-size 1024 --block-size 32 --assoc 2 --addr-bits 16 --input acessos.txt

verbose:
	$(PYTHON) $(SCRIPT) --cache-size 512 --block-size 8 --assoc 4 --addr-bits 16 --input acessos.txt --verbose

fifo:
	$(PYTHON) $(SCRIPT) --cache-size 2048 --block-size 64 --assoc 8 --addr-bits 32 --input acessos_conflito.txt --policy FIFO

test:
	$(PYTHON) -m py_compile simulator.py cache_simulator.py
	$(PYTHON) $(SCRIPT) --cache-size 256 --block-size 16 --assoc 1 --addr-bits 16 --input acessos.txt
	$(PYTHON) $(SCRIPT) --cache-size 1024 --block-size 32 --assoc 2 --addr-bits 16 --input acessos.txt
	$(PYTHON) $(SCRIPT) --cache-size 512 --block-size 8 --assoc 4 --addr-bits 16 --input acessos.txt
	$(PYTHON) $(SCRIPT) --cache-size 2048 --block-size 64 --assoc 8 --addr-bits 32 --input acessos_conflito.txt --policy FIFO

clean:
	rm -rf __pycache__
