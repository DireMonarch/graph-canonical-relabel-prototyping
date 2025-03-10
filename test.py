from utility import *
from refiner import is_discrete
from permutation import *


 



g0 = [[0], [1], [2], [3], [4], [5], [6], [7]]
p124 = [[0], [1], [3], [7], [5], [2], [4], [6]]
p128 = [[0], [1], [7], [3], [5], [2], [6], [4]]
p142 = [[0], [3], [1], [7], [5], [4], [2], [6]]
p214 = [[1], [0], [3], [7], [2], [5], [4], [6]]
p356 = [[2], [4], [5], [6], [1], [3], [0], [7]]

perm_g0_p124 = [[3, 2, 5, 4, 6, 7]]
perm_p124_p128 = [[7, 3], [6, 4]]
perm_p124_p142 = [[3, 1], [4, 2]]
perm_p124_p214 = [[1, 0], [2, 5]]
perm_p124_p356 = [[2, 0, 4, 1, 5, 3], [6, 7]]




g1 = [[0], [1], [2], [3], [4], [5], [6], [7]]
pab = [[0], [1], [2], [3], [7], [6], [5], [4]]
pac = [[0], [2], [1], [3], [6], [7], [4], [5]]
pdb = [[3], [1], [2], [0], [5], [4], [7], [6]]


perm_g1_pab = [[7, 4], [6, 5]]
perm_pab_pac = [[2, 1], [6, 7], [4, 5]]
perm_pab_pdb = [[3, 0], [5, 7], [4, 6]]
perm_comb_pac_pdb = [[0,3],[1,2],[4,7],[5,6]]






perm = [[7,3,2],[5,4]]

# ## testing _merge_perm_cells_after_dest_index
# print(perm)
# _merge_perm_cells_after_dest_index(perm, 1, 0, 2)
# print(perm)

## testing generate_permutation
print('\ng0 -> p124')
print(visualize_partition(generate_permutation(g0, p124), '1'))
print(visualize_partition(perm_g0_p124, '1'))

print('\np124 -> p128')
print(visualize_partition(generate_permutation(p124, p128), '1'))
print(visualize_partition(perm_p124_p128, '1'))

print('\np124 -> p142')
print(visualize_partition(generate_permutation(p124, p142), '1'))
print(visualize_partition(perm_p124_p142, '1'))

print('\np124 -> p214')
print(visualize_partition(generate_permutation(p124, p214), '1'))
print(visualize_partition(perm_p124_p214, '1'))

print('\np124 -> p356')
print(visualize_partition(generate_permutation(p124, p356), '1'))
print(visualize_partition(perm_p124_p356, '1'))


print('\ng1 -> pab')
print(visualize_partition(generate_permutation(g1, pab), 'a'))
print(visualize_partition(perm_g1_pab, 'a'))

print('\npab -> pac')
print(visualize_partition(generate_permutation(pab, pac), 'a'))
print(visualize_partition(perm_pab_pac, 'a'))

print('\npab -> pdb')
print(visualize_partition(generate_permutation(pab, pdb), 'a'))
print(visualize_partition(perm_pab_pdb, 'a'))

print('\nComposition pac * pdb')
print(visualize_partition(compose_permutations(perm_pab_pac, perm_pab_pdb, 8), 'a'))
print(visualize_partition(perm_comb_pac_pdb, 'a'))
