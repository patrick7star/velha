
# biblioteca do Python:
from curses import *
from math import floor, sqrt

# meus módulos:
import biblioteca_externa.espiral as BEE
from codigo.pecas import *
from codigo.motor import Fileira


# o que pode ser importado.
__all__ = ['Tabuleiro',"ForaTabuleiroError"]


# algumas exceções:
class ForaTabuleiroError(Exception):
   " exceção de que está fora do tabuleiro "
   def __str__(self):
      return "coordenada está fora da área do tabuleiro"
...
from enum import (IntEnum, auto)
# enumeradores:
class Quadrantes(IntEnum):
   """
   A contagem começa do superior esquerdo,
   indo à direita, e para baixo quando alcança
   a última coluna:

               1º 2º 3º
               4º 5º 6º
               7º 8º 9º
   """
   PRIMEIRO = auto()
   SEGUNDO  = auto()
   TERCEIRO  = auto()
   QUARTO  = auto()
   quinto  = auto()
   sexto  = auto()
   setimo = auto()
   oitavo  = auto()
   nono  = auto()
...

class Tabuleiro:
   # construtor ...
   def __init__(self, simbolo):
      # personalização do interface gráfica.
      self.janela = initscr()
      start_color()
      #use_default_colors()
      mousemask(True) # habilita mouse.
      curs_set(0)  # tira o cursor.
      self.janela.keypad(True) # ativa outras teclas não númericas.

      # paletas de cores:
      init_pair(1, COLOR_MAGENTA, COLOR_WHITE)
      init_pair(2, COLOR_GREEN, COLOR_WHITE)
      init_pair(3, COLOR_RED, COLOR_WHITE)
      init_pair(4, COLOR_BLUE, COLOR_WHITE)
      init_pair(5, COLOR_YELLOW, COLOR_WHITE)
      init_pair(6, COLOR_WHITE, COLOR_WHITE)

      # definindo uma cor do plano de fundo.
      self.janela.bkgd(' ', color_pair(6))

      # dimensão do terminal.
      self.LIN, self.COL = self.janela.getmaxyx()
      # comprimento das barras formando os tabuleiros.
      self.barra_h, self.barra_v = self.COL-35, self.LIN-5
      # impondo limite caso a tela se redimensiona
      # bastante.
      if self.barra_v >= 20 and self.barra_h >= 53:
         self.barra_h = 55
         self.barra_v = 22
      ...
      # 'a' de altura e 'c' de comprimento(miniretângulos).
      a, c = int(self.barra_v/3),int(self.barra_h/3)
      # canto superior esquerdo do retângulo onde
      # fica a tabela formando o tabuleiro.
      Y = int(self.LIN/2)-int(self.barra_v/2)
      X = int(self.COL/2)-int(self.barra_h/2)

      # formando barras horizontais:
      melhors = "\u2550"
      self.janela.hline(
         Y + a, X,
         "=", self.barra_h,
         color_pair(1)
      )
      self.janela.hline(
         Y + 2 * a, X,
         "=", self.barra_h,
         color_pair(1)
      )
      # formando barras verticais:
      self.janela.vline(
         Y, X + c,
         '#', self.barra_v,
         color_pair(1)
      )
      self.janela.vline(
         Y, X + 2 * c,
         '#', self.barra_v,
         color_pair(1)
      )
      # Lugares das peças. O canto superior
      # Lugares das peças. O canto superior
      # esquerdo para cada "escritura" das 
      # peças. Todos baseado na numeração
      # de 1 à 9; da esquerda à direita, de
      # cima para baixo.
      # primeira linha:
      self.q1 = (Y,X)
      self.q2 = (Y, X+c+1)
      self.q3 = (Y, X+2*(c+1))
      # segunda linha:
      self.q4 = (Y+(a+1), X)
      self.q5 = (Y+(a+1), X+c+1)
      self.q6 = (Y+(a+1), X+2*(c+1))
      # terceira linha:
      self.q7 = (Y+2*(a+1), X)
      self.q8 = (Y+2*(a+1), X+c+1)
      self.q9 = (Y+2*(a+1), X+2*(c+1))

      # Vamos adicionar a cada cojunto, este 
      # representando seu quadrante(em romano[por
      # estética]), todos pontos(coordenadas) que 
      # compõem tais quadrantes. Como o anterior,
      # tais variáveis são nomeadas com Q de quadrante
      # e o número do quadrante que representa, na
      # mesma ordem que o anterior.
      self.Q_I = set(
         (i,j) for i in range(Y,Y+a) 
         for j in range(X,X+c)
      )
      self.Q_II = set(
         (i,j) for i in range(Y,Y+a) 
         for j in range(X+c, X+2*c)
      )
      self.Q_III = set(
         (i,j) for i in range(Y,Y+a) 
         for j in range(X+2*c,X+3*c)
      )
      self.Q_IV = set(
         (i,j) for i in range(Y+a,Y+2*a) 
         for j in range(X,X+c)
      )
      self.Q_V = set(
         (i,j) for i in range(Y+a,Y+2*a) 
         for j in range(X+c,X+2*c)
      )
      self.Q_VI = set(
         (i,j) for i in range(Y+a,Y+2*a) 
         for j in range(X+2*c,X+3*c)
      )
      self.Q_VII = set(
         (i,j) for i in range(Y+2*a,Y+3*a) 
         for j in range(X,X+c)
      )
      self.Q_VIII = set(
         (i,j) for i in range(Y+2*a,Y+3*a) 
         for j in range(X+c,X+2*c)
      )
      self.Q_IX = set(
         (i,j) for i in range(Y+2*a,Y+3*a) 
         for j in range(X+2*c,X+3*c)
      )

      # as dimensões máximas e mínimas das
      # peças neste tabuleiro variam entre
      # 5x7 à 5x9, então posso fazer cálculos
      # na mão como centralizar tais dimensões
      # tão próximas. No futuro com mais
      # peças, de variado tamanhos, talvez
      # precise de uma função que compute 
      # o centro de variadas peças de, um bocado
      # de dimensões. Vamos levar a dimensão padrão
      # a do maior, ou seja, 5x9.
      ty,tx = (2.5,4.5)
      sequencia = (
         self.q1, self.q2, self.q3,
         self.q4, self.q5, self.q6,
         self.q7, self.q8, self.q9
      )
      for (i,(Y,X)) in enumerate(sequencia):
         var = 'q'+str(i+1)
         self.__dict__[var] = (
            self.__dict__[var][0] - 1 + int((a-ty)/2), 
            self.__dict__[var][1] + int((c-tx)/2)
         ) 
      ...

      self.janela.refresh() # monta todo tabuleiro vázio.
   ...

   def coloca_peca(self, peca: Jogadores, local):
      """ Só aceito nove valores inteiros(1 à 9).
      dimensões. """
      m,n = len(peca), len(peca[0])
      for i in range(m):
         for j in range(n):
            var = 'q' + str(local)
            # selecionando cor baseado na 
            # peça passada como argumento..
            if peca == xis:
               cor = color_pair(3)  # X é vermelho.
            elif peca == bola:
               cor = color_pair(4)  # O é azul.
            elif peca == quadrado:
               cor = color_pair(2)  # [] é verde.
            else:
               raise Exception('peça desconhecida')
            self.janela.addch(
               i + self.__dict__[var][0],
               j + self.__dict__[var][1], 
               peca[i][j], cor
            )
         ...
      ...
      self.janela.refresh()  # atualiza a janela.
   ...

   def marca_vitoria(self, fileira):
      " marca o 'tiro' de vitória do vencedor. "
      # compr. da barra horizontais e verticais.
      comprimento = self.barra_h + 5
      comprimentoV = self.barra_v + 2
      passo_adianteY = int(self.q1[0]/2)
      passo_adianteX = int(self.q1[1]/3)
      cor = color_pair(5)  # coloração da barra.

      if fileira == Fileira.HORIZONTAL_SUPERIOR:
         y = self.q1[0] + passo_adianteY
         x = self.q1[1] - passo_adianteX
      elif fileira == Fileira.HORIZONTAL_MEDIO:
         y = self.q4[0] + passo_adianteY
         x = self.q4[1] - passo_adianteX
      elif fileira == Fileira.HORIZONTAL_INFERIOR:
         y = passo_adianteY + self.q7[0]
         x = self.q7[1] - passo_adianteX
      elif fileira == Fileira.VERTICAL_ESQUERDA:
         y = self.q1[0] - passo_adianteY
         x = self.q1[1] + 2
      elif fileira == Fileira.VERTICAL_MEDIA:
         y = self.q2[0] - passo_adianteY
         x = self.q2[1] + 2
      elif fileira == Fileira.VERTICAL_DIREITA:
         y = self.q3[0] - passo_adianteY
         x = self.q3[1] + 2
      ...

      # se estiver entre 1 à 3 é uma fileira horizontal,
      # do contrário 4 à 6 vertical.
      if 1 <= fileira <= 3:
         for c in range(comprimento):
            self.janela.addch(y, x+c, '=', cor)
            napms(20)
            self.janela.refresh()
         ...
      elif 4 <= fileira <= 6:
         for l in range(comprimentoV):
            self.janela.addch(y+l, x, '&', cor)
            napms(20)
            self.janela.refresh()
         ...
      elif fileira == 7:
         risca_diagonal(self.janela, self.q1, self.q9)
      else:
         risca_diagonal_secundaria(self,self.q3,self.q7)
   ...

   def posicao_clicada(self, coord):
      """ 
      denuncia que local no tabuleiro o mouse
      clicou, eventuamente, retornando tal local. 
      """
      if coord in self.Q_I: return 1
      elif coord in self.Q_II: return 2
      elif coord in self.Q_III: return 3
      elif coord in self.Q_IV: return 4
      elif coord in self.Q_V: return 5
      elif coord in self.Q_VI: return 6
      elif coord in self.Q_VII: return 7
      elif coord in self.Q_VIII: return 8
      elif coord in self.Q_IX: return 9
      else:
         # sobe uma exceção por coordenada inválida.
         raise ForaTabuleiroError()
      pass
   ...

   def posicoes(self):
      """ 
      obtem a coordenada do clique na janela,
      e seu respectivo local no tabuleiro. 
      """
      try:
         coordenada = getmouse()
         # invertendo para colocar mais palatável
         # ao tipo de input do programa.
         coord_mouse = (coordenada[2],coordenada[1])
         return coord_mouse
      except: pass
   ...

   def desmancha_tabuleiro(self):
      napms(1_000)
      endwin()
   ...


