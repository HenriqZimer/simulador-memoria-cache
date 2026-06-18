# Simulador de Memória Cache M3

## Integrantes do Grupo
- Henrique Zimermann
- Gabriel Sereia

Link da Apresentacao:
[## Link da Apresentacao:](https://youtu.be/R5oLmub8Z7w)

## Descrição
Este projeto implementa um simulador de memória cache em Python, conforme a prática M3 de Organização de Computadores. O simulador lê uma sequência de endereços de memória, decompõe cada endereço em `tag`, `index` e `offset`, simula os acessos na cache e apresenta estatísticas de desempenho.

O programa suporta:
- Mapeamento direto (`--assoc 1`).
- Mapeamento associativo por conjunto (`--assoc N`).
- Política de substituição `LRU`.
- Política de substituição `FIFO`.
- Endereços em decimal ou hexadecimal.
- Comentários no arquivo de entrada usando `#`.
- Saída detalhada com `--verbose`.

## Estrutura do Projeto
```text
.
├── Makefile
├── README.md
├── acessos.txt
├── acessos_conflito.txt
├── cache_simulator.py
└── simulador.py
```

Arquivos principais:
- `simulador.py`: ponto de entrada do programa. Faz a leitura dos argumentos da linha de comando e do arquivo de endereços.
- `cache_simulator.py`: contém a lógica da cache, incluindo validações, decomposição de endereço, hits, misses e substituição.
- `acessos.txt`: arquivo curto de teste com endereços em decimal e hexadecimal.
- `acessos_conflito.txt`: arquivo de teste para observar conflitos e substituições.
- `Makefile`: atalhos para executar e testar o simulador.

## Requisitos
É necessário apenas Python 3. O projeto não usa bibliotecas externas.

## Como Executar
Comando básico:
```bash
python3 simulador.py --cache-size 1024 --block-size 32 --assoc 2 --addr-bits 16 --input acessos.txt
```

Com saída detalhada:
```bash
python3 simulador.py --cache-size 512 --block-size 8 --assoc 4 --addr-bits 16 --input acessos.txt --verbose
```

Usando FIFO:
```bash
python3 simulador.py --cache-size 2048 --block-size 64 --assoc 8 --addr-bits 32 --input acessos_conflito.txt --policy FIFO
```

## Executando com Make
Também é possível usar o `Makefile`:

```bash
make run
make verbose
make fifo
make test
make clean
```

Alvos disponíveis:
- `make run`: executa o exemplo básico.
- `make verbose`: executa o exemplo com estado da cache após cada acesso.
- `make fifo`: executa um exemplo usando a política FIFO.
- `make test`: compila os arquivos Python e roda as configurações de referência do enunciado.
- `make clean`: remove arquivos temporários do Python.

## Parâmetros
| Parâmetro | Descrição | Exemplo |
| --- | --- | --- |
| `--cache-size` | Tamanho total da cache em bytes. | `1024` |
| `--block-size` | Tamanho de cada bloco/linha em bytes. | `32` |
| `--assoc` | Grau de associatividade. Use `1` para mapeamento direto. | `1`, `2`, `4` |
| `--addr-bits` | Número de bits do endereço físico. | `16` |
| `--input` | Caminho do arquivo `.txt` com os endereços. | `acessos.txt` |
| `--policy` | Política de substituição. Pode ser `LRU` ou `FIFO`. | `LRU` |
| `--verbose` | Mostra cada acesso, os campos do endereço e o estado da cache. | flag |

## Formato do Arquivo de Entrada
O arquivo de endereços deve conter um endereço por linha. São aceitos valores decimais e hexadecimais com prefixo `0x`. Linhas vazias e linhas iniciadas com `#` são ignoradas.

Exemplo:
```text
# Exemplo de arquivo de endereços
0x0010
0x0024
0x0010
256
0x00FF
```

## Saída do Programa
Antes da simulação, o programa exibe a configuração calculada:
- Tamanho da cache.
- Tamanho do bloco.
- Associatividade.
- Bits de `tag`, `index` e `offset`.

Ao final, o relatório mostra:
- Total de acessos.
- Quantidade e percentual de cache hits.
- Quantidade e percentual de cache misses.

Com `--verbose`, cada acesso também mostra:
- Endereço acessado.
- Campos `tag`, `index` e `offset`.
- Resultado `HIT` ou `MISS`.
- Estado atual dos conjuntos preenchidos da cache.

## Validações Implementadas
O simulador trata entradas inválidas, incluindo:
- Tamanho de cache que não é potência de 2.
- Tamanho de bloco que não é potência de 2.
- Associatividade inválida.
- Bloco maior que a cache.
- Combinação inconsistente entre cache, bloco e associatividade.
- Número de bits de endereço insuficiente.
- Arquivo de entrada inexistente.
- Linha com endereço inválido.
- Endereço fora do espaço de endereçamento informado por `--addr-bits`.

## Configurações de Referência
Estas configurações foram usadas para validar a decomposição de endereços:

| Cache | Bloco | Assoc. | Endereço | Offset | Index | Tag |
| --- | --- | --- | --- | --- | --- | --- |
| 256 B | 16 B | 1-way | 16 bits | 4 bits | 4 bits | 8 bits |
| 1024 B | 32 B | 2-way | 16 bits | 5 bits | 4 bits | 7 bits |
| 512 B | 8 B | 4-way | 16 bits | 3 bits | 4 bits | 9 bits |
| 2048 B | 64 B | 8-way | 32 bits | 6 bits | 2 bits | 24 bits |
