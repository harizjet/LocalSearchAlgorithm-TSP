from cost import Cost
import numpy as np
import random
import math


class SimulatedAnnealing(object):
    def __init__(self,
                 ini_temp: int,
                 fin_temp: int,
                 options: list,
                 cost: Cost,
                 cool_rate=None):

        super().__init__()
        self.ini_temp = ini_temp
        self.fin_temp = fin_temp
        self.cool_rate = cool_rate
        self.options = options
        self.length = len(options)
        self.costFunc = cost
        self.acceptList = []
        self.bestList = []
        self.bestSol = None
        self.bestCost = None

    def pick_random(self, options: list) -> list:
        return list(np.random.choice(options,
                                     self.length,
                                     replace=False))

    def swap(self, cur_sol: list, number=2) -> list:
        t1 = np.random.choice(range(self.length),
                              number,
                              replace=False)
        t2 = np.random.choice(range(self.length),
                              number,
                              replace=False)
        for f, s in zip(t1, t2):
            cur_sol[f], cur_sol[s] = \
                cur_sol[s], cur_sol[f]

        return cur_sol

    def adjacent_swap(self, cur_sol: list) -> list:
        cur_sol = cur_sol[:]

        t1 = np.array(np.random.choice(range(1, self.length),
                             1,
                             replace=False))
        t2 = t1 - 1

        for f, s in zip(t1, t2):
            cur_sol[f], cur_sol[s] = \
                cur_sol[s], cur_sol[f]

        return cur_sol 

    def run(self, iteration: int):
        cur_sol = self.pick_random(self.options)
        cur_cost = self.costFunc.cost(cur_sol)

        best_sol = cur_sol
        best_cost = cur_cost

        cool_rate = (self.ini_temp-self.fin_temp)/iteration \
            if not self.cool_rate else self.cool_rate
        cur_temp = self.ini_temp

        self.acceptList.append(best_cost)
        self.bestList.append(best_cost)

        for _ in range(iteration):
            ran_sol = self.pick_random(cur_sol)
            ran_cost = self.costFunc.cost(ran_sol)

            if ran_cost < best_cost:
                best_sol = ran_sol
                cur_sol = ran_sol
                best_cost = ran_cost
            else:
                c = ran_cost-cur_cost
                ran_num = random.random()
                if ran_num < math.e**(-c/cur_temp):
                    cur_sol = ran_sol
            self.acceptList.append(self.costFunc.cost(cur_sol))
            self.bestList.append(best_cost)

            if self.cool_rate:
                cur_temp *= self.cool_rate
            else:
                cur_temp -= cool_rate

        self.bestSol = best_sol
        self.bestCost = best_cost
