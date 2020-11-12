# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:29:07 2020

@author: FSU
"""


 #The following program is not efficient   
 # it is mean to find the number of solutions to systemsw of equations
from scipy.special import comb


def doublehandleJoined(n):# a<B,B2<b<C,C2<c 
    sol = [(b-a-1)**2*(c-b-1)**2 for a in range(1,n-3) for b in range(a+1, n-1) for c in range(b+1, n+1) ]
    return  sum(sol)#, sum(sol)/n, sum(sol)/com, sum(sol)/sum(oneHandle),sum(sol)/(sum(oneHandle)*n),sum(sol)/(sum(oneHandle)*com),sum(sol)/(n*sum(oneHandle)*com)  




def rplot(M):
    dh = [doublehandleJoined(n) for n in range(5,M)]
    N = [v for v in range(5,M)]
        
    cub = [doublehandleJoined(n)/(n*comb(n, 5, exact=True)) for n in range(5,M)]
    print(f'points {N}\n  \n double joined handle {dh}')    
    import matplotlib.pyplot as plt
    
    
    plt.plot( N,cub, linewidth=2)
    plt.xlabel(' n ')
    plt.ylabel(f'O(double joined Handle))/n*comb ')
    plt.title(f"O(duuble joined handle)/n*comb as a function of 'n' ")
    plt.show()    
    #plt.plot()
rplot(40)

### results double joined handle [1, 10, 53, 200, 606, 1572, 3630, 7656, 15015, 27742, 48763, 82160, 133484, 210120, 321708, 480624, 702525, 1006962, 1418065, 1965304, 2684330, 3617900, 4816890, 6341400, 8261955, 10660806, 13633335, 17289568, 21755800, 27176336, 33715352, 41558880, 50916921, 62025690, 75149997]

    
    
def doublehandleSeparated(n):# a<b<c<d x<B<c b<C<d
    sol = [d-A-1 for a in range(1,n-2) for b in range(a+1, n-1) for c in range(b+1, n) for A in range(a+1,c) for d in range(c+1,n+1) ]
    return  sum(sol)#, sum(sol)/n, sum(sol)/com, sum(sol)/sum(oneHandle),sum(sol)/(sum(oneHandle)*n),sum(sol)/(sum(oneHandle)*com),sum(sol)/(n*sum(oneHandle)*com)  

def triplehandle(n):
    Handle = [(c-b-1)*(B-a-1)*(d-B-1) 
             for a in range(1,n-2) for b in range(a+1, n-1) for c in range(b+1, n)  for d in range(c+1, n+1) for B in range(b+1, c)]
    return sum(Handle)    
    
    
    
    
    
    
    
    
    
    
    
    
















from copy import deepcopy
import pdb
import pprint


class plants():
    def __init__(self, external=3,cost=0):
        if external <3:
            return None
        self.n = external-3  # we take 3 for pyramid(3) 
        self.cost = cost  # to allow other cost
        self.chinampa = {0:[complex(0,0),complex(1,0),complex(2,0)]}  # pyramid3
        self.top =  complex(2,2)  # auxiliary pointer
        self.h = 2  # height
        self.all = {}  # all activated
        self.b = 0 # bottom
        
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

    def digging(self, i=0):
        # adds the i transformation
        keys = sorted(self.chinampa.keys())
        activations = self.chinampa[keys[0]]
        try:
            root = activations[i]
        except IndexError:
            print('No such root')

        activations.remove(root)
        old = self.chinampa.get(keys[0]-1,[])
        self.chinampa[keys[0]-1] = old + [root-1j,root-1-1j]
        self.b = self.b - 1

    
    def fill(self):
        # creates a copy of external and returns all activations
        self.all = self.chinampa.copy()
        externals = self.all
        for i in range(self.b, self.h):
            listOfExternals = externals.get(i,[])
            numberAtLeveli = len(listOfExternals)
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


def poli(plant,garden, n, digging = True):
    # Auxiliar function
    if n == 0:
        garden.append(plant)
    elif n<0:
        pass    
    else:
        temp = deepcopy(plant)
        if digging:
            temp2 = deepcopy(plant)
            temp3 = deepcopy(plant)
            temp2.digging(0)
            temp3.digging(1)
            poli(temp2, garden, n-1)
            poli(temp3, garden, n-1)
        plant.gr()
        temp.gl()
        poli(plant, garden, n-1)
        poli(temp, garden, n-1)



def cost_Zero(n=3, printed = False):
    # this returns a list of all cascades with n external activations and cost 0
    pyramid = plants()
    ext = n-3
    garden = []
    poli(pyramid, garden, ext, False) # this makes plants
    chinampa = [plants() for i in [0,1,2]] # here we add roots
    [chinampa[i].digging(i) for i in [0,1,2]]
    poli(chinampa[0], garden, ext-1)
    poli(chinampa[1], garden, ext-1)
    poli(chinampa[2], garden, ext-1)
    if printed:
        [pprint.pprint(elem.fill(), indent=4, width=1) for elem in garden]
    return garden        
    
#first = cost_Zero(4, True)
#assert len(first) == 5
#print('test with all plants on 5 vertex passed')
#[pprint.pprint(elem.fill(),indent=4,width=1) for elem in first]
    
    
    
    
    
    
    
    
    
    
    
    
    
    

   

    
    
    
    
    
    