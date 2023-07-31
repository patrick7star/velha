
"""
 Motor do jogo; aqui ficará todos 
os procedimentos de verificação de vitória,
reposição de peças; pontuação do placar e etc...
"""


# o que pode ser importado:
__all__ = [
   "pecas_i", "pecas_ii","matriz",
  "peca_vitoriosa", "adiciona_peca",
  "numeracao_em_coord", "jogadas_restantes",
  "LocalJaPreenchidoError", "tabuleiro_str",
  "fileira_ganha", "Fileira"
]

# exceções:
class LocalJaPreenchidoError(Exception):
   def __str__(self):
      msg = "este local já foi preenchido por uma peça."
      return msg
...

# matriz contendo todas peças.
# no ínicio estará apenas como "null".
matriz = [
   [None for i in range(3)] 
   for j in range(3)
]
# peças(portanto, jogadores).
pecas_i, pecas_ii = ('X', 'O')
# tabuleiro em texto, seu molde.
tabuleiro_molde= """
   |     |
 {} |  {}  | {}
==============
 {} |  {}  | {}
==============
 {} |  {}  | {}
   |     |
"""


# verifica vitória de uma peça.
def peca_vitoriosa(peca):
   "verifica se peça é a vencedora"
   # apelido para variável global para
   # melhor a legibilidade e a codificação.
   m = matriz
   # todas proposições que validam uma vitória
   # para tal peça.
   if m[0][0] == m[0][1] == m[0][2] == peca:
      return True  # primeira linha.

   elif m[1][0] == m[1][1] == m[1][2] == peca:
      return True # segunda linha.

   elif m[2][0] == m[2][1] == m[2][2] == peca:
      return True # terceira linha.

   elif m[0][0] == m[1][0] == m[2][0] == peca:
      return True # primeira coluna.

   elif (m[0][1] == m[1][1]==m[2][1]==peca):
      return True # segunda coluna.

   elif m[0][2] == m[1][2] == m[2][2] == peca:
      return True # terceira coluna.

   elif m[0][0] == m[1][1] == m[2][2] == peca:
      return True # diagonal principal.

   elif m[0][2]==m[1][1]== m[2][0] == peca:
      return True # diagonal secundaria.

   else: 
      return False
...

# Adiciona uma peça na matriz. Você 
# adiciona apenas numa posição, ou 
# seja, não pode sobreescrever peça
# já posicionada.
def adiciona_peca(peca, coordenada):
   (linha,coluna) = coordenada
   # proposições:
   p1 = (peca != None) # peça válida.
   p2 = (matriz[linha][coluna] == None)  # lacuna vaga.
   if p2 and p1:
      matriz[linha][coluna] = peca
   else:
      raise LocalJaPreenchidoError()
...

# traduz um local numa coordenada legível
# pela matriz.
def numeracao_em_coord(local):
   """ retorna uma coordenada exclusiva para
   matriz, então será adicionada uma peça nela."""
   try:
      if local == 1: return (0,0)
      elif local == 2: return (0,1)
      elif local == 3: return (0,2)
      elif local == 4: return (1,0)
      elif local == 5: return (1,1)
      elif local == 6: return (1,2)
      elif local == 7: return (2,0)
      elif local == 8: return (2,1)
      elif local == 9: return (2,2)
      else: pass
   except:
      return numeracao_em_coord(local % 9 + 1)
...

def tabuleiro_str():
   """ retorna uma versão string do "tabuleiro"
   de tic-toc-toe, tendo peças adicionadas, ou
   não, e isto independe se a partida está
   finalizada. """
   pecas_posicionais = [
      str(matriz[i][j]) for i in range(3)
      for j in range(3)
   ]
   pecas_posicionais = [
      s.replace('None',' ')
      for s in pecas_posicionais
   ]
   return tabuleiro_molde.format(*pecas_posicionais)
...

def jogadas_restantes():
   """ retorna a contagem de jogadas restantes"""
   return sum(M.count(None) for M in matriz)
...

# biblioteca padrão.
import enum
from enum import (auto, IntEnum)

class Fileira(IntEnum):
   HORIZONTAL_SUPERIOR = auto()
   HORIZONTAL_MEDIO = auto()
   HORIZONTAL_INFERIOR= auto()
   VERTICAL_ESQUERDA = auto()
   VERTICAL_MEDIA = auto()
   VERTICAL_DIREITA = auto()
   DIAGONAL_PRINCIPAL = auto()
   DIAGONAL_SECUNDARIA = auto()
...

def fileira_ganha():
   """ 
   retorna o número da fileira ganha no jogo.
   A numeração é a seguinte: 1ª linha superior;
   2ª linha do meio; 3ª linha inferior; 4ª coluna
   da esquerda; 5ª coluna do meio; 6ª coluna da
   direita; 7ª diagonal principal e 8ª diagonal
   secundária.
   """
   if peca_vitoriosa(pecas_i):
      peca = pecas_i
   elif peca_vitoriosa(pecas_ii):
      peca = pecas_ii
   else:
      raise Exception("não há vencedor; jogo empatado!")

   if matriz[0][0] == matriz[0][1] == matriz[0][2] == peca:
      return Fileira.HORIZONTAL_SUPERIOR 

   elif matriz[1][0] == matriz[1][1] == matriz[1][2] == peca:
      return Fileira.HORIZONTAL_MEDIO

   elif matriz[2][0] == matriz[2][1] == matriz[2][2] == peca:
      return Fileira.HORIZONTAL_INFERIOR

   elif matriz[0][0] == matriz[1][0] == matriz[2][0] == peca:
      return Fileira.VERTICAL_ESQUERDA

   elif (matriz[0][1] == matriz[1][1]==matriz[2][1]==peca):
      return Fileira.VERTICAL_MEDIA

   elif matriz[0][2] == matriz[1][2] == matriz[2][2] == peca:
      return Fileira.VERTICAL_DIREITA

   elif matriz[0][0] == matriz[1][1] == matriz[2][2] == peca:
      # diagonal principal.
      return Fileira.DIAGONAL_PRINCIPAL

   else: 
      # diagonal secundaria.
      return Fileira.DIAGONAL_SECUNDARIA
... 

# excuções de testes:
if __name__ == '__main__':
   peca = 'x'
   print(tabuleiro_str())
   print('jogo ganho=', peca_vitoriosa(peca))
   adiciona_peca(peca, (0,0))
   print(tabuleiro_str())
   adiciona_peca(peca, (1,1))
   adiciona_peca(peca, (2,1))
   print(tabuleiro_str)
   print('jogo ganho=', peca_vitoriosa(peca))
   #matriz[0][2], matriz[1][2], matriz[2][2] = peca,peca,peca
   adiciona_peca(peca, (0,2))
   adiciona_peca(peca, (1,2))
   print(tabuleiro_str())
   adiciona_peca(peca, (2,2))
   print(tabuleiro_str())
   print('jogo ganho=', peca_vitoriosa(peca))

   try:
      adiciona_peca(peca,(0,2))
   except:
      print("tente outra coordenada!")
