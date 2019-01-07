import random
import Setting_Simulation_Value
import OpinionDynamics
import networkx as nx



class DecisionDynamics:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.opinion = OpinionDynamics.OpinionDynamics()      # opinion_dynamics 첫번째 인스턴스
        self.B_layer_dynamics()


    def B_layer_dynamics(self):  # B_layer 다이내믹스, 베타 적용 및 언어데스 알고리즘 적용
        global prob_beta
        for i in sorted(self.opinion.B_edges.nodes):
            opposite = []
            internal_edge_number = len(sorted(nx.all_neighbors(self.SS.B_edges, i)))
            external_edge_number = len(self.opinion.AB_neighbor[i])
            for j in range(internal_edge_number):
                if self.opinion.B[i] * self.opinion.B[sorted(nx.all_neighbors(self.opinion.B_edges, i))[j]] < 0:
                    opposite.append(1)
            for j in range(external_edge_number):
                if self.opinion.B[i] * self.opinion.A[self.opinion.AB_neighbor[i][j]] < 0:
                    opposite.append(1)
            prob_beta = (sum(opposite) / (external_edge_number + internal_edge_number)) ** beta
            self.opinion.B[i] = self.AS_model_function(self.opinion.B[i])
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
