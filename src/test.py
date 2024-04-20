import subprocess
from pathlib import Path
import json
import os
import platform
import logging
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
        print(dfs.items())
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
    ax.set_ylabel(y_column)

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

# Function to calculate the average duration depending on the n size (Nomber of vertices of the graph)
def test_n (n_min, n_max, probability, algorithm):

    results = pd.DataFrame(
        columns=[
            'n',
            'duration'
        ]
    )

    for n in range(n_min, n_max+1):

        durations = []

        # For each graph size, it is executed 10 times and then calculate the average execution time
        for index in range(200):
            run = test(n, probability, algorithm, 1)
            durations.append(run['duration'][0])

        avg_duration = statistics.mean(durations)
 
        #In the dataframe is saved the average time needed for each graph size
        new_values = pd.DataFrame({'n': [n], 'duration': [avg_duration]})

        results = pd.concat([results, new_values], ignore_index=True)

    return results
        

# Function to calculate the average duration depending on the n size (Nomber of vertices of the graph)
def test_p (n, algorithm):

    results = pd.DataFrame(
        columns=[
            'n',
            'p',
            'duration'
        ]
    )

    p = 0.1
    while p <= 1:

        durations = []

        # For each graph size, it is executed 10 times and then calculate the average execution time
        for index in range(200):
            run = test(n, p, algorithm, 1)
            durations.append(run['duration'][0])

        avg_duration = statistics.mean(durations)
 
        #In the dataframe is saved the average time needed for each graph size
        new_values = pd.DataFrame({'n': [n], 'p': [p], 'duration': [avg_duration]})
        p+=0.1
        print('P: ', p)
        results = pd.concat([results, new_values], ignore_index=True)

    return results



if __name__ == "__main__":
    if not SIMULATOR_EXEC.exists():
        exit(f"TM simulator executable not found at {SIMULATOR_EXEC}. Have you run CMake?")


    #----Unitary test----
    #result = test(4, 0.5, "PATH-DFS", 1)
    #print('Result: ', result['result'][0])
    #print('Duration: ', result['duration'][0])

    #----PATH-DFS test n----
    
    # 50% Probability of connect each node 
    test_DFS = test_n(2,20,0.5,"PATH-DFS")

    # 100% Probability of connect each node, worst case 
    test_DFS_worst = test_n(2,20,1,"PATH-DFS")

    # Plot graph
    plot_dataframes({'PATH-DFS': test_DFS, 'PATH-DFS-WORST-CASE': test_DFS_worst}, 'n', 'duration', IMAGE_FOLDER/'performace_DFS_n')

    #----PATH-DFS test p----
    
    # 50% Probability of connect each node 
    test_DFS = test_p(5,"PATH-DFS")

    # Plot graph
    plot_dataframes({'PATH-DFS': test_DFS}, 'p', 'duration', IMAGE_FOLDER/'performace_DFS_p')


    #----PATH-FW test n----

    # 50% Probability of connect each node 
    test_FW = test_n(2,20,0.5,"PATH-FW")

    # Plot graph
    plot_dataframes({'PATH-FW': test_FW}, 'n', 'duration', IMAGE_FOLDER/'performace_FW_n')

    #----PATH-FW test p----
    
    # 50% Probability of connect each node 
    test_FW = test_p(5,"PATH-FW")

    # Plot graph
    plot_dataframes({'PATH-FW': test_FW}, 'p', 'duration', IMAGE_FOLDER/'performace_FW_p')

    pass
