import numpy as np
import Layer_A_Modeling
import Layer_B_Modeling
import math
import Setting_Simulation_Value

# Modeling : AB_edges, AB_neighbor, R, D

class Modeling:
    def __init__(self):
        self.A = Layer_A_Modeling.Layer_A_Modeling()                  ## A layer 첫번째 인스턴스
        self.B = Layer_B_Modeling.Layer_B_Modeling()                  ## B layer 첫번째 인스턴스
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.AB_edges = self.making_interconnected_edges()[0]
        self.AB_neighbor = self.making_interconnected_edges()[1]
        self.R = self.simulation_condition(self.SS.gap)[0]
        self.D = self.simulation_condition(self.SS.gap)[1]

    def making_interconnected_edges(self):
        self.AB_edges = []
        self.AB_neighbor = []
        for i in range(int(self.SS.A_node / self.SS.inter_edges)):
            for j in range(self.SS.inter_edges):
                connected_A_node = np.array(self.A.A_edges.nodes).reshape(-1, self.SS.inter_edges)[i][j]
                self.AB_neighbor.append(connected_A_node)
                self.AB_edges.append((i, connected_A_node))
        self.AB_neighbor = np.array(self.AB_neighbor).reshape(-1, self.SS.inter_edges)
        return self.AB_edges, self.AB_neighbor

    def simulation_condition(self, gap):
        self.R = np.linspace(0, 2, gap)
        self.D = np.linspace(self.making_beta_scale(gap)[0], self.making_beta_scale(gap)[1], gap)
        return self.R, self.D

    def making_beta_scale(self, a):
        scale = math.log((1 / (self.SS.B_edge + 1)) ** 3)\
                / math.log(self.SS.inter_edges / (self.SS.B_edge + self.SS.inter_edges))
        return 0, scale, a


if __name__ == "__main__":
    Layer_A = Layer_A_Modeling.Layer_A_Modeling()
    Layer_B = Layer_B_Modeling.Layer_B_Modeling()
    modeling = Modeling()
    print(modeling.R)







