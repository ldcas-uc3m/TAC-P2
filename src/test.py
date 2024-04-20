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

def test(n: int, p: Annotated[float, "0 < p < 1"], algorithm: Literal["DFS", "PATH-DFS", "PATH-FW", "CLIQUE", "SAT-CLIQUE"], iterations: int) -> pd.DataFrame:
    """
    Creates random graphs of size `n` with probability of edges `p`, and applies the selected algorithm for the specified number of `iterations`.

    :param n: Size of the graph.
    :param p: Probability of an edge between two nodes, between `0` and `1`.
    :param algorithm: Algorithm to apply.
    :param iterations: Number of tests.

    :return: DataFrame with columns {n, result, duration}
    """

    results = pd.DataFrame(
        columns=[
            'n',
            'result',
            'duration'
        ]
    )

    tests: dict = json.loads(subprocess.check_output([
        SIMULATOR_EXEC,
        f"--n={n}",
        f"--p={p}",
        f"--algorithm={algorithm}",
        f"--iterations={iterations}",
        "--nograph"
    ]))['tests']

    for t in tests:
        # append to df
        results.loc[len(results)] = {
            'n': n,
            'result': t['result'],
            'duration': t['duration']
        }


    return results



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

    # Crear el gráfico
    fig, ax = plt.subplots()

    for name, df in dfs.items():
        # print(dfs.items())
        ax.plot(df[x_column], df[y_column], marker='o', label=name)


        if x_column == 'n':
        # Añadir ticks en el eje x para cada punto único en los datos de x
            x_ticks = df[x_column].dropna().astype(int).unique()  # Asegura la conversión a int
        else:
            x_ticks = df[x_column].dropna().astype(float).unique()
        ax.set_xticks(x_ticks)

    # Determinar la paleta de colores dependiendo del número de series de datos
    if len(dfs) <= len(mcolors.BASE_COLORS):
        palette = mcolors.BASE_COLORS
    else:
        palette = mcolors.XKCD_COLORS

    ax.set_prop_cycle(color=palette)

    # Agregar etiquetas
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column + ' (ns)')

    ax.legend()

    if save_file:
        fig.savefig(save_file)
    else:
        fig.show()

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

def test_n (n_min, n_max, probability, algorithm, n_tests):
    """
    Function to calculate the average duration depending on the n size (Nomber of vertices of the graph)
    """

    # Datframe to save the result
    results = pd.DataFrame(
        columns=[
            'n',
            'duration'
        ]
    )

    
    for n in range(n_min, n_max+1):

        print(f"n: {n}, p: {probability}", end='\r')

        #Run a battery of tests with the n given and the n_tests number of times given
        run = test(n, probability, algorithm, n_tests)
        
        #Take the average duration for each n size
        average_durations = run['duration'].mean()

        #Save the results into a dataframe
        new_row = pd.DataFrame({
            'n': [n],
            'duration': [average_durations]
        })
        results = pd.concat([results, new_row], ignore_index=True)

        sys.stdout.write("\033[K")  # clear line

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

        p+=0.1

        sys.stdout.write("\033[K")  # clear line

    #print(results)
    return results



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
    
    # 50% Probability of connect each node
    test_DFS = test_n(2,20,default_probability,"PATH-DFS", 300)
    test_DFS.to_csv(DATA_FOLDER/'test_DFS_n.csv', index=False)

    # 100% Probability of connect each node, worst case 
    test_DFS_worst = test_n(2,20,DFS_worst_probability ,"PATH-DFS",300)
    test_DFS_worst.to_csv(DATA_FOLDER/'test_DFS_n_worst.csv', index=False)

    # Plot graph
    plot_dataframes({'PATH-DFS (p = %.1f)' % default_probability: test_DFS, 'PATH-DFS-WORST-CASE (p = %.1f)' % DFS_worst_probability: test_DFS_worst}, 'n', 'duration', IMAGE_FOLDER/'performace_DFS_n.svg')


    #----PATH-DFS test p----
    
    # 50% Probability of connect each node 
    test_DFS = test_p(default_n,"PATH-DFS", 500)
    test_DFS.to_csv(DATA_FOLDER/'test_DFS_p.csv', index=False)

    # Plot graph
    plot_dataframes({'PATH-DFS (n =  %.1f)' % default_n: test_DFS}, 'p', 'duration', IMAGE_FOLDER/'performace_DFS_p.svg')

    logger.info("Testing PATH-FW...")


    #----PATH-FW test n----

    # 50% Probability of connect each node 
    test_FW = test_n(2,20,default_probability,"PATH-FW",300)
    test_FW.to_csv(DATA_FOLDER/'test_FW_n.csv', index=False)


    #test_FW_worst= test_n(2,20,1,"PATH-FW",300)

    # Plot graph
    plot_dataframes({'PATH-FW (p = %.1f)' % default_probability: test_FW}, 'n', 'duration', IMAGE_FOLDER/'performace_FW_n.svg')

    #----PATH-FW test p----
    
    # 50% Probability of connect each node 
    test_FW = test_p(default_n,"PATH-FW", 500)
    test_FW.to_csv(DATA_FOLDER/'test_FW_p.csv', index=False)


    # Plot graph
    plot_dataframes({'PATH-FW (n =  %.1f)' % default_n: test_FW}, 'p', 'duration', IMAGE_FOLDER/'performace_FW_p.svg')

    # TODO: save data to CSV
