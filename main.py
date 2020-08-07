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
        
    
    def gl(self,degree = 0):
        # grafring left
        self.chinampa[self.h-degree] = self.chinampa.get(self.h-degree,[]) + [self.top-1 -degree*(1j+1)]
        self.h = self.h+1
        self.top = self.top +1j


    def gr(self,degree = 0):
        # grafting right
        self.chinampa[self.h-degree] =self.chinampa.get(self.h-degree,[])+ [self.top+1-degree*1j] 
        self.h = self.h+1
        self.top = self.top +1+1j


    def chinampa(self):
        # returns chinampa
        return self.chinampa

    
    def root(self,i=0):
        # adds the i root
        keys = sorted(self.chinampa.keys())
        activations = self.chinampa[keys[0]]
        try:
            root = activations[i]
        except IndexError:
            print('No such root')
            return ''
        activations.remove(root)
        old = self.chinampa.get(keys[0]-1,[])
        self.chinampa[keys[0]-1] = old + [root-1,root-1-1j]
        return 'root updated'

        
    def fill(self):
        # creates a copy of external and returns all activations
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
        return self.all

    def __str__():
        # it should print x and y to form cascades
        return 'we are now using self.fill to get all activations'            
   