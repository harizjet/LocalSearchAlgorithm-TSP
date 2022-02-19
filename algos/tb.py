from cost import Cost
import numpy as np
import math
from typing import Tuple


class TabuSearch(object):
    def __init__(self,
                 tabu_size: int,
                 options: list,
                 cost: Cost):

        super().__init__()
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

    def best_swap_taboo(self, 
                        cur_sol: list, 
                        best_cost: int, 
                        tabu_queue: list) -> Tuple[list, list]:
        t_sol = cur_sol[:]
        t_cost = math.inf
        now_sol = None
        now_cost = None
        now_step = None

        t1 = np.arange(1, len(cur_sol))
        t2 = t1 - 1

        for f, s in zip(t1, t2):
            tarray = t_sol[:]
            tarray[f], tarray[s] = \
                tarray[s], tarray[f]
            tstep = [tarray[f], tarray[s]]
            tcost = self.costFunc.cost(tarray)
            tstep.sort()

            if tstep not in tabu_queue or tcost < best_cost:
                if tcost < t_cost:
                    now_sol = tarray
                    now_cost = tcost
                    now_step = tstep
                    t_cost = tcost

        return now_sol, now_cost, now_step

    def run(self, iteration: int) -> None:
        cur_sol = self.pick_random(self.options)
        cur_cost = self.costFunc.cost(cur_sol)

        best_sol = cur_sol
        best_cost = cur_cost

        tabu_queue = []

        for _ in range(iteration):
            now_sol, now_cost, now_step = self.best_swap_taboo(cur_sol, best_cost, tabu_queue)
            cur_sol = now_sol

            if len(tabu_queue) == self.tabu_size:
                tabu_queue.pop(0)
            tabu_queue.append(now_step)
        
            if now_cost < best_cost:
                best_sol = now_sol
                best_cost = now_cost

            self.acceptList.append(self.costFunc.cost(cur_sol))
            self.bestList.append(best_cost)

        self.bestSol = best_sol
        self.bestCost = best_cost

            

            