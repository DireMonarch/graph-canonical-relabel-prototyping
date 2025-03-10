
from refiner import is_discrete
import copy

def _index_of_perm_cell_containing_vertex(perm, v):
    for i in range(len(perm)):
        if v in perm[i]:
            return i
    return -1

def _merge_perm_cells_after_dest_index(perm, src_cell_idx, dst_cell_idx, insert_idx):
    perm[dst_cell_idx] = perm[dst_cell_idx][0:insert_idx+1] + perm[src_cell_idx] + perm[dst_cell_idx][insert_idx+1:]
    perm.pop(src_cell_idx)

def generate_permutation(source_part, dest_part):
    if not is_discrete(source_part) or not is_discrete(dest_part):
        return []
        
    perm = []
    
    for i in range(len(source_part)):
        src_vert = source_part[i][0]
        dst_vert = dest_part[i][0]
        if src_vert != dst_vert:
            ## vertices are different, need to add to permutation
            src_idx = _index_of_perm_cell_containing_vertex(perm, src_vert)
            dst_idx = _index_of_perm_cell_containing_vertex(perm, dst_vert)
            if src_idx == -1 and dst_idx == -1:
                ## neither vertex is in permutation, add new cell
                perm.append([dst_vert, src_vert])  # This order matters, always destiation first!!!
            elif src_idx > -1 and dst_idx > -1:
                if src_idx != dst_idx:  ## only run this section if the vertices are in differnt cells
                    ## both vertices in permutation, merge two cells
                    j = perm[dst_idx].index(dst_vert)
                    _merge_perm_cells_after_dest_index(perm, src_idx, dst_idx, i)
            else:
                ## Only one vertex is in permutation, add the other
                if src_idx > -1:
                    ## source vertex is in permutation, add destination vertex before source vertex
                    j = perm[src_idx].index(src_vert)
                    perm[src_idx].insert(j, dst_vert)
                else:
                    ##  destination vertex is in permutation, add source vertex after destination vertex
                    j = perm[dst_idx].index(dst_vert)
                    perm[dst_idx].insert(j+1, src_vert)
            
        
    return perm 




def _permutate_partition(part, perm):
    result = copy.deepcopy(part)
                    
    for p in perm:
        if len(p) > 1:
            di = p[0]
            for si in p[1:]:
                temp = result[di]
                result[di] = result[si]
                result[si] = temp
    return result



def compose_permutations(perm1, perm2, partition_length):
    # print('perm1', perm1)
    start = [[i] for i in range(partition_length)]
    # print('start', start)
    curr = _permutate_partition(start, perm1)
    # print('perm1(start)', curr)
    curr = _permutate_partition(curr, perm2)
    # print('perm2(curr)', curr)
    
    # print(start, curr)
    return generate_permutation(start, curr)