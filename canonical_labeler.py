import utility
from path_node import path_node
from refiner import compare_invariant

class canonical_labeler:
    def __init__(self, G):
        self.G = G
        self.prune_automorphisms = True
        self.dl = '0'
        self.tree_size = 0
    
    
    def go(self):
        tree_root = path_node(self.G, None, None, prune_autos=self.prune_automorphisms)
        tree_root.dl = self.dl
        # self.best_invar_node = tree_root
        self.best_invar_node = None
        curr = tree_root
        self.automorphisms = []
        
        self.nodes_processed = 0
        
        theta = []
        
        while curr is not None:
            curr = curr.process(self.best_invar_node, theta)
            self.nodes_processed += 1
            if curr is not None and curr.is_discrete():
                if curr.cmp < 0:
                    self.best_invar_node = curr
                    self.automorphisms = []
                    theta = [curr]
                elif curr.cmp == 0:
                    self.automorphisms.append(curr)
                    theta.append(curr)
                    
        self.CL = self.best_invar_node.invariant
        self.tree_size = tree_root.size