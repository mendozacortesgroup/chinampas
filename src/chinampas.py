#Authors: Luke Van Popering, Eric Dolores Cuenca and Antonio Arciniega-Nevarez. 
import copy
import numpy as np
import abc

class PrimaryVertex(object):
    '''
    Stores attributes for primary vertices.

    :param position: Position of primary vertex.
    :type position: int

    :param time: Activation time of primary vertex.
    :type time: int
    '''
    def __init__(self,position : int,time : int):

        self.position = position
        self.time = time

    def __eq__(self,other):
        if isinstance(other,PrimaryVertex):
          if self.time == other.time and self.position == other.position:
              return True
        else: return False


class Pyramid(object):
    def __init__(self,lP,rP,time):
        '''
        Stores attributes for pyramids.

        :param lP: Left vertex of pyramid.
        :type lP: int

        :param rP: Right vertex of pyramid.
        :type rP: int

        :param time: Activation time of pyramid "base".
        :param time: int
        '''
        self.lP,self.rP = lP,rP
        self.time = time

class Chinampa(abc.ABC):
    @abc.abstractmethod
    def __len__(self): return

    @abc.abstractmethod
    def will_vertex_be_activated(self,n : int,t_0 : int): return

    @abc.abstractmethod
    def when_will_vertex_be_activated(self,n : int): return
    
 
class Chain_Chinampa(Chinampa):
    def __init__(self,activations : list, sorted = True):
        '''
        Model of "chinampa" cascade within a chain.
        :param activations: Nested list of primary vertex (PV) positions and activation 
                            times.
        :type activations: list[list[int]]

        :param sorted: Optional. If True, we assume [activations] 
                            to be sorted by time and position.
        :type sorted: bool

        :Example: Chain_Chinampa([[0,0],[1,0],[2,1],[3,1],[1,2]]) defines the
                            chain with PVs 0 and 1 at time 0, PVs 2 and 3 at time 1, and PV
                            1 at time 2.
        '''
        if not sorted:
            activations = sorted(activations,key = lambda x: (x[1],x[0]))

        self.PVList = [PrimaryVertex(PV[0],PV[1]) for PV in activations]
        self.lV = min([self.PVList[idx].position for idx in range(len(self.PVList))])
        self.rV = max([self.PVList[idx].position for idx in range(len(self.PVList))])

    def __len__(self):
        ''' 
        Returns length of chain. 
        :rtype: int
        '''
        return self.rV - self.lV
        
    def reset_pryamids(self):
        ''' Resets and reconstructs pyramids. '''
        self.pyramids = self.build_Pyramids()

    def will_vertex_be_activated(self,n : int,t_0 : int):
        '''
        Returns whether vertex [n] will be active at time [t_0].
    
        :type n: int
        :type t_0: int

        :rtype: bool
        '''
        for vertex in self.PVList:
          if vertex.time == t_0 and vertex.position == n: return True;

        if not hasattr(self,'pyramids'):
            self.pyramids = self.build_Pyramids()

        for pyramid in self.pyramids:
          dT = t_0 - pyramid.time
          offset = n - pyramid.lP
          if dT <= offset and n <= pyramid.rP:
              if pyramid.time <= t_0 and t_0 <= offset + pyramid.time:
                  return True
          elif pyramid.time > t_0: break
        return False

    def when_will_vertex_be_activated(self,n : int):
        '''
        Returns the list of times for which vertex [n] will be active.
        
        :type n: int

        :rtype: list[int]
        '''
        times = []
        if not hasattr(self,'pyramids'):
            self.pyramids = self.build_Pyramids()

        for pyramid in self.pyramids:
          offset = n - pyramid.lP
          if pyramid.lP <= n and n <= pyramid.rP:
              times.extend(list(range(pyramid.time,pyramid.time+offset+1)))
        return times

    def remove_Duplicates(self,listOfPyramids):
        ''' 
        Merge adjacent pyramids.

        :type listOfPyramids: List[Pyramid].

        :return: List of non-adjacent pyramids.
        :rtype: list[Pyramid]
        '''
        dynamic_copy = copy.deepcopy(listOfPyramids)
        previous = dynamic_copy[0]
        index = 0
        for walker in listOfPyramids[1::]:
            if previous.rP==walker.lP - 1 and previous.time == walker.time:
                previous.rP = walker.rP
                dynamic_copy = dynamic_copy[:index] + dynamic_copy[idx+1::]
            else:
                previous = dynamic_copy[index]
                index += 1
        return dynamic_copy

    def build_Pyramids(self):
        '''
        Construct pyramids determined by the provided PVs.

        :return: List of pyramids.
        :rtype: list[Pyramid]
        '''
        r_index = []
        for idx,PV in enumerate(self.PVList[:-1]):
            for jdx,inner_PV in enumerate(self.PVList[idx+1::]):
                if PV == inner_PV: r_index.append(jdx+idx+1)
        self.PVList = [PV for idx,PV in enumerate(self.PVList) if idx not in r_index]


        listOfPyramids = []
        pyramid = Pyramid(self.PVList[0].position,self.PVList[0].position,self.PVList[0].time)
        
        for vertex in self.PVList[1::]:
            if vertex.time == pyramid.time and vertex.position == pyramid.rP + 1:
                pyramid.rP = vertex.position
            else:
                listOfPyramids.append(pyramid)
                pyramid = Pyramid(vertex.position,vertex.position,vertex.time)

        listOfPyramids.append(pyramid)
        pastPyramids = copy.copy(listOfPyramids)

       
        for pyramid in listOfPyramids:
            r_index = []
            width = pyramid.rP - pyramid.lP
            for idx,lower_pyramid in enumerate(pastPyramids):
                dT = pyramid.time - lower_pyramid.time
                lower_width = lower_pyramid.rP - lower_pyramid.lP
                if  lower_width < dT:
                    r_index.append(idx)
                elif dT + width < 0: break;
                elif pyramid.lP == lower_pyramid.rP + 1:
                    pyramid.lP = lower_pyramid.lP + dT 
                elif pyramid.rP == lower_pyramid.lP + dT - 1:
                    pyramid.rP = lower_pyramid.rP
            pastPyramids = [p for idx,p in enumerate(pastPyramids) if idx not in r_index]
        return self.remove_Duplicates(listOfPyramids)
      
      
