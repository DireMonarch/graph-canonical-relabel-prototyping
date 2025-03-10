import utility
from path_node import path_node
from refiner import mcr, merge_permutation_into_orbit
from permutation import generate_permutation

class canonical_labeler:
    def __init__(self, G):
        self.G = G
        self.prune_automorphisms = True
        self.dl = '0'
        self.tree_size = 0
    
    
    def go(self):
        tree_root = path_node(self.G, None, None, prune_autos=self.prune_automorphisms)
        tree_root.dl = self.dl
        self.best_invar_node = None
        curr = tree_root
        self.automorphisms = []
        
        self.nodes_processed = 0
        self.theta = [[i] for i in range(len(self.G[0]))]
        self.theta_mcr = mcr(self.theta)
        
        while curr is not None:
            curr = curr.process(self.best_invar_node, self.theta_mcr)
            # if curr is not None: curr.visualize()
            self.nodes_processed += 1
            if curr is not None and curr.is_discrete():
                if curr.cmp < 0:
                    self.best_invar_node = curr
                    self.automorphisms = []
                    self.theta = [[i] for i in range(len(self.G[0]))]
                    self.theta_mcr = mcr(self.theta)
                elif curr.cmp == 0:
                    ##   Found an automorphism
                    self.automorphisms.append(curr)
                    self.theta = merge_permutation_into_orbit(generate_permutation(self.best_invar_node.partition, curr.partition), self.theta)
                    self.theta_mcr = mcr(self.theta)
                    
        self.CL = self.best_invar_node.invariant
        self.tree_size = tree_root.size