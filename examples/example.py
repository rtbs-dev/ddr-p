from pathlib import Path
import argparse
import logging
from functools import partial
import matplotlib.pyplot as plt
import utils.plot_utils as pu

toplvl_directory = Path(__file__).parents[1]
data_path = toplvl_directory/'data'
latex_path = toplvl_directory/'latex'/'example'/'img'  # <-- EDIT ME
latex_path.mkdir(parents=True, exist_ok=True)
log_path = latex_path/'logfile-example.txt'


def big_experiment_code(foo):
    if foo:
        s = 'foo\'d!'
    else:
        s = 'not foo\'d...'
    plt.plot(range(10), [2*x-3 for x in range(10)])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Generate plot/results for Excavator case study'
    )
    parser.add_argument('-s', '--save', action='store_true', default=False)
    parser.add_argument('foo', type=bool,
                        help='is `foo` true or false?')

    args = parser.parse_args()
    ps = partial(pu.plot_or_save, latex_path, args)

    pu.figure_setup()
    # np.random.seed(42)  # if using RNG in numpy, set seed to reproduce

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
    )
    logging.info('############ NEW RUN #############')
    logging.info("Run Parameters:\n"+str(args))

    big_experiment_code(args.foo)
    ps('willitfoo')

    if not args.save():
        # keep plots open for viewing if they weren't saved.
        plt.show()
