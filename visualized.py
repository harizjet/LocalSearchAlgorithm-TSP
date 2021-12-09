import matplotlib.pyplot as plt
import configparser


def visualized():
    config = configparser.ConfigParser()
    config.read('config.ini')

    fig, axes = plt.subplots(figsize=(15, 15), ncols=2, nrows=1)

    with open('data/result_gd.csv', 'r') as f:
        losses_gd = [t.split(',') for t in f.read().split('\n')]
    axes[0].plot(range(1, len(losses_gd) + 1),
                 list(map(int, [l[0] for l in losses_gd])),
                 color='red',
                 alpha=0.5,
                 label='accepted_cost',
                 linewidth=3)
    axes[0].plot(range(1, len(losses_gd) + 1),
                 list(map(int, [l[1] for l in losses_gd])),
                 color='blue',
                 alpha=0.3,
                 label='best_cost',
                 linewidth=3)
    axes[0].set_title('Loss curve for Great Deluge' +
                      '\n' +
                      config.get("variable", "gd_best_sol") +
                      '\n' +
                      'Distance: ' +
                      config.get("variable", "gd_best_cost"))
    axes[0].set_xlabel('iteration')
    axes[0].set_ylabel('loss')
    axes[0].legend()

    with open('data/result_sa.csv', 'r') as f:
        losses_sa = [t.split(',') for t in f.read().split('\n')]
    axes[1].plot(range(1, len(losses_sa) + 1),
                 list(map(int, [l[0] for l in losses_sa])),
                 color='red',
                 alpha=0.5,
                 label='accepted_cost',
                 linewidth=3)
    axes[1].plot(range(1, len(losses_sa) + 1),
                 list(map(int, [l[1] for l in losses_sa])),
                 color='blue',
                 alpha=0.3,
                 label='best_cost',
                 linewidth=3)
    axes[1].set_title('Loss curve for Simulated Annealing' +
                      '\n' +
                      config.get("variable", "sa_best_sol") +
                      '\n' +
                      'Distance: ' +
                      config.get("variable", "sa_best_cost"))
    axes[1].set_xlabel('iteration')
    axes[1].set_ylabel('loss')
    axes[1].legend()

    plt.show()


if __name__ == '__main__':
    visualized()
