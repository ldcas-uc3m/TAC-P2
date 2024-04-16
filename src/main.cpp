
#include <iostream>
#include <string>
#include <functional>
#include <sstream>
#include <chrono>

#include "graph/graph.hpp"
#include "parser.hpp"




/* TESTS */

using path_f = std::function<bool(const RandomUndirectedGraph &, int, int)>;  // PATH function wrapper


/**
* @brief generates a RandomUndirectedGraph and tests the performance of a method, outputting it to stdout in JSON format
*/
void test(int n, float p, int iter, int u, int v, path_f func, bool print_graph) {
    std::cout << "{";
    std::cout << "\"n\":" << n << ",";
    std::cout << "\"p\":" << p << ",";
    std::cout << "\"u\":" << u << ",";
    std::cout << "\"v\":" << v << ",";

    std::cout << "\"tests\":[";

    for (int i = 0; i < iter; ++i) {
        std::cout << "{";

        // create graph
        RandomUndirectedGraph graph {n, p};
        if (print_graph) {
            std::cout << "\"graph\":" << graph << ",";
        }

        // run
        auto tic = std::chrono::high_resolution_clock::now();
        bool result = func(graph, u, v);
        auto toc = std::chrono::high_resolution_clock::now();

        auto duration = std::chrono::duration_cast<std::chrono::nanoseconds>(toc-tic).count();

        std::cout << "\"result\":" << (result ? "true" : "false") << ",";
        std::cout << "\"duration\":" << duration << "}";

        if (i < iter - 1) std::cout << ",";
    }

    std::cout << "]}";
}



/* CLI */

DEFINE_int(n, 5, "size of the graph");
DEFINE_float(p, 0.5, "probability of an edge between two nodes");
DEFINE_int(iterations, 1, "number of iterations to execute");
DEFINE_string(algorithm, "DFS", "algorithm to apply (DFS)");
DEFINE_bool(graph, true, "output the graph");
DEFINE_bool(help, false, "show a list of command-line options");



/* MAIN */

int main(int argc, char* argv[]) {


    // parse cli
    REGISTER_FLAG(argc, argv, n);
    REGISTER_FLAG(argc, argv, p);
    REGISTER_FLAG(argc, argv, algorithm);
    REGISTER_FLAG(argc, argv, iterations);
    REGISTER_FLAG(argc, argv, graph);
    REGISTER_FLAG(argc, argv, help);

    if (FLAG_help) {
        std::cout << "Usage:\n  " << argv[0] << " [options]\n\nOPTIONS";
        flaghelp();

        return 0;
    }

    // run tests
    const int v = FLAG_n - 1;
    const int u = 0;

    path_f f;

    if (FLAG_algorithm == "DFS") { 
        f = &RandomUndirectedGraph::path_dfs; 
    }
    else {
        std::cerr << "Unknown algorithm '" << FLAG_algorithm << "'\n";
        return -1;
    }

    test(FLAG_n, FLAG_p, FLAG_iterations, u, v, f, FLAG_graph);


}