
__DEBUG__ = False

def is_discrete(pi):
    '''Returns true of all cells in pi are length 1, otherwise returns False'''
    for cell in pi:
        if len(cell) > 1:
            return False
    return True

def scoped_degree(G, scope, v):
    '''
    Returns the degree of vertex v with respect to the verticies in scope
    
    parameters:
        G       the graph's adjacency matrix
        scope   the scope of vertices with which to calculate the degree
        v       the vertex on which we are calculating the degree
        
    returns an integer value of the degree of v with respect to scope over graph G
    '''
    
    d = 0
    for s in scope:
        d += G[v][s]
    return d


def partition_by_scoped_degree(G, scope, cell):
    '''
    splits (partitions) cell into a smaller cells, grouped by their scoped degree
    with respect to scope, and numerically sorted by the value of their degree
        
    parameters:
        G       the graph's adjacency matrix
        scope   the scope of vertices with which to calculate the degree
        cell    the cell we are splitting
    
    returns a list containing the new cells
    '''
    hash_table = {}
    for v in cell:
        degree = scoped_degree(G, scope, v)
        if degree not in hash_table:
            hash_table[degree] = []
        hash_table[degree].append(v)
    return [sorted(hash_table[i]) for i in sorted(hash_table.keys())]


def first_index_of_max_cell_size_of_partition(partition):
    '''
    Finds the largest cell size in partition, and returns the index of the first
    occurrence of a cell of that size
    '''
    
    max = 0
    idx = 0
    for i, cell in enumerate(partition):
        if len(cell) > max:
            max = len(cell)
            idx = i
    return idx


def refine(G, pi, set):
    pi_hat = pi.copy()  # Version of pi that is being refined, the result #
    alpha = set.copy()
    a = 0  # Alpha index varaible, was m in the paper #
    
    if __DEBUG__: print(f'pi: {pi},  alpha: {alpha}')
    while a < len(alpha) and not is_discrete(pi_hat):
        refine_scope_cell = alpha[a]  # refine_scope_cell was W in the paper #
        if __DEBUG__: print(f'\n\n\nStarting Outer Loop:  pi_hat {pi_hat},  alpha {alpha}, a {a}, refine_scope_cell {refine_scope_cell}')
        p = 0  # pi_hat index variable, was k in the paper #
        while p < len(pi_hat):
            cell = pi_hat[p] # current cell we are partitioning, was V/V_k in the paper #
            pi_local = partition_by_scoped_degree(G, refine_scope_cell, cell)
            if __DEBUG__: print('\np', p, 'a', a, "refine scope", refine_scope_cell, 'cell', cell, 'pi_local', pi_local)
            if __DEBUG__: print('pi_local', pi_local)
            if len(pi_local) == 1:
                p += 1
            else:
                t = first_index_of_max_cell_size_of_partition(pi_local)
                if __DEBUG__: print(f't = {t}   a = {a}   cell = {cell}   alpha = {alpha}')
                if cell in alpha:
                    i = alpha.index(cell)
                    alpha[i] = pi_local[t]
                    if __DEBUG__: print(f'\tupdating alpha = {alpha}')
                    
                    for i in range(len(pi_local)):
                        if i != t:
                            alpha.append(pi_local[i])
                            if __DEBUG__: print(f'\tappending cell was in alpha, i != t {i} != {t}, new alpha = {alpha}')
                
                else:
                    for i in range(len(pi_local)):
                        alpha.append(pi_local[i])
                        if __DEBUG__: print(f'\tappending cell not in alpha, i = {i} new alpha = {alpha}')
                
                    
                    
                if __DEBUG__: print(f'pi_hat = {pi_hat},   alpha = {alpha}')
                pi_hat = pi_hat[:p] + pi_local + pi_hat[p+1:]
                if __DEBUG__: print(f'pi_local = {pi_local}')
                if __DEBUG__: print(f'pi_hat = {pi_hat}\n')
        a += 1
    return pi_hat


def first_index_of_non_fixed_cell_of_smallest_size(partition):
    '''
    Finds the smallest cell size > 1, and returns the index of the first instance
    of a cell of that size in partition
    '''
    smallest = -1
    idx = -1
    for i, cell in enumerate(partition):
        if len(cell) == 2:
            return i
        if len(cell) > smallest:
            smallest = len(cell)
            idx = i
    return idx


def compare_invariant(a, b):
    for r in range(len(a)):
        for c in range(len(a[r])):
            if a[r][c] != b[r][c]:
                # print(f'first differes at ({r}, {c}).')
                return -1 if a[r][c] < b[r][c] else 1
    return 0


