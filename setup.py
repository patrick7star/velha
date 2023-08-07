#!/bin/python3 -BO

# biblioteca do jogo.
from codigo.tabuleiro import *
from codigo.pecas import *
from codigo.motor import *
# bibliote externas:
from biblioteca_externa.utilitarios.lib import tela

from os import (chmod, getenv)
from stat import (S_IXGRP, S_IRWXU, S_IXOTH)
from os.path import join as JoinPath
# muda a permição do arquivo script que lança
# estes jogo. Só clicar e jogar.
try:
   chmod("setup.py", S_IRWXU | S_IXGRP | S_IXOTH)
except FileNotFoundError:
   caminho = JoinPath(
      getenv("PYTHON_CODES"), 
      "velha/setup.py"
   )
   chmod(caminho, S_IRWXU | S_IXGRP | S_IXOTH)
...


# dício contendo todos os DOIS possíveis
# jogadores.
jogadores = {
   True: xis,
   False: quadrado
}
# peça xis, sempre o primeiro.
primeiro = True
# instância o tabuleiro para o jogo(inicializa
# a "interface gráfica").
tabuleiro = Tabuleiro()

from codigo.ponto import Direcao
from curses import (
   KEY_RIGHT, KEY_LEFT,
   KEY_DOWN, KEY_UP, KEY_ENTER
)
# fazendo com que o teclado também funcione
# para marcar posições, navegando através
# do jogo.
def converte_em_direcoes(code: int) -> Direcao:
   if code == KEY_UP:
      return Direcao.CIMA
   elif KEY_DOWN == code:
      return Direcao.BAIXO
   elif KEY_LEFT == code:
      return Direcao.ESQUERDA
   elif KEY_RIGHT == code:
      return Direcao.DIREITA
   else:
      return None
   ...
...

from sys import argv
qtd_args = len(argv)
uso_do_teclado = (qtd_args > 1 and argv[1] == "--teclado")

# roda o jogo até não houver mais jogadas.
while jogadas_restantes() != 0:
   # desenha todo tabuleiro e seus objetos.
   tabuleiro.desenha_tudo()
   # pega 'input' do teclado.
   tecla = tabuleiro.janela.getch()
   # pega possível tecla direcional, e converte-a
   # na sua respectiva Direção.
   seta = converte_em_direcoes(tecla)

   # escape da partida.
   if tecla == ord('s') or tecla == ord('S'):
      break

   # uso do teclado para jogar
   if uso_do_teclado:
      if seta is not None:
         tabuleiro.seletor.move(seta)
         local = tabuleiro.seletor.atual
         continue
      elif tecla == KEY_ENTER:
         tabuleiro.coloca_peca(
            jogadores[primeiro],
            tabuleiro.seletor.atual
         )
      ...
   # uso do mouse.
   else:
      # coordenadas do mouse relativo a janela.
      coord = tabuleiro.posicoes()
      try:
         local = tabuleiro.posicao_clicada(coord)
         tabuleiro.coloca_peca(jogadores[primeiro], local)
      except ForaTabuleiroError:
         tabuleiro.informa_algo("fora do tabuleiro!")
         # dá chance a outro clique.
         continue
      except LocalJaPreenchidoError:
         tabuleiro.informa_algo("posição já marcada")
         continue
      ...
   ...

   try:
      # se estiver no primeiro, então adiciona
      # a peça(1), caso contŕario, peça(2).
      if primeiro:
         adiciona_peca(pecas_i, numeracao_em_coord(local))
      else:
         adiciona_peca(pecas_ii, numeracao_em_coord(local))
   except LocalJaPreenchidoError:
      # voltar para o começo do laço, e
      # tentar novamente.
      continue
   ...

   if peca_vitoriosa(pecas_i) or peca_vitoriosa(pecas_ii):
      #tabuleiro.marca_vitoria(fileira_ganha())
      break
   ...

   # obtem evento do mouse/teclado.
   primeiro = (not primeiro)  # alterna de player.
...

# encerra a "interface do curses".
tabuleiro.desmancha_tabuleiro()

# mostra resultado do jogo e demais informações.

if peca_vitoriosa(pecas_i):
   o_vencedor = "\"xis\" GANHOU."
elif peca_vitoriosa(pecas_ii):
   o_vencedor = "\"quadrado\" GANHOU."
else:
   o_vencedor = "jogo EMPATADO."

# cria tela de desenho.
t = tela.Tela(12, 300, grade=False)
# cabeçalho sobre os jogadores.
t.escreve(0, 0, "1º jogador: 'X'\t2º jogador: 'O'")

# desenha o vencedor.
(linha, coluna) = (4, 10)
t.escreve(linha, coluna, o_vencedor)
t.enquadra(
   linha-2, coluna-3,
   altura = 4,
   largura = len(o_vencedor) + 4
)

# screenshot miniaturizado sobre os jogo em geral.
t.escreve(0, 40, "como o jogo terminou:")
tabuleiro_screenshot = tabuleiro_str().split('\n')
while tabuleiro_screenshot.count('') > 0:
   tabuleiro_screenshot.remove('')
arg1 = tabuleiro_screenshot[0]
arg2 = tabuleiro_screenshot[1]
arg3 = tabuleiro_screenshot[2]
arg4 = tabuleiro_screenshot[3]
arg5 = tabuleiro_screenshot[4]
arg6 = tabuleiro_screenshot[5]
arg7 = tabuleiro_screenshot[6]
t.lista_strings(2, 43, arg1, arg2, arg3, arg4, arg5, arg6, arg7)

# risco de divisão do resultado.
t.risca(1, 34, 9, simbolo='|', horizontal=False)

# visualizando tela o resultado geral.
print(t)
# registrando no banco de screenshots do tabuleiro.
resultado_bd = open("dados/resultados.txt", mode="at")
print(t, file=resultado_bd)
