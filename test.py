from refiner import merge_permutation_into_orbit
from utility import *



theta = [[i] for i in range(8)]
o2 = [[3, 7], [4, 6]]

print('th', visualize_partition(theta, "1"), '\n')
print('o2', visualize_partition(o2, "1"))


theta = merge_permutation_into_orbit(o2, theta)
print('th', visualize_partition(theta, "1"), '\n')

o3 = [[1, 3], [2, 4]]
print('o3', visualize_partition(o3, "1"))

theta = merge_permutation_into_orbit(o3, theta)
print('th', visualize_partition(theta, "1"), '\n')


o4 = [[0, 1], [2, 5]]
print('o4', visualize_partition(o4, "1"))

theta = merge_permutation_into_orbit(o4, theta)
print('th', visualize_partition(theta, "1"), '\n')


o5 = [[0, 1, 2, 3, 4, 5], [6, 7]]
print('o4', visualize_partition(o5, "1"))

theta = merge_permutation_into_orbit(o5, theta)
print('th', visualize_partition(theta, "1"), '\n')
