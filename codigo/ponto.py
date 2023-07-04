
# outro nome para o mesmo objeto.
class Ponto:
   "representação do 'Ponto', posições (y, x)"
   def __init__(self, vertical, horizontal):
      self._y = vertical
      self._x = horizontal
   ...
   def __str__(self):
      return "({}, {})".format(self._y, self._x)
   def __add__(self, ponto):
      if not isinstance(ponto, Ponto):
         raise ValueError("'%s' não é do tipo 'Ponto'" % type(ponto))
      return Ponto(self._y + ponto.y, self._x + ponto.x)
   def __sub__(self, ponto):
      if not isinstance(ponto, Ponto):
         raise ValueError("'%s' não é do tipo 'Ponto'" % type(ponto))
      return Ponto(self._y - ponto.y, self._x - ponto.x)
   ...
   # só delega as funções acimas que já fazem
   # quase todo o trabalho.
   def __iadd__(self, ponto):
      return self + ponto
   def __isub__(self, ponto):
      return self - ponto
   # encapsulamento ...
   def valor_x(self):
      return self._x
   def valor_y(self):
      return self._y
   x = property(valor_x, doc="coordenada X(horizontal)")
   y = property(valor_y, doc="coordenada Y(vertical)")
...
