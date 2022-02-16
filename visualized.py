import matplotlib.pyplot as plt
import configparser
from utils import visual_variable


def visualized(algo_s: list) -> None:
    config = configparser.ConfigParser()
    config.read('config.ini')

    fig, axes = plt.subplots(figsize=(15, 15), ncols=len(algo_s), nrows=1)
    
    for i, algo in enumerate(algo_s):
        variable = visual_variable(algo)
        axe = axes[i] if len(algo_s) > 1 else axes

        with open(variable[0], 'r') as f:
            losses = [t.split(',') for t in f.read().split('\n')]
        axe.plot(range(1, len(losses) + 1),
                     list(map(int, [l[0] for l in losses])),
                     color='red',
                     alpha=0.5,
                     label='accepted_cost',
                     linewidth=3)
        axe.plot(range(1, len(losses) + 1),
                     list(map(int, [l[1] for l in losses])),
                     color='blue',
                     alpha=0.3,
                     label='best_cost',
                     linewidth=3)
        axe.set_title('Loss curve for {}'.format(variable[1]) +
                          '\n' +
                          config.get("variable", variable[2]) +
                          '\n' +
                          'Distance: ' +
                          config.get("variable", variable[3]))
        axe.set_xlabel('iteration')
        axe.set_ylabel('loss')
        axe.legend()

    plt.show()


if __name__ == '__main__':
    visualized()
