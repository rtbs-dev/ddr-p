from pathlib import Path
import sys, os
sys.path.insert(0, os.path.abspath('..'))

toplvl_directory = Path(__file__).parents[1]
data_path = toplvl_directory/'data'
# latex_path = toplvl_directory/'submodule-name'/'img'
# latex_path.mkdir(parents=True, exist_ok=True)
# log_path = latex_path/'logfile-example.txt'

def big_experiment_code(foo):
    if foo:
        print('foo\'d!')
    else:
        print('not foo\'d...')

