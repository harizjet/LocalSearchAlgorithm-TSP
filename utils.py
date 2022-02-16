def visual_variable(algo: str) -> list:
    tdict = {
        'sa': ['data/result_gd.csv', 'Great Deluge', 'gd_best_sol', 'gd_best_cost'],
        'gd': ['data/result_sa.csv', 'Simulated Annealing', 'sa_best_sol', 'sa_best_cost'],
        'tb': ['data/result_tb.csv', 'Tabu Search', 'tb_best_sol', 'tb_best_cost']
    }

    return tdict[algo]