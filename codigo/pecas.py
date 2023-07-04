# meus módulos.
from biblioteca_externa.moldura_str import imprime, matriciar

""" fabricante de peças """

# o que pode ser importado.
__all__ = ['bola', 'xis', 'quadrado', "Jogadores"]

# obtem a matriz de tanto a bola, como
# o xis.
CAMINHO_BOLA = "dados/bola.txt"
CAMINHO_XIS = "dados/xis.txt"
CAMINHO_QUADRADO = "dados/quadrado.txt"
...

try:
   with (open(CAMINHO_BOLA, 'rt') as arq_i,
     open(CAMINHO_XIS) as arq_ii,
     open(CAMINHO_QUADRADO,'rt') as arq
   ):
      bola = matriciar(arq_i.read())
      xis = matriciar(arq_ii.read())
      quadrado = matriciar(arq.read())
   ...
except FileNotFoundError:
   CAMINHO_BOLA = "../dados/bola.txt"
   CAMINHO_XIS = "../dados/xis.txt"
   CAMINHO_QUADRADO = "../dados/quadrado.txt"
   with (
     open(CAMINHO_BOLA, 'rt') as arq_i,
     open(CAMINHO_XIS) as arq_ii,
     open(CAMINHO_QUADRADO,'rt') as arq
   ):
      bola = matriciar(arq_i.read())
      xis = matriciar(arq_ii.read())
      quadrado = matriciar(arq.read())
   ...
...

from enum import (Enum, auto)

class Jogadores(Enum):
   "molde de peças muito mais bem trabalhado"
   BOLA = ('O', bola)
   XIS = ('X', xis)
...



# execução para testes:
if __name__ == "__main__":
   imprime(bola)
   imprime(xis)
   imprime(quadrado)
...

