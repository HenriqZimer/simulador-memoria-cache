"""Modulo com a logica principal do simulador de memoria cache.

Este arquivo fica separado da interface de linha de comando para deixar o codigo
mais organizado: aqui estao os calculos de tag/index/offset, a estrutura da
cache, as politicas de substituicao e as estatisticas da simulacao.
"""

import math


def is_power_of_two(n):
    """Retorna True quando n e uma potencia de 2 positiva."""
    return isinstance(n, int) and n > 0 and (n & (n - 1) == 0)


class CacheSimulator:
    """Simula uma cache com mapeamento direto ou associativo por conjunto."""

    def __init__(self, cache_size, block_size, assoc, addr_bits, policy="LRU", verbose=False):
        self._validate_parameters(cache_size, block_size, assoc, addr_bits)

        self.cache_size = cache_size
        self.block_size = block_size
        self.assoc = assoc
        self.addr_bits = addr_bits
        self.policy = policy.upper()
        self.verbose = verbose

        self.num_sets = cache_size // (block_size * assoc)
        if not is_power_of_two(self.num_sets):
            raise ValueError("Erro: A configuração resulta em um número de conjuntos que não é potência de 2.")

        # Quantidade de bits usada em cada campo do endereco.
        self.offset_bits = int(math.log2(block_size))
        self.index_bits = int(math.log2(self.num_sets))
        self.tag_bits = addr_bits - self.index_bits - self.offset_bits

        if self.tag_bits < 0:
            raise ValueError("Erro: addr-bits insuficiente para representar tag, index e offset.")

        # Cada conjunto guarda as tags em ordem: a primeira e a candidata a sair.
        self.cache = [[] for _ in range(self.num_sets)]

        self.hits = 0
        self.misses = 0
        self.accesses = 0

    def _validate_parameters(self, cache_size, block_size, assoc, addr_bits):
        """Valida os parametros obrigatorios descritos no enunciado."""
        if not is_power_of_two(cache_size) or not is_power_of_two(block_size):
            raise ValueError("Erro: O tamanho da cache e o tamanho do bloco devem ser potências de 2.")

        if not is_power_of_two(assoc):
            raise ValueError("Erro: A associatividade deve ser uma potência de 2 maior que zero.")

        if not isinstance(addr_bits, int) or addr_bits <= 0:
            raise ValueError("Erro: addr-bits deve ser um inteiro positivo.")

        if block_size > cache_size:
            raise ValueError("Erro: O tamanho do bloco não pode ser maior que o tamanho da cache.")

        if cache_size % (block_size * assoc) != 0:
            raise ValueError("Erro: Parâmetros inconsistentes; cache-size deve ser divisível por block-size * assoc.")

    def split_address(self, address):
        """Divide um endereco em tag, index e offset."""
        if address < 0 or address >= (1 << self.addr_bits):
            raise ValueError(f"Erro: Endereço {address} fora do espaço de endereçamento de {self.addr_bits} bits.")

        offset = address & ((1 << self.offset_bits) - 1)
        index = (address >> self.offset_bits) & ((1 << self.index_bits) - 1)
        tag = address >> (self.offset_bits + self.index_bits)
        return tag, index, offset

    def access(self, address):
        """Executa um acesso a memoria e atualiza hits, misses e estado da cache."""
        tag, index, offset = self.split_address(address)
        target_set = self.cache[index]

        self.accesses += 1
        hit = tag in target_set

        if hit:
            self.hits += 1
            if self.policy == "LRU":
                # Em LRU, uma tag acessada vira a mais recente do conjunto.
                target_set.remove(tag)
                target_set.append(tag)
        else:
            self.misses += 1
            self._insert_tag(target_set, tag)

        if self.verbose:
            status = "HIT" if hit else "MISS"
            print(f"Endereço: {hex(address)} | Tag: {tag} | Index: {index} | Offset: {offset} -> {status}")
            print(f"Estado da cache: {self.format_cache_state()}")

        return hit

    def _insert_tag(self, target_set, tag):
        """Insere uma tag e remove a mais antiga quando o conjunto esta cheio."""
        if len(target_set) >= self.assoc:
            target_set.pop(0)

        target_set.append(tag)

    def format_cache_state(self):
        """Retorna uma representacao textual dos conjuntos preenchidos."""
        sets = []
        for index, cache_set in enumerate(self.cache):
            if cache_set:
                tags = ", ".join(str(tag) for tag in cache_set)
                sets.append(f"Set {index}: [{tags}]")
        return " | ".join(sets) if sets else "vazia"

    def print_configuration(self):
        """Imprime a configuracao e a decomposicao calculada antes da simulacao."""
        print("=" * 50)
        print(" CONFIGURAÇÃO DA CACHE ")
        print("=" * 50)
        print(f"Cache={self.cache_size}B, Bloco={self.block_size}B, Assoc={self.assoc}-way")
        print(f"Tag={self.tag_bits} bits, Index={self.index_bits} bits, Offset={self.offset_bits} bits")
        print("=" * 50)

    def report(self):
        """Imprime o relatorio final exigido pelo enunciado."""
        print("\n" + "=" * 50)
        print(" RELATÓRIO DA SIMULAÇÃO DE CACHE ")
        print("=" * 50)
        print(f"Configuração: Cache={self.cache_size}B, Bloco={self.block_size}B, Assoc={self.assoc}-way")
        print(f"Decomposição: Tag={self.tag_bits} bits, Index={self.index_bits} bits, Offset={self.offset_bits} bits")
        print("-" * 50)
        print(f"Total de acessos : {self.accesses}")

        if self.accesses > 0:
            hit_rate = (self.hits / self.accesses) * 100
            miss_rate = (self.misses / self.accesses) * 100
            print(f"Cache Hits       : {self.hits} ({hit_rate:.2f}%)")
            print(f"Cache Misses     : {self.misses} ({miss_rate:.2f}%)")

        print("=" * 50 + "\n")
