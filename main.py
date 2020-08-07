# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:29:07 2020

@author: FSU
"""
import pdb
class plants():
    def __init__(self, cost=0,external=3):
        if external <3:
            return None
        self.n = external-3  # we take 3 for pyramid(3) 
        self.cost = cost  # to allow other cost
        self.chinampa = {0:[complex(0,0),complex(1,0),complex(2,0)]}  # pyramid3
        self.top =  complex(2,2)  # auxiliary pointer
        self.h = 2  # height
        self.all = {}  # all activated
        
    def fill(self):
        self.__str__()
        return self.all
    
    def gl(self,degree = 0):
        self.chinampa[self.h-degree] = self.chinampa.get(self.h-degree,[]) + [self.top-1 -degree*(1j+1)]
        self.h = self.h+1
        self.top = self.top +1j

    def gr(self,degree = 0):        
        self.chinampa[self.h-degree] =self.chinampa.get(self.h-degree,[])+ [self.top+1-degree*1j] 
        self.h = self.h+1
        self.top = self.top +1+1j
        
    def __str__(self):
        pdb.set_trace()
        self.all = self.chinampa.copy()
        externals = self.all
        for i in range(self.h):
            listOfExternals = externals.get(i,[])
            numberAtLeveli = len(listOfExternals)
            print(numberAtLeveli)
            if numberAtLeveli:
                listOfExternals = sorted( listOfExternals, key = lambda x: x.real)                
                initial = listOfExternals[0]
                for element in listOfExternals[1:]:
                    if element == initial+1:
                        self.all[i+1] = self.all.get(i+1,[])+[element+1j]
                        initial = element
        return str('output in self.all')
            
            
   