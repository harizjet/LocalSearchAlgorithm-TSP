from cost import Cost
import numpy as np


class GreatDeluge(object):
    def __init__(self,
                 estimation: int,
                 options: list,
                 cost: Cost,
                 level=None):

        self.estimation = estimation
        self.options = options
        self.length = len(options)
        self.costFunc = cost
        self.level = level
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

        level = best_cost if not self.level else self.level
        change_rate = (level - self.estimation) / iteration

        self.acceptList.append(best_cost)
        self.bestList.append(best_cost)

        for _ in range(iteration):
            ran_sol = self.pick_random(cur_sol)
            ran_cost = self.costFunc.cost(ran_sol)

            if ran_cost < best_cost:
                best_sol = ran_sol
                best_cost = ran_cost

            if ran_cost < level:
                cur_sol = ran_sol

            self.acceptList.append(self.costFunc.cost(cur_sol))
            self.bestList.append(best_cost)
            level -= change_rate

        self.bestSol = best_sol
        self.bestCost = best_cost
