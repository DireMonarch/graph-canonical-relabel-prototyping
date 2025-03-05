import copy

from utility import *
from refiner import refine, is_discrete, compare_invariant, first_index_of_non_fixed_cell_of_smallest_size as tc

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
        
        print(f'DEBUG NODE CREATED path: {visualize_path(self.path, self.dl)}  partion: {visualize_partition(self.partition, self.dl)}')
        
        
    def next(self):
        pass
    
    def is_discrete(self):
        return is_discrete(self.partition)
    
    def permutation(self, source=None):
        if not self.is_discrete():
            return []
        
        swaps = []
        if source is None:
            for i, v in enumerate(self.partition):
                if(i != v[0]):
                    if (v[0], i) not in swaps and (i, v[0]) not in swaps:
                        swaps.append((i, v[0]))
        else:
            if not source.is_discrete():
                return []
            for i in range(len(self.partition)):
                if self.partition[i] != source.partition[i]:
                    swap = [source.partition[i][0], self.partition[i][0]]
                    swap.sort()
                    if swap not in swaps:
                        swaps.append(swap)
        swaps.sort()
        return swaps
    
    def _calc_invariant(self):
        perm = self.permutation()
        inv = copy.deepcopy(self.G)
        
        for p in perm:
            # First swap rows #
            temp = inv[p[0]]
            inv[p[0]] = copy.deepcopy(inv[p[1]])
            inv[p[1]] = copy.deepcopy(temp)
            
            # Then swap columns #
            for i in range(len(inv[0])):
                temp = inv[i][p[0]]
                inv[i][p[0]] = inv[i][p[1]]
                inv[i][p[1]] = temp
        return inv
    
    def process_node(self, best_invariant, theta):
        if self.target_cell == -1:
            self.target_cell = tc(self.partition)
            self.W = self.partition[self.target_cell].copy()
        

        
        
        if len(self.W) == 0:
            return self.backup(theta)
        
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
        
        # print(f'\tDEBUG path: {visualize_path(self.branches[self.target_branch].path, self.dl)}  cmp: {self.branches[self.target_branch].cmp}')
        # if self.branches[self.target_branch].path[0]==0:
        #     if best_invariant is not None:
        #         print(f'Best: \n{visualize_graph(best_invariant.invariant, self.dl)}')
        #     else:
        #         print(f'Best: \nNone')
        #     print(f'Curr: \n{visualize_graph(self.branches[self.target_branch].invariant, self.dl)}')
        
        if self.branches[self.target_branch].cmp <= 0:
            return self.branches[self.target_branch]
        
                
        return self
        
    
    def process_leaf(self, theta):
        '''
        Processes a leave node in the tree.
        
        
        --or, and hear me out, it doesn't do any of this--
        Returns a 3-tuple with the following elements:
            the next node in the tree to process (using the backup function)
            a deep copy of the leaf's partition (if it is min??)
            permutation of the current partition, which is an automorphism generator
        '''
        
        return self.backup(theta)
        
    
    def process(self, best_invariant, theta):
        if self.is_discrete():
            return self.process_leaf(theta)
        else:
            return self.process_node(best_invariant, theta)
    
    def backup(self, theta):
        # walk up the tree until we find a parent node that still has values to process i.e. W is not empty
        curr = self        
        while(curr is not None and len(curr.W) == 0):
            # fixes = [curr.fix()]
            curr.target_branch = -1
            curr = curr.parent
            
        # if curr is None, then we are done, otherwise...    
        if curr is not None:
            # find fixes for automorphims in current tree
            fixes = []
            for auto in theta:
                inpath = True
                for i in range(len(curr.path)):
                    if curr.path[i] != auto.path[i]:
                        inpath = False
                        break
                if inpath:
                    current_auto_position = auto
                    while current_auto_position.path != curr.path:
                        fixes.append(current_auto_position.fix())
                        current_auto_position = current_auto_position.parent                        
                # print(f'auto: {visualize_path(auto.path, self.dl)}   curr: {visualize_path(curr.path, self.dl)}  in?  {inpath}')
            curr.prune_automorphisms(fixes)
        return curr
    
    
    # def mcr(self):
    #     value = []
    #     for cell in self.partition:
    #         if len(cell) > 1:
    #             value.append(min(cell))
    #     return value

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

    def prune_automorphisms(self, fixes):
        if self.prune_autos:
            old_W = self.W.copy()
            for fix in fixes:
                self.W = list(set(self.W) & set(fix))
            # print(f'DEBUG PRUNE: {visualize_path(self.path, self.dl)}  Fixes: {visualize_partition(fixes, self.dl)}  old W: {visualize_path(old_W, self.dl)}  W: {visualize_path(self.W, self.dl)}')

    
    # def fixes(self):
    #     value = [self.fix()]
    #     if self.parent is not None:
    #         value = self.parent.fixes() + value
    #     return value
    
    def visualize(self):

        print(f'\n{visualize_path(self.path, self.dl)}')
        print(f'\tPartition: {visualize_partition(self.partition, self.dl)}')
        # print(self.levelast_hop_from_parent)
        # print(f'\tLevel = {self.level},  Path: {path},  cmp: {self.cmp}')
        # print(f'\tW: {self.W}')
        # print(f'\tBest Invariant: {self.best_invariant}')
        # print(f'\tChildren Generated: {list(self.branches.keys())}')
        print(f'\tPermutation: {visualize_partition(self.permutation(), self.dl)}')
        print('')


