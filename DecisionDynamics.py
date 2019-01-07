import random
import Modeling
import Setting_Simulation_Value
import Layer_A_Modeling
import Layer_B_Modeling
import networkx as nx


class DecisionDynamics:
    def __init__(self):
        self.A = Layer_A_Modeling.Layer_A_Modeling()
        self.B = Layer_B_Modeling.Layer_B_Modeling()
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.M = Modeling.Modeling()
        ##self.B_layer_dynamics()

    def B_layer_dynamics(self):  # B_layer 다이내믹스, 베타 적용 및 언어데스 알고리즘 적용
        global prob_beta
        flow_prob_beta = []  # 베타 적용 확률 변화 리스트
        for i in sorted(B_edges.nodes):
            opposite = []
            intra_edge_number = len(sorted(nx.all_neighbors(self.SS.B_edges, i)))
            inter_edge_number = len(AB_neighbor[i])
            for j in range(intra_edge_number):
                if B[i] * B[sorted(nx.all_neighbors(B_edges, i))[j]] < 0:
                    opposite.append(1)
            for j in range(inter_edge_number):
                if B[i] * A[AB_neighbor[i][j]] < 0:
                    opposite.append(1)
            prob_beta = (sum(opposite) / (inter_edge_number + intra_edge_number)) ** beta
            B[i] = AS_model_function(B[i])
            flow_prob_beta.append(prob_beta)  # 베타 적용 확률 변화 리스트
        Flow_prob_beta.append(np.mean(flow_prob_beta))  # 노드의 prob_beta 평균에 대한 변화 리스트
        return B, Flow_prob_beta

    def AS_model_function(self, a):  # B layer 에서 일어나는 변동 현상
        z = random.random()
        if z < prob_beta:
            a = -a
        return a


if __name__ == "__main__" :
    modeling = Modeling()
