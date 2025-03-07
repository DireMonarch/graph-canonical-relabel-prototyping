import copy

from utility import *
from refiner import refine, is_discrete, compare_invariant, mcr, first_index_of_non_fixed_cell_of_smallest_size as tc

class path_node:
    def __init__(self, G, parent, last_hop, prune_autos=True):
        self.G = G
        parent_part = [list(range(len(G[0])))] if parent is None else parent.partition
        refine_against = parent_part.copy() if parent is None else [[last_hop]]
        self.partition = refine(G, parent_part,refine_against)
        self.W = []  # set of unused branch keys
        self.parent = parent
        self.target_cell = -1
        self.target_branch = -1
        self.branches = {}
        self.level = 0 if parent is None else parent.level + 1
        self.last_hop_from_parent = last_hop
        self.cmp = None
        self.invariant = self._calc_invariant()
        
        self.path = parent.path + [self.last_hop_from_parent] if parent is not None else []

        self.dl = parent.dl if parent is not None else '0'  # Variable used as the starting display label
        self.prune_autos = prune_autos  # Normally set to true, set to false to skip pruning automorphisms for testing
        
        self.size = 1
        curr = self.parent
        while curr is not None:
            curr.size += 1
            curr = curr.parent
        
        self.debug = False
        
        if self.debug: print(f'C {visualize_path(self.path, self.dl)}  partion: {visualize_partition(self.partition, self.dl)}  cmp: {self.cmp}')
        

        
    
    def is_discrete(self):
        return is_discrete(self.partition)
    
    def permutation(self, source=None, debug=False):
        if not self.is_discrete():
            return []
        
        if source is not None and not source.is_discrete():
            return []
        
        source_partition = source.partition if source is not None else [[i] for i in range(len(self.partition))]
        
        # Get pairwise swaps that don't really work, need to be combined
        swaps = []

        for i in range(len(self.partition)):
            if self.partition[i] != source_partition[i]:
                swap = [self.partition[i][0], source_partition[i][0]]
                if swap not in swaps and [swap[1], swap[0]] not in swaps:
                    swaps.append(swap)

        # Combine:

        perm = []
        curr_cell =[]
        while len(swaps) > 0:
            if len(curr_cell) == 0:
                ## Cell is empty, grab next cell from swaps
                curr_cell = swaps.pop(0)
            else:
                ## Cell is not empty, look for another cell in swaps that starts the last elemnt of cell
                found_next = None
                for swap_cell in swaps:
                    if curr_cell[-1] == swap_cell[0]:
                        found_next = swap_cell
                        break
                if found_next != None:
                    if curr_cell[0] == found_next[1]:
                        ## if we are here, then we found the end of the cycle
                        perm.append(curr_cell)
                        curr_cell = []
                    else:
                        curr_cell.append(found_next[1])   # add the next step to curr cell
                    swaps.remove(found_next)  # remove the found cell from swaps
                else:
                    perm.append(curr_cell)  #if we are here, we didn't find another cell in the chain
                    curr_cell = [] # Start a new cell for next round
        if len(curr_cell) > 0:
            perm.append(curr_cell)
            
            
        return perm       
        
    
    def _calc_invariant(self):
        perm = self.permutation()
        inv = copy.deepcopy(self.G)
                       
        for p in perm:
            if len(p) > 1:
                di = p[0]
                for si in p[1:]:
                    # First swap rows #
                    temp = inv[di]
                    inv[di] = inv[si]
                    inv[si] = temp
                    
                    # Then swap columns #
                    for i in range(len(inv[0])):
                        temp = inv[i][di]
                        inv[i][di] = inv[i][si]
                        inv[i][si] = temp            
                
                
        return inv


    def process(self, best_invariant, theta):
        if self.is_discrete():
            return self.process_leaf(best_invariant, theta)
        else:
            return self.process_node(best_invariant, theta)
        
            
    def process_node(self, best_invariant, theta_mcr):
        if self.debug: print(f'P {visualize_path(self.path, self.dl)}  tc {self.target_cell}, {visualize_path(self.partition[self.target_cell], self.dl) if self.target_cell > -1 else []}   W {visualize_path(self.W, self.dl)}')
        if self.target_cell == -1:
            self.target_cell = tc(self.partition)
            self.W = self.partition[self.target_cell].copy()
        
        ## PRUNE
        
        # W = list(set(self.W) & set(mcr(theta)))
        # if W != self.W:
        #     if self.debug: print(f'R {visualize_path(self.path, self.dl)}  OLD: {visualize_path(self.W, self.dl)}  NEW: {visualize_path(W, self.dl)}')
        #     self.W = W
        
        if len(self.W) == 0:
            return self.backtrack(theta_mcr)
        
        self.target_branch = min(self.W)
        self.W.remove(self.target_branch)
        
        self.branches[self.target_branch] = path_node(self.G, self, self.target_branch, prune_autos=self.prune_autos)
        # self.branches[self.target_branch].cmp = compare_invariant(self.branches[self.target_branch].invariant(), self.invariant())
        if self.branches[self.target_branch].is_discrete():
            if best_invariant is None:
                self.branches[self.target_branch].cmp = -1
            else:
                self.branches[self.target_branch].cmp = compare_invariant(self.branches[self.target_branch].invariant, best_invariant.invariant)
        else:
            self.branches[self.target_branch].cmp = 0
        
        if self.branches[self.target_branch].cmp <= 0:
            return self.branches[self.target_branch]
        
                
        return self
        
    
    def process_leaf(self, best_invariant, theta_mcr):
        '''
        Processes a leave node in the tree.
        
        
        --or, and hear me out, it doesn't do any of this--
        Returns a 3-tuple with the following elements:
            the next node in the tree to process (using the backup function)
            a deep copy of the leaf's partition (if it is min??)
            permutation of the current partition, which is an automorphism generator
        '''
        
        to = None if self.cmp == -1 else self.greatest_common_ancestor(best_invariant)
        # if self.debug: print(f'T {visualize_path(self.path, self.dl)}  CMP: {self.cmp}   BI: {visualize_path(best_invariant.path, self.dl)}  TO: {visualize_path(to, self.dl)}')
        
        return self.backtrack(theta_mcr, to)
        
    
    def greatest_common_ancestor(self, other_node):
        gca = []
        for i in range(min(len(self.path), len(other_node.path))):
            if self.path[i] == other_node.path[i]:
                gca.append(self.path[i])
            else:
                return gca
        return gca
    
    
    def backtrack(self, theta_mcr, to_path=None):
        # # walk up the tree until we find a parent node that still has values to process i.e. W is not empty
        # curr = self        
        # while(curr is not None and len(curr.W) == 0):
        #     # fixes = [curr.fix()]
        #     curr.target_branch = -1
        #     curr = curr.parent
            
        # # if curr is None, then we are done, otherwise...    
        # if curr is not None:
        #     # find fixes for automorphims in current tree
        #     mcrs = []
        #     for auto in theta:
        #         amcr = []
        #         inpath = True
        #         for i in range(len(curr.path)):
        #             if curr.path[i] != auto.path[i]:
        #                 inpath = False
        #                 break
        #         if inpath:
        #             # current_auto_position = auto
        #             # while current_auto_position.path != curr.path:
        #             #     fixes.append(current_auto_position.fix())   # swapping to new mcr...
        #             #     # fixes.append(current_auto_position.mcr())
        #             #     current_auto_position = current_auto_position.parent   
        #             amcr = mcr(auto.permutation(best_invariant))
        #             mcrs.append(amcr)
        #         if self.debug: print(f'A {visualize_path(auto.path, self.dl)}   curr: {visualize_path(curr.path, self.dl)}  in?  {inpath}   mcr:  {visualize_path(amcr, self.dl)}')
        #     curr.prune_automorphisms(mcrs)
        if to_path is None:
            if self.debug: print(f'B {visualize_path(self.path, self.dl)}   to: PARENT')
            if self.parent is not None:
                self.parent.prune_automorphisms(theta_mcr)
            return self.parent
        
        if self.debug: print(f'B {visualize_path(self.path, self.dl)}   to: {visualize_path(to_path, self.dl)}')
        curr = self
        while curr is not None and curr.path != to_path:
            curr = curr.parent
        if curr is not None:
            curr.prune_automorphisms(theta_mcr)
        return curr
    
    
    def mcr(self):
        value = []
        for cell in self.partition:
            value.append(min(cell))
        return value

    # def mcrs(self):
    #     value =[self.mcr()]
    #     curr = self.parent
    #     while curr is not None:
    #         value.insert(0, curr.mcr())
    #         curr = curr.parent
    #     return value
    
    def fix(self):
        value = []
        for cell in self.partition:
            if len(cell) == 1:
                value.append(cell[0])
        return value

    def prune_automorphisms(self, theta_mcr):
        if self.prune_autos:
            old_W = self.W.copy()
            self.W = list(set(self.W) & set(theta_mcr))
            if self.debug: print(f'P {visualize_path(self.path, self.dl)}   MCR: {visualize_path(theta_mcr, self.dl)}  old W: {visualize_path(old_W, self.dl)}  W: {visualize_path(self.W, self.dl)}')

    
    # def fixes(self):
    #     value = [self.fix()]
    #     if self.parent is not None:
    #         value = self.parent.fixes() + value
    #     return value
    
    def visualize(self):
        cmp = self.cmp if self.is_discrete() else '-'
        print(f'V {visualize_path(self.path, self.dl)}  partion: {visualize_partition(self.partition, self.dl)}  cmp: {cmp}')
        # if cmp in [-1, 0]:
        #     print(f'{visualize_partition(self.permutation(), self.dl)}')
        #     print(f'{visualize_graph(self.invariant, self.dl)}')

        # print(f'\n{visualize_path(self.path, self.dl)}')
        # print(f'\tPartition: {visualize_partition(self.partition, self.dl)}')
        # # print(self.levelast_hop_from_parent)
        # # print(f'\tLevel = {self.level},  Path: {path},  cmp: {self.cmp}')
        # # print(f'\tW: {self.W}')
        # # print(f'\tBest Invariant: {self.best_invariant}')
        # # print(f'\tChildren Generated: {list(self.branches.keys())}')
        # print(f'\tPermutation: {visualize_partition(self.permutation(), self.dl)}')
        # print('')


