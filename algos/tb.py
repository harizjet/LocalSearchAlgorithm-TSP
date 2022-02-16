from cost import Cost
import numpy as np


class TabuSearch(object):
    def __init__(self,
                 tabu_size: int,
                 options: list,
                 cost: Cost):
    
        self.tabu_size = tabu_size
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

    def adjacent_swap(self, cur_sol: list, number=1) -> list:
        t1 = np.array(np.random.choice(range(1, self.length),
                             number,
                             replace=False))
        t2 = t1 - 1

        for f, s in zip(t1, t2):
            cur_sol[f], cur_sol[s] = \
                cur_sol[s], cur_sol[f]

        return cur_sol

    def run(self, iteration: int) -> None:
        cur_sol = self.pick_random(self.options)
        cur_cost = self.costFunc.cost(cur_sol)

        best_sol = cur_sol
        best_cost = cur_cost

        tabu_queue = []

        for _ in range(iteration):
            ran_sol = self.adjacent_swap(cur_sol)
            ran_cost = self.costFunc.cost(ran_sol)
            cur_cost = self.costFunc.cost(cur_sol)

            if ran_sol not in tabu_queue or ran_cost < cur_cost:
                cur_sol = ran_sol
                if len(tabu_queue) == self.tabu_size:
                    tabu_queue.pop(0)
                tabu_queue.append(cur_sol)
            
                if ran_cost < best_cost:
                    best_sol = ran_sol
                    best_cost = ran_cost
            
            self.acceptList.append(self.costFunc.cost(cur_sol))
            self.bestList.append(best_cost)

        self.bestSol = best_sol
        self.bestCost = best_cost

            

            