def risca(janela, A, B):
   """ faz um risco diagonal dado um ponto A
   (inicial), e um ponto B(final). """
   (y1,x1),(y2,x2) = (A, B)
   cor = color_pair(5)  # coloração da barra.
   # estimando a quantia de "lugares" da matriz
   # é mais ou menos a diagonal do retângulo
   # que ela adequa-se.
   L = int(floor(sqrt((x1-x2)**2+(y1-y2)**2)))
   # proporção básica de quantos colunas 
   # têm para linhas.
   variacao = (x2-x1)/(y2-y1)
   while L > 0:
      if not((x1 > x2) and (y1 <= y2)): break
      x1 = int(x1+variacao)  # vai para direita.
      L -= 1   # desconta na contagem.
      y1 += 1  # vai um para baixo.
      janela.addch(y1,x1, 'H',cor)
      napms(50) # 50 milisegundos.
      janela.refresh()
   pass


def projecao(I, F):
   " faz a projeção de risco de um ponto inicial à um final"
   (yi,xi),(yf,xf) = (I,F)
   d_IF = int(floor(sqrt((xi-xf)**2+(yi-yf)**2)))
   try:
      # taxa de variação de x em relação a y.
      dxdy = floor((xf-xi)/(yf-yi))
   except ZeroDivisionError:
      dxdy = 0
   while d_IF > 0:
      yi += 1
      xi = int(xi+dxdy)
      yield((yi,xi))
      d_IF -= 1
   pass