class Tree_Chinampa(Chinampa):
    def __init__(self,chain_idx, activations : dict, parent = (None,None)):
        '''
        Model of "chinampa" cascade within tree structure.

        :param chain_idx: Index of current chain within tree
        :type chain_idx: int

        :param activations: Maps [chain_idx] to dict containing 1) nested list of 
                            primary vertex positions and activation times and 2) list 
                            of branches. Assumed to be sorted. See example.
        :type activations:  dict{int:{str:list[list],str:dict{int:int}}}

        :param parent: Optional. Tuple of self.chain attribute and [chain_idx] of parent chain.
        :type parent: tuple(Chain_Chinampa,int)

        :example: TD_Tree_Chinampa(0,{0:{'activations':[[3,0],[4,0]],'branches':[1,2]},
                                        1:{'activations':[[0,0],[1,0]],'branches':{}},
                                        2:{'activations':[[2,0]],'branches':{}}
                                        }
                                   )
                            defines a tree wherein we have
                                 a. PVs 3 and 4 at time 0 within 
                                    chain 0.
                                 b. PVs 0 and 1 at time 0 within 
                                    chain 1. 
                                 c. PV 2 at time 0 within chain 2. 
                                 
                            Chain 0 is connected to chain 1 via vertex 1 -> vertex 3,
                            and also to chain 2 via vertex 2 -> vertex 3.

        '''

        self.chain = Chain_Chinampa(activations[chain_idx]['activations'])

        self.parent = parent[0]
        self.parent_index = parent[1]

        self.branches = []
        for branch_idx in activations[chain_idx].get('branches',{}):
            self.branches.append(Tree_Chinampa(branch_idx,activations,
                                        (self.chain,chain_idx)))

    def __len__(self):
        ''' 
        Return # of vertices in tree.

        :rtype: int
        '''
        return max([self.chain.rV] + [len(branch) for branch in self.branches])

    def select_branch(self,n):
        '''
        Given a vertex [n], determine which branch it is located in.

        :param n:
        :type n: int

        :return: Index of branch containing [n].
        :rtype: int or NoneType
        '''
        branch_rVs = [branch.chain.rV for branch in self.branches]
        for idx,branch in enumerate(self.branches):
            if self.chain.rV > n and n <= len(branch):
                return idx
        return None

    def extend_chain(self):
        '''
        Add overlapping PVs of self.branches to self.chain.
        '''

        if not hasattr(self,'extended'):
            branch_times = []
            for branch in self.branches:
                times = self.when_will_vertex_be_activated(branch.chain.rV)
                
                for time in times:
                    if time in branch_times: 
                      self.chain.PVList.append(PrimaryVertex(self.chain.lV,time+1))
                    else:
                      self.chain.PVList.append(PrimaryVertex(self.chain.lV - 1 ,time))

                branch_times.extend(times)
            self.extended = True

    def will_vertex_be_activated(self,n,t_0):
        '''
        Returns whether vertex [n] will be active at time [t_0].
    
        :type n: int
        :type t_0: int

        :rtype: bool
        '''
        if self.chain.lV <= n and n<= self.chain.rV:
            self.extend_chain()
            return self.chain.will_vertex_be_activated(n,t_0)

        branch_index = self.select_branch(n)
        return self.branches[branch_index].will_vertex_be_activated(n,t_0)
    
    def when_will_vertex_be_activated(self,n):
        '''
        Returns the list of times for which vertex [n] will be active.
        
        :type n: int

        :rtype: list[int]
        '''
        if self.chain.lV <= n and n<= self.chain.rV:
            self.extend_chain()
            return list(set(self.chain.when_will_vertex_be_activated(n)))

        branch_index = self.select_branch(n)
        return self.branches[branch_index].when_will_vertex_be_activated(n)
  
