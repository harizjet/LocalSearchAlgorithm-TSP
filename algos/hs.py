import numpy as np
import random
from location import Map
from cost import Cost
import time


class HarmonySearch(object):
    def __init__(self, 
                 hms: int, 
                 hmcr: float, 
                 par: float, 
                 options: list,
                 map: Map,
                 cost: Cost):

        super().__init__()
        self.hms = hms
        self.hmcr = hmcr
        self.par = par
        self.options = options
        self.length = len(options)
        self.map = map
        self.costFunc = cost
        self.acceptList = []
        self.bestList = []
        self.bestSol = None
        self.bestCost = None

    def pick_random(self, options: list) -> list:
        return list(np.random.choice(options,
                                     self.length,
                                     replace=False))

    def initialization(self) -> None:
        self.memoryHS = self.pick_random(self.options)
        for _ in range(self.hms - 1):
            random = self.pick_random(self.options)
            self.memoryHS = np.vstack((self.memoryHS, random))

    def sort_memory(self) -> None:
        self.memoryHS = np.array(sorted(self.memoryHS.tolist(), 
            key = lambda x: self.costFunc.cost(x)))

    def pick_avai_city(self, 
                       avai_city: set, 
                       memory_city: set) -> str:
        cities = list(memory_city.intersection(avai_city))
        if cities:
            return random.choice(cities)
        else:
            return random.choice(list(avai_city))

    def pick_closest_city(self, avai_city: set, select_city: str) -> str:
        t = []
        for city, dist in self.map.locations[select_city].directions.items():
            if (not t or dist < t[1]) and city in avai_city:
                t = [city, dist]
        if t:
            return t[0]
        else:
            return list(avai_city)[0]

    def run(self, n: int, n_for_improve=False):
        # generate feasible solution
        self.initialization()
        # sort the memory
        self.sort_memory()

        # while haven't reach target
        i, plateau_n = 0, 0
        while i < n:
            new_route = [0] * self.length
            avai_city = set(self.options.copy())

            # for every col in solution
            for col in range(self.length):
                city = None

                # generate a number between 0 and 1 and compare with HMCR value
                pHMCR = random.random()
                if pHMCR < self.hmcr:
                    # pick an available city in HS memory for that col
                    tSet = set(self.memoryHS[:,col: col+1].squeeze().tolist())
                    city = self.pick_avai_city(avai_city, tSet)

                    # generate a number between 0 and 1 and compare with PAR value
                    pPAR = random.random()
                    if pPAR < self.par:
                        # mutation by select closest city from the selected city
                        city = self.pick_closest_city(avai_city, city)
                else:
                    # pick a city randomly
                    city = random.choice(list(avai_city))

                # added the city and remove from the available city
                new_route[col] = city
                avai_city.remove(city)

            # calculate the fitness of the solution
            new_cost = self.costFunc.cost(new_route)
            # debugging
            print(new_cost, self.costFunc.cost(self.memoryHS[-1]), self.costFunc.cost(self.memoryHS[0]), i)
            # check if the fitness value is better than the fitness value of the lowest solution in memory
            if new_cost < self.costFunc.cost(self.memoryHS[-1]):
                self.memoryHS[-1] = new_route
                self.sort_memory()

                # check if the n is used for improving count
                if n_for_improve:
                    self.acceptList.append(new_cost)
                    self.bestList.append(self.costFunc.cost(self.memoryHS[0]))
                    i += 1
                # reset the plateau value
                plateau_n = 0

            # check if the n is used for iteration count
            if not n_for_improve:
                self.acceptList.append(new_cost)
                self.bestList.append(self.costFunc.cost(self.memoryHS[0]))

                i += 1

            # increase the plateau value
            plateau_n += 1

            # quit if the plateau value hit
            if plateau_n == n * 10:
                break

        self.bestSol = self.memoryHS[0]
        self.bestCost = self.costFunc.cost(self.memoryHS[0])
