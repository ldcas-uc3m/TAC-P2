# Práctica 2: Algoritmos aplicados a Grafos
By Ignacio Arnaiz Tierraseca & Luis Daniel Casais Mezquida  
Teoría Avanzada de la Computación 23/24  
Bachelor's Degree in Computer Science and Engineering  
Universidad Carlos III de Madrid


## Enunciado de la práctica
En esta práctica se propone estudiar varios algoritmos que se aplican a resolver problemas en Grafos. Se pide aplicar los conocimientos adquiridos en Magistral, en especial Análisis de Coste Computacional, pero también algunas cuestiones de Complejidad Computacional.

Los problemas seleccionados son:
- `PATH(u,v)`: determinar si existe un camino entre dos nodos cualesquiera de un grafo.
- `CLIQUE(G)`: obtener el subgrafo de mayor tamaño en el que los nodos estén completamente interconectados.

La elección de estos problemas se debe a que ambos se pueden relacionar con 2SAT y 3SAT por lo que también se pueden estudiar reducciones. De esta forma se cubren diversos aspectos de Complejidad Computacional (clases P y NP-C, reducciones).  
En Magistral se comentarán algunos aspectos sobre dichos problemas.

También se plantearán algunas variantes asociadas, como el MST (Minimum Spanning Tree), o la valoración de arcos del grafo dado que forman parte de muchos algoritmos de resolución al uso.

Para comenzar sería recomendable repasar los conceptos de Matrices de Adyacencia y el algoritmo DFS (_Depth First Search_).

El alumno deberá implementar y analizar los algoritmos. Se puede basar en librerías existentes, pero se entiende que los algoritmos más sencillos no deberían representar un problema en cuanto a su implementación, por lo que será un aspecto que se valorará. Las librerías deben servir de apoyo para funciones de gestión y algoritmos más complejos.

### Tarea 1
Diseñar funciones que generen grafos permitiendo añadir arcos valuados que conectan nodos siguiendo algún esquema, Por ejemplo, con un valor de conectividad determinado, siguiendo alguna distribución aleatoria, etc. Los valores de los arcos se deben poder inicializar a 0 o 1, o con valores aleatorios enteros dentro de un rango. Debe existir la posibilidad de que los valores entre cada par de nodos sean iguales (grafo no dirigido, matriz simétrica).

### Tarea 2
Implementar una función para aplicar DFS, y determinar si dos nodos dados están conectados.

### Tarea 3
Generalizar mediante un algoritmo de cierre transitivo o tipo _Floyd-Warshall_ que permita determinar qué nodos están conectados entre sí a uno o más pasos.

### Tarea 4
Determinar el coste computacional de los algoritmos diseñados. Incluir desarrollo analítico, estudio empírico, tablas y gráficas.

### Tarea 5
Implementar una función para buscar el subgrafo _Clique_. Este algoritmo puede requerir un coste computacional elevado. Se pueden plantear métodos de fuerza bruta como backtracking, pero es conveniente usar heurísticas y podas, o recurrir a métodos más elaborados.

### Tarea 6
Determinar el coste computacional de los algoritmos diseñados. Incluir desarrollo analítico, estudio empírico, tablas y gráficas.

### Tarea 7
Implementar un pequeño Sat-Solver a través de la resolución del problema K-Clique.  
Para ello debemos disponer:
- Del procedimiento que determina la existencia de un grafo de tipo k-clique
- Un procedimiento que lea del input una ecuación lógica que cumpla las especificaciones de 3-SAT.  
  Los símbolos que debemos contemplar son:
    - letras minúscula para las variables
    - paréntesis para delimitar las cláusulas
    - conectivas: `*` (AND), `+` (OR) y `-` (NOT)
- El procedimiento de k-clique podrá proporcionar tanto si la ecuación es satisfacible, como una solución a la misma
- Este Sat-Solver tendrá limitaciones respecto al tamaño de problemas que pueda abordar. No se pide implementar heurísticas elaboradas, pero hay alguna optimización fácil de implementar (eliminar los literales repetidos de una misma cláusula).


### Tarea 8
Estudio para PATH:
1. Determinar cómo se comportan las distancias mínimas para todo el grafo cuando se varía la conectividad de los nodos
2. Determinar el Coste Computacional de obtener PATH(p,q) para todos los nodos del grafo cuando
    1. éste aumenta de tamaño
    2. varía la conectividad para un tamaño fijado

### Tarea 9
Estudio de k-Clique. Se pide algo similar. Incluir estudio en su vertiente de Sat-Solver.



## Installation and execution


### Running the C++ simulator
<!-- TODO -->


### Running the Python tests
This requires Python 3.10+.

1. Create a Python virtual enviroment in the `.venv` folder:
    ```bash
    python3 -m venv ./.venv
    ```
2. Activate the virtual enviroment:
   - Linux:
        ```bash
        source .venv/bin/activate
        ```
    - Windows (PowerShell):
        ```powershell
        & .\.venv\Scripts\Activate.ps1
        ```
3. Install the dependencies
   ```
   pip install -r requirements.txt
   ```
4. Compile the C++ simulator with CMake. Make sure you install [CMake](https://cmake.org/) and [GCC 11+](https://gcc.gnu.org/) (C++23).  
   If you're in Windows, we recommend you to install [WSL2](https://learn.microsoft.com/es-es/windows/wsl/install) and run "in Linux", or use GCC through [MinGW-W64](https://www.mingw-w64.org/), you can find compiled binaries in the [niXman/mingw-builds-binaries repo](https://github.com/niXman/mingw-builds-binaries).  
   Build:
    - Linux (through [make](https://www.gnu.org/software/make/manual/make.html)):
        ```powershell
        cd build
        cmake ..
        make
        ```
    - Windows/Linux (through [ninja-build](https://ninja-build.org/)):
        ```powershell
        cd build
        cmake .. -G Ninja
        cmake --build .
        ```
5. Run the tests.
   ```
   python3 src/test.py
   ```