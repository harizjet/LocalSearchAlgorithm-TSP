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
        self.best_sol = None
        self.best_cost = None

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

    def run(self, improve_count: int):
        self.initialization()
        self.sort_memory()
        i = 0
        while i < improve_count:
            new_route = [0] * self.length
            avai_city = set(self.options.copy())
            for col in range(self.length):
                city = None

                pHMCR = random.random()
                if pHMCR < self.hmcr:
                    # pick a available city in HS memory
                    tSet = set(self.memoryHS[:,col: col+1].squeeze().tolist())
                    city = self.pick_avai_city(avai_city, tSet)

                    pPAR = random.random()
                    if pPAR < self.par:
                        # mutation by select closest city from the selected city
                        city = self.pick_closest_city(avai_city, city)
                else:
                    # pick a city randomly
                    city = random.choice(list(avai_city))
                new_route[col] = city
                avai_city.remove(city)

            new_cost = self.costFunc.cost(new_route)
            print(new_cost, self.costFunc.cost(self.memoryHS[-1]), self.costFunc.cost(self.memoryHS[0]), i)
            if new_cost < self.costFunc.cost(self.memoryHS[-1]):
                self.memoryHS[-1] = new_route 
                self.sort_memory()
                i += 1

        self.best_sol = self.memoryHS[0]
        self.best_cost = self.costFunc.cost(self.memoryHS[0])
