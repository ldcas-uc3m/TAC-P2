import subprocess
from pathlib import Path
import json
import os
import platform
import logging
import sys
from typing import Callable, Literal, Annotated
from itertools import product

import statistics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
import matplotlib.colors as mcolors




logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(handler)


REPO_ROOT = Path(__file__).parent.parent
SIMULATOR_EXEC: Path = REPO_ROOT/f"build/src/p2{'.exe' if platform.system() == 'Windows' else ''}"
DATA_FOLDER = REPO_ROOT/"data/"

if os.path.exists(REPO_ROOT/"report"):
    IMAGE_FOLDER = REPO_ROOT/"report/img/"
else:
    IMAGE_FOLDER = DATA_FOLDER/"img"
    os.mkdir(IMAGE_FOLDER)




# ==============
# TEST FUNCTIONS
# ==============

def test(n: int, p: float, algorithm: str, iterations: int) -> pd.DataFrame:
    """
    Creates random graphs or SAT problems of size `n` with probability of edges `p`, and applies the selected algorithm for the specified number of `iterations`.

    :param n: Size of the graph or number of variables/clauses in SAT problem.
    :param p: Probability of an edge between two nodes, between `0` and `1`.
    :param algorithm: Algorithm to apply.
    :param iterations: Number of tests.
    :param sat_problem: The SAT problem string (only used if algorithm is 'SAT-CLIQUE').

    :return: DataFrame with columns {n, result, duration}
    """
    args = [
        SIMULATOR_EXEC,
        f"--n={n}",
        f"--p={p}",
        f"--algorithm={algorithm}",
        f"--iterations={iterations}",
        "--nograph"
    ]

    results = pd.DataFrame(columns=['n', 'result', 'duration'])
    output = subprocess.check_output(args)
    tests = json.loads(output)['tests']

    for t in tests:
        results.loc[len(results)] = {
            'n': n,
            'result': t['result'],
            'duration': t['duration']
        }

    return results


def test_n (n_min, n_max, probability, algorithm, n_tests):
    """
    Function to calculate the average duration depending on the n size (Number of vertices of the graph)
    """

    results = pd.DataFrame(columns=['n', 'duration'])
    
    for n in range(n_min, n_max + 1):
        print(f"n: {n}, p: {probability}, algorithm: {algorithm}", end='\r')
        run = test(n, probability, algorithm, n_tests)
        average_duration = run['duration'].mean()
        results = results._append({'n': n, 'duration': average_duration}, ignore_index=True)

    return results


def test_p (n, algorithm, n_tests):
    """
    Function to calculate the average duration depending on the p (probability of edge between two nodes)
    """

    results = pd.DataFrame(
        columns=[
            'n',
            'p',
            'duration'
        ]
    )

    p = 0.1
    while p <= 1:
        print(f"n: {n}, p: {p}", end='\r')
        durations = []

        ''' 
        # For each graph size, it is executed 10 times and then calculate the average execution time
        for index in range(n_tests):
            run = test(n, p, algorithm, 1)
            durations.append(run['duration'][0])
        
        avg_duration = statistics.mean(durations)

        #In the dataframe is saved the average time needed for each graph size
        new_values = pd.DataFrame({'n': [n], 'p': [p], 'duration': [avg_duration]})
        p+=0.1
        results = pd.concat([results, new_values], ignore_index=True)
        
        '''
        #Run a battery of tests with the n given and the n_tests number of times given
        run = test(n, p, algorithm, n_tests)
        
        #Take the average duration for each n size
        average_durations = run['duration'].mean()

        #Save the results into a dataframe
        new_row = pd.DataFrame({
            'n': [n],
            'p': [p],
            'duration': [average_durations]
        })
        results = pd.concat([results, new_row], ignore_index=True)

        p+=0.05

        sys.stdout.write("\033[K")  # clear line

    #print(results)
    return results



