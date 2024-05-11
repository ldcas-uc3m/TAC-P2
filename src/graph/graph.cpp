#include "graph.hpp"

#include <random>
#include <functional>
#include <set>
#include <limits>
#include <algorithm>
#include <array>
#include <iostream>
#include <regex>
#include <cmath>



std::random_device rd;
std::uniform_int_distribution<int> dist(1, 100);
std::mt19937 engine(rd());  // Mersenne twister MT19937
auto generator = std::bind(dist, engine);


inline bool random(float prob) {
    if (prob == 1) return true;
    return (static_cast<float>(generator()) / 100.0) < prob;
}



void Graph::init(std::initializer_list<std::initializer_list<int>> new_nodes) {
    edges.clear();
    for (auto & node : new_nodes) {
        edges.push_back(node);
    }
}


void Graph::add_node(std::vector<int> adj_nodes) {
    std::vector<int> new_node {};

    int edge;

    // add adjacent nodes
    size_t j = 0;  // counter for adj_nodes
    for (size_t i = 0; i < size(); ++i) {
        if (adj_nodes.size() > 0 && (static_cast<int>(i) == adj_nodes[j])) {  // there is an edge
            edge = 1;
            if (j < adj_nodes.size()) ++j;
        }
        else edge = 0;

        edges[i].push_back(edge);
        new_node.push_back(edge);
    }

    new_node.push_back(0);  // link to self

    edges.push_back(new_node);
}



void RandomUndirectedGraph::add_random_node(float prob_edge) {
    assert(prob_edge > 0 && prob_edge <= 1);

    if (edges.empty()) {  // initialize
        edges.push_back({0});
        return;
    }

    // create new empty node
    std::vector<int> new_node {};

    // randomly connect nodes to new one
    for (size_t i = 0; i < edges.size(); ++i) {
        int edge = static_cast<int>(random(prob_edge));

        edges[i].push_back(edge);
        new_node.push_back(edge);
    }

    new_node.push_back(0);  // it's not connected to itself
    edges.push_back(new_node);

}




/* PATH(u,v) */


bool Graph::_path_dfs(int u, int v, std::set<int> & visited) const {
    if (u == v) return true;
    visited.insert(u);

    // check adjacent nodes
    for (size_t i = 0; i < edges.size(); ++i) {
        if (edges[i][u] == 1 && !visited.contains(i)) {
            if (_path_dfs(i, v, visited)) return true;
        }
    }

    return false;
}

bool Graph::path_dfs(int u, int v) const {
    // wrapper that initializes the set
    assert(u < static_cast<int>(edges.size()));
    assert(v < static_cast<int>(edges.size()));

    std::set<int> visited {};
    return _path_dfs(u, v, visited);
}




bool Graph::path_fw(int u, int v) const {
    assert(u < static_cast<int>(edges.size()));
    assert(v < static_cast<int>(edges.size()));

    if (u == v) return true;

    constexpr int infinity {std::numeric_limits<int>::max()};

    std::vector<std::vector<int>> distance {};

    // initialize distances
    for (size_t u = 0; u < edges.size(); ++u) {
        distance.push_back({});
        distance[u].reserve(edges.size());
        for (size_t v = 0; v < edges.size(); ++v) {
            int d;
            if (u == v) {
                d = 0;
            }
            else if (edges[u][v] != 0) {
                d = edges[u][v];
            }
            else d = infinity;

            distance[u].push_back(d);
        }
    }

    // compute distances
    for (size_t k = 0; k < edges.size(); ++k) {
        for (size_t i = 0; i < edges.size(); ++i) {
            for (size_t j = 0; j < edges.size(); ++j) {
                if ((distance[i][k] == infinity) || (distance[k][j] == infinity)) continue;
                distance[i][j] = std::min(distance[i][j], distance[i][k] + distance[k][j]);
            }
        }
    }

    return distance[u][v] < infinity;
}


/* K_CLIQUE(k) */


inline int Graph::degree(int i) const {
    return std::count_if(edges[i].begin(), edges[i].end(), [](int i) { return i > 0; });
}


bool Graph::k_clique(int k) const {
    std::vector<int> subgraph {};
    return _k_clique(0, subgraph, k);
}



bool Graph::_k_clique(int i, std::vector<int> & subgraph, int k) const {
    for (size_t j = i; j < size(); ++j) {
        if (degree(i) >= k - 1) {
            subgraph.push_back(j);  // add current node to clique subgraph

            if (is_connected(j, subgraph)) {  // new node forms clique
                if (static_cast<int>(subgraph.size()) < k) {  // continue searching
                    _k_clique(j, subgraph, k);
                }
                else {
                    return true;
                }
            }
        }
    }

    return false;
}


bool Graph::is_connected(int i, std::vector<int> & list) const {
    if (list.size() == 0) return true;

    for (auto & j : list) {
        if (edges[i][j] == 0) {
            if (i == j) continue;
            return false;
        }
    }
    return true;
}



bool Graph::is_clique(std::vector<int> & graph) const {
    for (size_t i = 0; i < graph.size(); ++i) {
        for (size_t j = i + 1; j < graph.size(); ++j) {
            if (edges[i][j] == 0) {
                return false;
            }
        }
    }

    return true;
}




/* K-SAT to K-Clique */

std::tuple<Graph, size_t> sat_to_clique(const std::string & problem) {
    // TODO: validate problem format

    // extract vars
    std::vector<std::string> vars;

    const std::regex re_vars(R"((-?[a-z]))");
    std::smatch match;

    std::sregex_iterator start {problem.cbegin(), problem.cend(), re_vars};
    std::sregex_iterator end;

    for (auto i = start; i != end; ++i) {
        vars.push_back(i->str());
        // std::cout << i->str() << ", ";
    }

    const auto k = static_cast<size_t>(std::sqrt(vars.size()));
    assert(vars.size() == k * k);  // check k perfect square (correct number of vars)

    // generate graph
    Graph g {};
    std::vector<std::string> in_vars;

    for (size_t i = 0; i < vars.size(); ++i) {
        std::vector<int> adj_nodes {};

        // compute inverse of element
        std::string el = vars[i];
        std::string not_el;
        if (el[0] == '-') {
            not_el = el[1];
        }
        else not_el = '-' + el;

        // connect to rest of graph
        for (size_t j = 0; j < in_vars.size(); ++j) {
            if (i / k == j / k) continue;  // don't connect if same group
            if (in_vars[j] != not_el) adj_nodes.push_back(j);
        }

        g.add_node(adj_nodes);

        in_vars.push_back(std::move(vars[i]));
    }

    // std::cout << g << "\n";
    // print_v(in_vars);
    // std::cout << "\n";

    return {g, k};
}



template <typename T>
inline void print_v(const std::vector<T> & container) {
    std::cout << '[';
    for (auto it = container.begin(); it != container.end(); ++it) {
        std::cout << *it;
        if (std::next(it) != container.end()) std::cout << ", ";
    }
    std::cout << ']';
}