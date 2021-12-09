from location import Map


class Cost(object):
    def __init__(self,
                 the_map: Map):

        self.the_map = the_map

    def cost(self, chosen: list) -> int:
        total = 0
        for i in range(len(chosen)):
            total += self.the_map.locations[chosen[i]].\
                directions[chosen[(i + 1) % len(chosen)]]
        return total
