
#include <iostream>
#include <string>

#include "graph/graph.hpp"



/* MAIN */

int main(int argc, char* argv[]) {

    RandomUndirectedGraph graph {5, 0.3};
    std::cout << graph << std::endl;

    std::string result = graph.path_dfs(0, 4) ? "true" : "false";
    std::cout << "PATH(0,4): " << result << std::endl;

    return 0;
}