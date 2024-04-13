import subprocess
from pathlib import Path
import json
import os
import platform
import logging
from typing import Callable
from itertools import product

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
# TURING_EXEC: Path = REPO_ROOT/f"turing-machine-simulator/turing{'.exe' if platform.system() == 'Windows' else ''}"
DATA_FOLDER = REPO_ROOT/"data/"
TM_FOLDER = REPO_ROOT/"src/tm/"

if os.path.exists(REPO_ROOT/"report"):
    IMAGE_FOLDER = REPO_ROOT/"report/img/"
else:
    IMAGE_FOLDER = DATA_FOLDER/"img"
    os.mkdir(IMAGE_FOLDER)




# ==============
# TEST FUNCTIONS
# ==============

# def tests(file: Path, inputs: list[str], ntapes: int = 0) -> pd.DataFrame:
#     """
#     Runs the specified `inputs` through the Turing Machine in `file`, on the Turing Machine simulator in `TURING_EXEC`, and returns the results.

#     :param file: Turing machine definition file path, in turingmachinesimulator.com format.
#     :param inputs: List of inputs to the TM.
#     :param ntapes: Number of tapes of the TM.

#     :return: DataFrame with columns {n, steps, result}
#     """

#     results = pd.DataFrame(
#         columns=[
#             'input',
#             'n',
#             'steps',
#             *[f'result{i}' for i in range(ntapes)]
#         ]
#     )

#     for input in inputs:
#         tm_result = json.loads(subprocess.check_output([TURING_EXEC, str(file), input, "--json"]))

#         if not tm_result["accepted"]:
#             logger.error(f"Input '{input}' for TM {file} was not accepted")
#             continue

#         r = {
#             'input': input,
#             'n': len(input),
#             'steps': tm_result["steps"],
#             **{f'result{i}': tm_result["tapes"][i].strip("_") for i in range(ntapes)}
#         }


#         # append to results
#         results.loc[len(results)] = r


#     return results



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
        ax.plot(df[x_column], df[y_column], marker='o', label=name)

    # automatic colors
    if len(dfs) <= len(mcolors.BASE_COLORS):
        pallete = mcolors.BASE_COLORS
    else:
        pallete = mcolors.XKCD_COLORS

    ax.set_prop_cycle(color=pallete)

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






if __name__ == "__main__":
    # if not TURING_EXEC.exists():
    #     exit(f"TM simulator executable not found at {TURING_EXEC}. Have you run make?")

    pass
