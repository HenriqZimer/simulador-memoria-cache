"""Interface de linha de comando para o simulador de memoria cache.

Autores:
- [Seu Nome]
- [Nome do Colega]

O programa le os parametros da cache, carrega os enderecos de um arquivo texto
e delega a simulacao para a classe CacheSimulator.
"""

import argparse
import os

from cache_simulator import CacheSimulator


def parse_address_file(filepath):
    """Le enderecos decimais ou hexadecimais de um arquivo .txt."""
    addresses = []
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Erro: Arquivo '{filepath}' não encontrado.")

    with open(filepath, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            # Linhas vazias e comentarios nao fazem parte da sequencia de acessos.
            if not line or line.startswith("#"):
                continue

            try:
                addresses.append(int(line, 16) if line.lower().startswith("0x") else int(line, 10))
            except ValueError as exc:
                raise ValueError(f"Erro: Endereço inválido na linha {line_number}: '{line}'.") from exc

    return addresses


def build_parser():
    """Configura os argumentos aceitos pela linha de comando."""
    parser = argparse.ArgumentParser(description="Simulador de Memória Cache")
    parser.add_argument("--cache-size", type=int, required=True, help="Tamanho total da cache em bytes")
    parser.add_argument("--block-size", type=int, required=True, help="Tamanho do bloco em bytes")
    parser.add_argument("--assoc", type=int, required=True, help="Grau de associatividade (1 para mapeamento direto)")
    parser.add_argument("--addr-bits", type=int, required=True, help="Número de bits do endereço físico")
    parser.add_argument("--input", type=str, required=True, help="Caminho do arquivo com endereços")
    parser.add_argument("--policy", type=str, default="LRU", choices=["LRU", "FIFO"], help="Política de substituição")
    parser.add_argument("--verbose", action="store_true", help="Exibe o estado detalhado a cada acesso")
    return parser


def main():
    args = build_parser().parse_args()

    try:
        simulator = CacheSimulator(
            cache_size=args.cache_size,
            block_size=args.block_size,
            assoc=args.assoc,
            addr_bits=args.addr_bits,
            policy=args.policy,
            verbose=args.verbose,
        )

        addresses = parse_address_file(args.input)
        simulator.print_configuration()

        for address in addresses:
            simulator.access(address)

        simulator.report()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
