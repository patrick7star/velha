""" tentar criar um código para me ceder 
coordenadas de forma espiral; ou um dado 
intervalo bidimensional. """

def espiral(ponto):
   """ dá um pares-ordenados(no formato tela,
   não matemático) para um desenho formando
   uma espiral nascendo de um ponto passado."""
   y,x = ponto # par ordenado de tela, não-matemático.
   # funções que mudam a direção das
   # cordenadas iniciais.
   def baixo():
      nonlocal y
      y += 1
   def direita():
      nonlocal x
      x += 1
   def esquerda():
      nonlocal x
      x -= 1
   def cima():
      nonlocal y
      y -= 1
   # funções numa ordem crescente de quatro.
   direcoes = (baixo, esquerda, cima, direita)
   q = 0 # contador e chave.
   while q <= 12:
      # gera uma quantia 'q' inicialmente.
      for k in range(q):
         direcoes[q%4]()
         yield((y,x))
      # aumenta a quantia a criar, e 
      # a chave para nova função computada.
      q += 1
   pass


def range_bidimensional(ponto, raio):
   """ pega um ponto e circunda ela com
   todos pontos formando um quadrado, dado
   ele como centro. O "raio"(metade do
   lado de tal quadrado também tem de ser
   informado também, com um limite. """
   # par ordenado baseado em tela, não-matemático molde.
   y, x = ponto
   # acha ponto superior esquerdo.
   x -= raio
   y -= raio
   # partindo deste ponto superior-esquerdo
   # mapeia todo o quadrado.
   for i in range(x, x+2*raio):
      for j in range(y, y+2*raio):
         yield(j,i,)
   pass


if __name__ == "__main__":
   # biblioteca para testes.
   import time, tela

   coords = range_bidimensional((5,12), 4)

   T = tela.Tela(0,0)

   for (y,x) in coords:
      T.marca(y,x)

   #time.sleep(2.5)  # dois segundos e meio.
   T.marca(5, 12,simbolo='O')

   for (y,x) in espiral((18,45)):
      T.marca(y,x, simbolo='*')
   print(T)

   for (linha, coluna) in espiral((6,25)):
      T.marca(linha,coluna, simbolo='O')
      time.sleep(0.1)
      print(T)
