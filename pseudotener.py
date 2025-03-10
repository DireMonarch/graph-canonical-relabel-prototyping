import sys
from utility import *
import json
# from path_node import path_node
# from refiner import compare_invariant
from canonical_labeler import canonical_labeler
from permutation import generate_permutation

# curr = path_node(None)




# def canonical_labeling(G, pi, tc, I):
#     curr.partition = refine(G, )
    

def usage():
    print(f'Usage:\n\n{sys.argv[0]} graph-json-filename')
    print('\tOptions:')
    print('\t--label C    Where C is any character to start labelling at')
    print('\t--skip-prunning    if set, automormorphisms won\'t be pruned from the tree')
    exit(-1)
    
    
def main():
    if len(sys.argv) < 2:
        usage()
    
    filename = sys.argv[1]
    with open(filename, 'r') as infile:
        G = json.load(infile)
    
    # print(visualize_graph(G, '1'))
    
    labeler = canonical_labeler(G)
    if '--label' in sys.argv:
        i = sys.argv.index('--label')
        if len(sys.argv) < i+2:
            usage()
        dl = sys.argv[i+1]
        if len(dl) != 1:
            usage()
        labeler.dl = dl
        
    if '--skip-pruning' in sys.argv:
        labeler.prune_automorphisms = False
        
    labeler.go()
    
    node_with_best_invariant = labeler.best_invar_node
    
    print(f'\nCanonical Label:  Path: {visualize_path(node_with_best_invariant.path, labeler.dl)}   Permutation: {visualize_partition(node_with_best_invariant.get_permutation(), labeler.dl)}')
        
    for auto in labeler.automorphisms:
        print(f'Automorphism:  Path: {visualize_path(auto.path, labeler.dl)}  Auto Generator: {visualize_partition( generate_permutation(node_with_best_invariant.partition, auto.partition), labeler.dl)}')

    print(f'Number of Nodes in Tree: {labeler.tree_size}   Total Processing Steps: {labeler.nodes_processed}')
    
 
if __name__ == '__main__':
    main()