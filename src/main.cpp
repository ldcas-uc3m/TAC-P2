
#include <iostream>
#include <string>
#include <functional>
#include <sstream>
#include <chrono>
#include <cmath>
#include <algorithm>

#include "graph/graph.hpp"
#include "parser.hpp"




/* TESTS */

using path_t = std::function<bool(const RandomUndirectedGraph &, int, int)>;  // PATH function wrapper
using clique_t = std::function<bool(const RandomUndirectedGraph &, int)>;  // CLIQUE function wrapper

// template <typename F>
// concept executable_function = requires (F f) {
//     f();
// };


/**
* @brief generates a RandomUndirectedGraph and tests the performance of a PATH algorithm, outputting it to stdout in JSON format
*/
void test_path(int n, float p, int iter, int u, int v, path_t func, bool print_graph) {
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


/**
* @brief generates a RandomUndirectedGraph and tests the performance of a CLIQUE algorithm, outputting it to stdout in JSON format
*/
void test_clique(int n, float p, int iter, int k, clique_t func, bool print_graph) {
    std::cout << "{";
    std::cout << "\"n\":" << n << ",";
    std::cout << "\"p\":" << p << ",";
    std::cout << "\"k\":" << k << ",";

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
        bool result = func(graph, k);
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
DEFINE_string(algorithm, "CLIQUE", "algorithm to apply (PATH-DFS, PATH-FW, CLIQUE, SAT-CLIQUE)");
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

    // algorithm name to uppercase
    std::transform(FLAG_algorithm.begin(), FLAG_algorithm.end(), FLAG_algorithm.begin(), ::toupper);

    // run tests

    /* PATH */
    if (FLAG_algorithm.contains("PATH")) {
        const int v = FLAG_n - 1;
        const int u = 0;
        path_t f;

        if (FLAG_algorithm == "PATH-DFS") { 
            path_t f = &RandomUndirectedGraph::path_dfs;
        }
        else if (FLAG_algorithm == "PATH-FW") {
            f = &RandomUndirectedGraph::path_fw;
        }
        else {
            std::cerr << "Unknown algorithm '" << FLAG_algorithm << "'\n";
            return -1;
        }

        test_path(FLAG_n, FLAG_p, FLAG_iterations, u, v, f, FLAG_graph);
    }
    /* CLIQUE */
    else if (FLAG_algorithm.contains("CLIQUE")) {
        const int k = std::floor(FLAG_n / 2);
        clique_t f;

        if (FLAG_algorithm == "CLIQUE") {
            f = &RandomUndirectedGraph::k_clique;
        }
        else {
            std::cerr << "Unknown algorithm '" << FLAG_algorithm << "'\n";
            return -1;
        }
        test_clique(FLAG_n, FLAG_p, FLAG_iterations, k, f, FLAG_graph);
    }
    else {
        std::cerr << "Unknown algorithm '" << FLAG_algorithm << "'\n";
        return -1;
    }

    return 0;

}