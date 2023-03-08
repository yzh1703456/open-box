# License: MIT
import numpy as np
import matplotlib.pyplot as plt
from openbox import ParallelOptimizer, space as sp
from openbox.utils.constants import SUCCESS


# Define Objective Function
def branin(config):
    x1, x2 = config['x1'], config['x2']
    y = (x2 - 5.1 / (4 * np.pi ** 2) * x1 ** 2 + 5 / np.pi * x1 - 6) ** 2 \
        + 10 * (1 - 1 / (8 * np.pi)) * np.cos(x1) + 10
    return {'objectives': [y]}


def test_examples_evaluate_sync_parallel_optimization():
    max_runs = 20

    # Define Search Space
    space = sp.Space()
    x1 = sp.Real("x1", -5, 10, default_value=0)
    x2 = sp.Real("x2", 0, 15, default_value=0)
    space.add_variables([x1, x2])

    # Parallel Evaluation on Local Machine
    opt = ParallelOptimizer(
        branin,
        space,
        parallel_strategy='sync',
        batch_size=4,
        batch_strategy='default',
        num_objectives=1,
        num_constraints=0,
        max_runs=max_runs,
        # surrogate_type='gp',
        surrogate_type='auto',
        task_id='parallel_sync',
        logging_dir='logs/pytest/',
    )
    history = opt.run()

    print(history)

    history.plot_convergence(true_minimum=0.397887)
    # plt.show()
    plt.savefig('logs/pytest/sync_parallel_convergence.png')
    plt.close()

    assert history.trial_states[:max_runs].count(SUCCESS) == max_runs
