from chinampas import chinampa as ch


class TestClass:
    def __init__(self):
        activations = [[2,0],[3,0],[4,1],[0,2],[1,2],[3,2],[2,3],[3,3],[5,5]]
        self.chain = ch.Chain_Chinampa(activations)
        self.tree = ch.Tree_Chinampa(0,{0:{'activations':[[4,0],[5,0]],'branches':[1,2]},
                           1:{'activations':[[0,0],[1,0]],'branches':[]},
                           2:{'activations':[[2,2],[3,2]],'branches':[]}
                           }
                       )


    def test_line_one(self):
        x = self.chain.will_vertex_be_activated(2,2)
        assert x == False

    def test_line_two(self):
        x = self.chain.will_vertex_be_activated(5,7)
        assert x == True

 
    def test_one(self):
        x = self.tree.will_vertex_be_activated(5,5)
        assert x == True

    def test_two(self):
        x = self.tree.will_vertex_be_activated(5,6)
        assert x == False

