from location import Location
from location import Map
from algos.gd import GreatDeluge
from algos.sa import SimulatedAnnealing
from algos.tb import TabuSearch
from cost import Cost
from visualized import visualized
import configparser
import sys

if __name__ == '__main__':

    if len(sys.argv) > 1:
        algo = sys.argv[1]
    else:
        raise Exception("Wrong argument, please select an algorithm.")

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

    if algo == 'gd':
        # Great Deluge
        gd_algorithm = GreatDeluge(
            estimation=30,
            options=list(theMap.locations.keys()),
            cost=Cost(theMap))
        gd_algorithm.run(200)
        resAccGD = gd_algorithm.acceptList
        resBesGD = gd_algorithm.bestList
        config['variable']['gd_best_sol'] = '->'.join(gd_algorithm.bestSol)
        config['variable']['gd_best_cost'] = str(gd_algorithm.bestCost)

        with open('data/result_gd.csv', 'w') as f:
            f.write('\n'.join([','.join([str(x), str(y)]) for x, y in zip(resAccGD, resBesGD)]))
    elif algo == 'sa':
        # Simulated Annealing
        sa_algorithm = SimulatedAnnealing(
            ini_temp=10,
            fin_temp=1,
            options=list(theMap.locations.keys()),
            cost=Cost(theMap))
        sa_algorithm.run(200)
        resAccSA = sa_algorithm.acceptList
        resBesSA = sa_algorithm.bestList
        config['variable']['sa_best_sol'] = '->'.join(sa_algorithm.bestSol)
        config['variable']['sa_best_cost'] = str(sa_algorithm.bestCost)

        with open('data/result_sa.csv', 'w') as f:
            f.write('\n'.join([','.join([str(x), str(y)]) for x, y in zip(resAccSA, resBesSA)]))

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    elif algo == 'tb':
         # Great Deluge
        gd_algorithm = GreatDeluge(
            estimation=30,
            options=list(theMap.locations.keys()),
            cost=Cost(theMap))
        gd_algorithm.run(200)
        resAccGD = gd_algorithm.acceptList
        resBesGD = gd_algorithm.bestList
        config['variable']['gd_best_sol'] = '->'.join(gd_algorithm.bestSol)
        config['variable']['gd_best_cost'] = str(gd_algorithm.bestCost)

        with open('data/result_gd.csv', 'w') as f:
            f.write('\n'.join([','.join([str(x), str(y)]) for x, y in zip(resAccGD, resBesGD)]))
            
        # Tabu Search
        tb_algorithm = TabuSearch(
            tabu_size=2,
            options=list(theMap.locations.keys()),
            cost=Cost(theMap))
        tb_algorithm.run(200)
        resAccTB = tb_algorithm.acceptList
        resBesTB = tb_algorithm.bestList
        config['variable']['tb_best_sol'] = '->'.join(tb_algorithm.bestSol)
        config['variable']['tb_best_cost'] = str(tb_algorithm.bestCost)

        with open('data/result_tb.csv', 'w') as f:
            f.write('\n'.join([','.join([str(x), str(y)]) for x, y in zip(resAccTB, resBesTB)]))

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        raise Exception('Wrong algo selected.')
    visualized()
