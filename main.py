from location import Location
from location import Map
from algos.gd import GreatDeluge
from algos.sa import SimulatedAnnealing
from algos.tb import TabuSearch
from algos.hs import HarmonySearch
from cost import Cost
from visualized import visualized
import configparser
import sys

if __name__ == '__main__':

    if len(sys.argv) > 1:
        run_n = int(sys.argv[1])
        algos = sys.argv[2:]
    else:
        raise Exception("Wrong argument")

    theMap = Map()
    for _ in range(int(input())):
        place = input()
        theMap.add_location(place, Location(place))
    directions = []
    for _ in range(int(input())):
        directions.append(input().split())

    for direct in directions:
        ta, tb, dis = direct
        theMap.locations[ta].add_direction(tb, int(dis))
        theMap.locations[tb].add_direction(ta, int(dis))

    config = configparser.ConfigParser()
    config['variable'] = {}

    if 'gd' in algos:
        # Great Deluge
        gd_algorithm = GreatDeluge(
            estimation=30,
            options=list(theMap.locations.keys()),
            cost=Cost(theMap))
        gd_algorithm.run(run_n)
        resAccGD = gd_algorithm.acceptList
        resBesGD = gd_algorithm.bestList
        config['variable']['gd_best_sol'] = '->'.join(gd_algorithm.bestSol)
        config['variable']['gd_best_cost'] = str(gd_algorithm.bestCost)

        with open('data/result_gd.csv', 'w') as f:
            f.write('\n'.join([','.join([str(x), str(y)]) for x, y in zip(resAccGD, resBesGD)]))

    if 'sa' in algos:
        # Simulated Annealing
        sa_algorithm = SimulatedAnnealing(
            ini_temp=10,
            fin_temp=1,
            options=list(theMap.locations.keys()),
            cost=Cost(theMap))
        sa_algorithm.run(run_n)
        resAccSA = sa_algorithm.acceptList
        resBesSA = sa_algorithm.bestList
        config['variable']['sa_best_sol'] = '->'.join(sa_algorithm.bestSol)
        config['variable']['sa_best_cost'] = str(sa_algorithm.bestCost)

        with open('data/result_sa.csv', 'w') as f:
            f.write('\n'.join([','.join([str(x), str(y)]) for x, y in zip(resAccSA, resBesSA)]))

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    if 'tb' in algos:
        # Tabu Search
        tb_algorithm = TabuSearch(
            tabu_size=2,
            options=list(theMap.locations.keys()),
            cost=Cost(theMap))
        tb_algorithm.run(run_n)
        resAccTB = tb_algorithm.acceptList
        resBesTB = tb_algorithm.bestList
        config['variable']['tb_best_sol'] = '->'.join(tb_algorithm.bestSol)
        config['variable']['tb_best_cost'] = str(tb_algorithm.bestCost)

        with open('data/result_tb.csv', 'w') as f:
            f.write('\n'.join([','.join([str(x), str(y)]) for x, y in zip(resAccTB, resBesTB)]))

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    if 'hs' in algos:
        # Harmony Search
        hs_algorithm = HarmonySearch(
            hms=5,
            hmcr=0.7,
            par=0.2,
            options=list(theMap.locations.keys()),
            map=theMap,
            cost=Cost(theMap))
        hs_algorithm.run(improve_count=100)


    # if not config['variable']:
    #     raise Exception('Wrong algo selected.')
    
    # with open('config.ini', 'w') as configfile:
    #     config.write(configfile)

    # visualized(algos)