def test_sat() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Performs a batch of 3-SAT problems.
    """
    results = pd.DataFrame(columns=['iteration', 'result', 'time'])
    results_t = pd.DataFrame(columns=['iteration', 'result', 'time'])

    programs = [
        "((c+b+-c)*(a+b+c)*(-a+b+c))",
        "((c+b+-c)*(a+b+c)*(-a+b+-c))",
        "((c+b+-c)*(a+-b+c)*(-a+b+-c))",
        "((c+b+-c)*(b+b+c)*(a+b+-c))"
    ]

    i: int = 0
    for program in programs:
        test: dict = json.loads(subprocess.check_output([
            SIMULATOR_EXEC,
            "--algorithm=SAT-CLIQUE",
            "--nograph",
            program
        ]))

        results.loc[len(results)] = {
            'iteration': i,
            'result': test['result'],
            'time': test['duration'],
        }

        results_t.loc[len(results)] = {
            'iteration': i,
            'result': test['result'],
            'time': test['duration_transf']
        }

        i += 1

    return results, results_t



# ==============
# PLOT FUNCTIONS
# ==============


def plot_dataframes(
    dfs: dict[str, pd.DataFrame],
    x_column: str,
    y_column: str,
    save_file: str | None = None
):
    """
    Plots dataframes.

    :param df: Map of DF name and DF.
    :param x_column: Column from DF to represent on the X axis.
    :param y_column: Column from DF to represent on the Y axis.
    :param save_file: File to save the image to. If `None`, shows the plot.
    """

    fig, ax = plt.subplots()

    for name, df in dfs.items():
        ax.plot(df[x_column], df[y_column], marker='o', label=name)

        # Set x-axis ticks specifically for 'n' or based on the x_column data type
        if x_column == 'n':
            # Set ticks on the x-axis for each unique point in the x data, spaced by intervals of 20
            ax.xaxis.set_major_locator(MultipleLocator(20))
        elif x_column == 'p':
            # Set ticks on the x-axis for each unique point in the x data, spaced by intervals of 20
            ax.xaxis.set_major_locator(MultipleLocator(0.1))
        else:
            # Set ticks for other x_columns
            unique_x = df[x_column].dropna().unique()
            ax.set_xticks(unique_x if len(unique_x) < 20 else np.linspace(min(unique_x), max(unique_x), 20))

    # Determine the color palette depending on the number of data series
    if len(dfs) <= len(mcolors.BASE_COLORS):
        palette = list(mcolors.BASE_COLORS.values())
    else:
        palette = list(mcolors.XKCD_COLORS.values())

    ax.set_prop_cycle(color=palette)

    # Add labels
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column + ' (ms)')

    ax.legend()

    if save_file:
        fig.savefig(save_file)
    else:
        plt.show()

    plt.close()


def plot_functions(
    funcs: dict[str, Callable[[np.ndarray], np.ndarray]],
    n0: int = 10,
    n_max: int = 100,
    granularity: int = 1,
    save_file: str | Path | None = None
):
    """
    Plots functions refering to the complexity of turing machines (in terms of n and number of steps).

    :param funcs: Map of function name and function (`{"f(n)": f_n, ...}`).
    :param n0: Initial value of n.
    :param n_max: Maximum value of n to plot.
    :param granularity: Granularity of the plot. Default (`1`) means plot `nmax - n0` random points
    :param save_file: File to save the image to. If `None`, shows the plot.
    """

    fig, ax = plt.subplots()

    x = np.linspace(n0, n_max, granularity * (n_max - n0))

    for name, fn in funcs.items():
        ax.plot(x, fn(x), label=name)

    # automatic colors
    if len(funcs) <= len(mcolors.BASE_COLORS):
        pallete = mcolors.BASE_COLORS
    else:
        pallete = mcolors.XKCD_COLORS

    ax.set_prop_cycle(color=pallete)

    # Agregar etiquetas
    ax.set_xlabel('n')
    ax.set_ylabel('steps')

    ax.legend()

    if save_file:
        fig.savefig(save_file)
    else:
        fig.show()

    plt.close()





if __name__ == "__main__":
    if not SIMULATOR_EXEC.exists():
        exit(f"TM simulator executable not found at {SIMULATOR_EXEC}. Have you run CMake?")

    default_probability = 0.5
    DFS_worst_probability = 1
    default_n = 5

    #----Unitary test----
    #result = test(4, 0.5, "PATH-DFS", 1)
    #print('Result: ', result['result'][0])
    #print('Duration: ', result['duration'][0])

    logger.info("Testing PATH-DFS...")


    #----PATH-DFS test n----
    
    # 25% Probability of connect each node, worst case 
    test_DFS1 = test_n(2,120,0.25 ,"PATH-DFS",300)
    test_DFS1.to_csv(DATA_FOLDER/'test_DFS_n1.csv', index=False)

    # 50% Probability of connect each node
    test_DFS2 = test_n(2,120,0.5,"PATH-DFS", 300)
    test_DFS2.to_csv(DATA_FOLDER/'test_DFS_n2.csv', index=False)

    # 100% Probability of connect each node, worst case 
    test_DFS3 = test_n(2,120,1.0,"PATH-DFS",300)
    test_DFS3.to_csv(DATA_FOLDER/'test_DFS_n3.csv', index=False)

    # Plot graph
    plot_dataframes({'PATH-DFS (p = %.1f)' % 0.25: test_DFS1, 'PATH-DFS (p = %.1f)' % 0.5: test_DFS2, 'PATH-DFS (p = %.1f)' % 1.0: test_DFS3}, 'n', 'duration', IMAGE_FOLDER/'performance_DFS_n.svg')

    print('Ploted DFS according to n')
    

    #----PATH-DFS test p----
    
    # 50% Probability of connect each node 
    test_DFS = test_p(200,"PATH-DFS", 300)
    test_DFS.to_csv(DATA_FOLDER/'test_DFS_p.csv', index=False)

    # Plot graph
    plot_dataframes({'PATH-DFS (n =  %.1f)' % 200: test_DFS}, 'p', 'duration', IMAGE_FOLDER/'performance_DFS_p.svg')

    logger.info("Testing PATH-FW...")
    
    

    #----PATH-FW test n----
    
    
    # 25% Probability of connect each node, worst case 
    test_DFS1 = test_n(2,120,0.25 ,"PATH-FW",300)
    test_DFS1.to_csv(DATA_FOLDER/'test_FW_n1.csv', index=False)

    # 50% Probability of connect each node
    test_DFS2 = test_n(2,120,0.5,"PATH-FW", 300)
    test_DFS2.to_csv(DATA_FOLDER/'test_FW_n2.csv', index=False)

    # 100% Probability of connect each node, worst case 
    test_DFS3 = test_n(2,120,1.0 ,"PATH-FW",300)
    test_DFS3.to_csv(DATA_FOLDER/'test_FW_n3.csv', index=False)
    
    # Plot graph
    plot_dataframes({'PATH-FW (p = %.1f)' % 0.25: test_DFS1, 'PATH-DFS (p = %.1f)' % 0.5: test_DFS2, 'PATH-DFS (p = %.1f)' % 1.0: test_DFS3}, 'n', 'duration', IMAGE_FOLDER/'performance_FW_n.svg')
    

    #----PATH-FW test p----
    
    # 50% Probability of connect each node 
    test_FW = test_p(200,"PATH-FW", 300)
    test_FW.to_csv(DATA_FOLDER/'test_FW_p.csv', index=False)

    # Plot graph
    plot_dataframes({'PATH-FW (n =  %.1f)' % default_n: test_FW}, 'p', 'duration', IMAGE_FOLDER/'performance_FW_p.svg')
    logger.info("Testing PATH-CLIQUE...")

    

    #----CLIQUE test n----
    
    # 25% Probability of connect each node, worst case 
    test_DFS1 = test_n(2,120,0.25 ,"CLIQUE",300)
    test_DFS1.to_csv(DATA_FOLDER/'test_CLIQUE_n1.csv', index=False)

    # 50% Probability of connect each node
    test_DFS2 = test_n(2,120,0.5,"CLIQUE",300)
    test_DFS2.to_csv(DATA_FOLDER/'test_CLIQUE_2.csv', index=False)

    # 100% Probability of connect each node, worst case 
    test_DFS3 = test_n(2,120,1.0 ,"CLIQUE",300)
    test_DFS3.to_csv(DATA_FOLDER/'test_CLIQUE_n3.csv', index=False)
    
    # Plot graph
    plot_dataframes({'CLIQUE (p = %.1f)' % 0.25: test_DFS1, 'CLIQUE (p = %.1f)' % 0.5: test_DFS2, 'CLIQUE (p = %.1f)' % 1.0: test_DFS3}, 'n', 'duration', IMAGE_FOLDER/'performance_CLIQUE_n.svg')
    

    #----CLIQUE test p----
    
    # 50% Probability of connect each node 
    logger.info("Testing PATH-CLIQUE...")
    test_FW = test_p(200,"CLIQUE", 300)
    test_FW.to_csv(DATA_FOLDER/'test_CLIQUE_p.csv', index=False)

    # Plot graph
    plot_dataframes({'PATH-FW (n =  %.1f)' % default_n: test_FW}, 'p', 'duration', IMAGE_FOLDER/'performance_CLIQUE_p.svg')
    

    #----SAT test n----
    logger.info("Testing SAT-CLIQUE...")
    test_SAT, test_SAT_t = test_sat()
    plot_dataframes(
        {"total duration": test_SAT, "transformation": test_SAT_t},
        x_column="iteration",
        y_column="time",
        save_file=IMAGE_FOLDER/'performance_SAT.svg'
    )