def risca_diagonal(janela, A,B):
   """ risca diagonal principal na janela, dado
   um ponto inicial e um final; tais pontos
   no formato (y,x) é claro!"""
   (y1,x1),(y2,x2) = (A, B)
   cor = color_pair(5)  # coloração da barra.
   # estimando a quantia de "lugares" da matriz
   # é mais ou menos a diagonal do retângulo
   # que ela adequa-se.
   L = int(floor(sqrt((x1-x2)**2+(y1-y2)**2)))
   # proporção básica de quantos colunas 
   # têm para linhas.
   variacao = abs(x1-x2)/abs(y1-y2)
   #L = 21
   while L > 0:
      x1 = int(x1+variacao)  # vai para direita.
      L -= 1   # desconta na contagem.
      y1 += 1  # vai um para baixo.
      if (y1 < y2) and (x1 < x2):
         janela.addch(y1,x1, 'X',cor)
      napms(50) # 50 milisegundos.
      janela.refresh()
   pass


def risca_diagonal_secundaria(TAB,A,B):
   """ uma função que projeta a trajetória a
   cada passo, se não atingir o ponto B em tal
   projeção, então faz um ajuste na direção até
   que uma nova projeção alcance. """
   # escolhendo um ponto certo.
   for ponto in BEE.espiral(A):
      if B in projecao(ponto,B):
         A = ponto
         break
   risca(TAB.janela, A,B)
   pass


# execução de testes:
if __name__ == "__main__":
   t = Tabuleiro('#')
   import random, sys

   for i in range(9):
      aleatorio = random.randint(1,9)
      t.coloca_peca(xis, aleatorio)

   tecla = t.janela.getch()
   coord = None
   try:
      coord = getmouse()
   except:
      coord = 'erro pelo caminho'
      pass
   else:
      pass
   t.janela.refresh()
   endwin()

   print("coordenas ==> %s"%coord)
   E = sys.exc_info()
   print("exeção:\n%s\n%s\n%s"%(E[0],E[1],E[2]))
   raise ForaTabuleiroError()
