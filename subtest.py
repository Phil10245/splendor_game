from classes import Ressources, Player

r = Ressources()
r.set_all(6)

k = Ressources()
k["green"]= 7
k.set_red(20)

smmmme = {_: k[_] + r[_] for _ in k }
print(smmmme)
