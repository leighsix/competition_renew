import random
import Modeling
import Setting_Simulation_Value
import DecisionDynamics


class OpinionDynamics:
    def __init__(self):
        self.SS = Setting_Simulation_Value.Setting_Simulation_Value()
        self.M = Modeling.Modeling()                           # modeling 첫번째 인스턴스
        self.decision = DecisionDynamics.DecisionDynamics()    # decision 첫번째 인스턴스
        self.A_layer_dynamics()

    def A_layer_dynamics(self):  # A_layer 다이내믹스, 감마 적용 및 설득/타협 알고리즘 적용
        if DecisionDynamics.STEPS > 1:
            for i, j in sorted(self.M.A_edges.edges()):
                if self.decision.A[i] * self.decision.A[j] > 0:
                    self.decision.A[i] = self.A_layer_persuasion_function(self.decision.A[i], self.decision.A[j])[0]
                    self.decision.A[j] = self.A_layer_persuasion_function(self.decision.A[i], self.decision.A[j])[1]
                elif self.decision.A[i] * self.decision.A[j] < 0:
                    self.decision.A[i] = self.A_layer_compromise_function(self.decision.A[i], self.decision.A[j])[0]
                    self.decision.A[j] = self.A_layer_compromise_function(self.decision.A[i], self.decision.A[j])[1]
            for i, j in sorted(self.M.AB_edges):
                if self.decision.A[j] * self.decision.B[i] > 0:
                    self.decision.A[j] = self.AB_layer_persuasion_function(self.decision.A[j], self.B.B[i])[0]
                    self.decision.B[i] = self.AB_layer_persuasion_function(self.decision.A[j], self.B.B[i])[1]
                elif self.decision.A[j] * self.decision.B[i] < 0:
                    self.decision.A[j] = self.AB_layer_compromise_function(self.decision.A[j], self.B.B[i])[0]
                    self.decision.B[i] = self.AB_layer_compromise_function(self.decision.A[j], self.B.B[i])[1]
            return self.decision.A

        elif DecisionDynamics.STEPS <= 1:
            for i, j in sorted(self.M.A_edges.edges()):
                if self.M.A[i] * self.M.A[j] > 0:
                    self.M.A[i] = self.A_layer_persuasion_function(self.M.A[i], self.M.A[j])[0]
                    self.M.A[j] = self.A_layer_persuasion_function(self.M.A[i], self.M.A[j])[1]
                elif self.M.A[i] * self.M.A[j] < 0:
                    self.M.A[i] = self.A_layer_compromise_function(self.M.A[i], self.M.A[j])[0]
                    self.M.A[j] = self.A_layer_compromise_function(self.M.A[i], self.M.A[j])[1]
            for i, j in sorted(self.M.AB_edges):
                if self.M.A[j] * self.M.B[i] > 0:
                    self.M.A[j] = self.AB_layer_persuasion_function(self.M.A[j], self.B.B[i])[0]
                    self.M.B[i] = self.AB_layer_persuasion_function(self.M.A[j], self.B.B[i])[1]
                elif self.M.A[j] * self.M.B[i] < 0:
                    self.M.A[j] = self.AB_layer_compromise_function(self.M.A[j], self.B.B[i])[0]
                    self.M.B[i] = self.AB_layer_compromise_function(self.M.A[j], self.B.B[i])[1]
            return self.M.A


    def A_layer_persuasion_function(self, a, b):  # A layer 중에서 same orientation 에서 일어나는  변동 현상
        z = random.random()
        if z < prob_p:
            if a > 0:
                a = self.A_layer_node_right(a, self.SS.MAX)
                b = self.A_layer_node_right(b, self.SS.MAX)
            elif a < 0:
                a = self.A_layer_node_left(a, self.SS.MIN)
                b = self.A_layer_node_left(b, self.SS.MIN)
        elif z > prob_p:
            a = a
            b = b
        return a, b

    def A_layer_compromise_function(self, a, b):  # A layer  중에서 opposite orientation 에서 일어나는 변동 현상
        z = random.random()
        if z < (1 - prob_p):
            if a * b == -1:
                if z < ((1 - prob_p) / 2):
                    a = 1
                    b = 1
                elif z > ((1 - prob_p) / 2):
                    a = -1
                    b = -1
            elif a > b:
                a = self.A_layer_node_left(a, self.SS.MIN)
                b = self.A_layer_node_right(b, self.SS.MAX)
            elif a < b:
                a = self.A_layer_node_right(a, self.SS.MAX)
                b = self.A_layer_node_left(b, self.SS.MIN)
        elif z > (1 - prob_p):
            a = a
            b = b
        return a, b

    def AB_layer_persuasion_function(self, a, b):  # A-B layer 중에서 same orientation 에서 일어나는  변동 현상
        z = random.random()
        if z < prob_p:
            if a > 0:
                a = self.A_layer_node_right(a, self.SS.MAX)
                b = b
            elif a < 0:
                a = self.A_layer_node_left(a, self.SS.MIN)
                b = b
        elif z > prob_p:
            a = a
            b = b
        return a, b

    def AB_layer_compromise_function(self, a, b):  # A-B layer  중에서 opposite orientation 에서 일어나는 변동 현상
        z = random.random()
        if z < (1 - prob_p):
            if a * b == -1:
                if z < ((1 - prob_p) / 2):
                    a = 1
                    b = b
                elif z > ((1 - prob_p) / 2):
                    a = -1
                    b = b
            elif a > b:
                a = self.A_layer_node_left(a, self.SS.MIN)
                b = b
            elif a < b:
                a = self.A_layer_node_right(a, self.SS.MAX)
                b = b
        elif z > (1 - prob_p):
            a = a
            b = b
        return a, b

    def A_layer_node_left(self, a, Min):
        if a >= Min:
            if a == Min:
                a = a
            elif a < 0 or a > 1:
                a = a - 1
            elif a == 1:
                a = -1
        elif a < Min:
            a = Min
        return a

    def A_layer_node_right(self, a, Max):
        if a <= Max:
            if a == Max:
                a = a
            elif a > 0 or a < -1:
                a = a + 1
            elif a == -1:
                a = 1
        elif a > Max:
            a = Max
        return a

if __name__ == "__main__":
    opinion_dynamics = OpinionDynamics()