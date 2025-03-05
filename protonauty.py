

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


def pop_vertex_from_cell_in_partition(partition, v):
    '''
    Pulls vertex from a cell in the partition
    
    parameters:
        partition   partition to operate on
        v           vertex to pop
    
    returns new partition with v popped to its own cell before the cell that
    it was in
    '''
    new_part = []
    for cell in partition:
        new_cell = cell.copy()
        if v in cell:
            if len(new_cell) == 1:
                return partition.copy()
            new_part.append([v])
            new_cell.remove(v)
            new_part.append(new_cell)
        else:
            new_part.append(new_cell)
    return new_part


def refine(G, pi, alpha):
    # print(f'pi: {pi},  alpha: {alpha}')
    pi_hat = pi.copy()  # Version of pi that is being refined, the result #
    a = 0  # Alpha index varaible, was m in the paper #
    
    while a < len(alpha) and not is_discrete(pi_hat):
        refine_scope_cell = alpha[a]  # refine_scope_cell was W in the paper #
        a += 1
        p = 0  # pi_hat index variable, was k in the paper #
        while p < len(pi_hat):
            cell = pi_hat[p] # current cell we are partitioning, was V/V_k in the paper #
            pi_local = partition_by_scoped_degree(G, refine_scope_cell, cell)
            # print('\np', p, 'a', a, "refine scope", refine_scope_cell, 'cell', cell, 'pi_local', pi_local)
            # print('pi_local', pi_local)
            if len(pi_local) == 1:
                p += 1
            else:
                t = first_index_of_max_cell_size_of_partition(pi_local)
                # print(f't = {t}   a = {a}   cell = {cell}   alpha = {alpha}')
                if cell in alpha:
                    i = alpha.index(cell)
                    alpha[i] = pi_local[t]
                for i in range(t):
                    alpha.append(pi_local[i])
                for i in range(t+1, len(pi_local)):
                    alpha.append(pi_local[i])
                # print(f'pi_hat = {pi_hat},   alpha = {alpha}')
                pi_hat = pi_hat[:p] + pi_local + pi_hat[p+1:]
                # print(f'pi_local = {pi_local}')
                # print(f'pi_hat = {pi_hat}\n')
                p += 1
    return pi_hat


def search_tree(G):
    V = [list(range(len(G[0])))]
    pi = V.copy()
    pis = {0:refine(G, pi, V)}
    p = 0  # pi_hat index variable, was k in the paper #
    store = {}
    print(f'Start: {pi}')
    count = 0
    while p >= 0:
        # print(f'\n<BEG> p: {p}   pi: {pis[p]}   store: {store}')
        if is_discrete(pis[p]):
            print(f'Terminal Node: {pis[p]}     Tree:  {pis}')
            count += 1
            p -= 1
            if p < 0:
                break
        else:
            store[p] = pis[p][first_index_of_non_fixed_cell_of_smallest_size(pis[p])].copy()
            # print(f'<FIN> p: {p}   pi: {pis[p]}   store: {store}')
        
        end = False
        while len(store[p]) ==  0:
            p -= 1
            if p < 0:
                end = True
                break
        if end:
            break
        
        v = min(store[p])
        store[p].remove(v)
        pv = pop_vertex_from_cell_in_partition(pis[p], v)
        # print(f'Before Refinement:  popped: {pv}  v {v}')
        pis[p+1] = refine(G, pv, [[v]])
        # print(f'Refined against {v} : {pis[p+1]}')
        # print(f'<MID> p+1: {p+1}   pi: {pis[p+1]}   store: {store.get(p, [])}')
        
        p += 1

    print(f'Terminal Node Count = {count}')
    return pis, store

def main():
    G1 = [
        [0, 1, 0, 0, 1],
        [1, 0, 1, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0]
        ]
    # pi = [list(range(len(G1[0])))]
    # alpha = [list(range(len(G1[0])))]
    # print(f'pi = {pi}, discrete = {is_discrete(pi)}')
    # print(f'alpha = {alpha}, discrete = {is_discrete(alpha)}')
    
    # # print(scoped_degree(G1, alpha[0], 1))
    
    # # print(partition_by_scoped_degree(G1, alpha[0], pi[0]))
    # # print(first_index_of_max_cell_size_of_partition(partition_by_scoped_degree(G1, alpha[0], pi[0])))
    
    
    
    
    # print('refine G1: ', refine(G1, pi, alpha))
    
    G2 = [
        [0,0,1,0,1,0,1,0],
        [0,0,0,0,1,1,1,0],
        [1,0,0,1,0,0,0,1],
        [0,0,1,0,0,1,1,0],
        [1,1,0,0,0,0,0,1],
        [0,1,0,1,0,0,0,1],
        [1,1,0,1,0,0,0,0],
        [0,0,1,0,1,1,0,0]
    ]
    
    # pi = [list(range(len(G2[0])))]
    # alpha = [list(range(len(G2[0])))]
    # print('refine G2: ', refine(G2, pi, alpha))
    # print('refine G2: ', refine(G2, pi, [[0]]))  #Not sure if this is returning out of order, or if the example is wrong!!
    
    # pi = [[5], [1, 3, 7], [0], [2, 4, 6]]
    v = 1
    # print(pop_vertex_from_cell_in_partition(pi, v))
    # print(refine(G2, pop_vertex_from_cell_in_partition(pi, v), [[v]]))


    G3 = [
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1],
        [1,0,0,0]
    ]

    print(search_tree(G3))

if __name__ == '__main__':
    main()