from copy import deepcopy
from classes import Player


pla1 = Player("P", 1)
pla2 = Player("p", 1)

old_lst = [pla1, pla2]
new_lst = deepcopy(old_lst)
new_lst.pop(0)
print(new_lst)