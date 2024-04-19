#include "graph.hpp"

#include <random>
#include <functional>
#include <set>
#include <limits>
#include <algorithm>
#include <array>
#include <iostream>


std::random_device rd;
std::uniform_int_distribution<int> dist(1, 100);
std::mt19937 engine(rd()); // Mersenne twister MT19937
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


void Graph::add_node(std::initializer_list<int> node) {
    std::vector<int> new_node {node};

    // update edges
    for (size_t i = 0; i < edges.size(); ++i) {
        edges[i].push_back(new_node[i]);
    }

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


bool Graph::_path_dfs(int u, int v, std::set<int> & visited) const{
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

    // constexpr int infinity {std::numeric_limits<int>::max()};
    const int infinity = 100;

    // initialize distances to infinity
    std::vector<std::vector<int>> distance {};
    distance.resize(edges.size());
    for (auto & vec : distance) {
        vec.resize(edges.size(), infinity);
    }

    // set weights
    for (size_t u = 0; u < edges.size(); ++u) {
        for (size_t v = 0; v < edges.size(); ++v) {
            if (u == v) {
                distance[u][v] = 0;
            }
            else if (edges[u][v] == 1) {
                distance[u][v] = 1;
            }
        }
    }

    for (size_t k = 0; k < edges.size(); ++k) {
        for (size_t i = 0; i < edges.size(); ++i) {
            for (size_t j = 0; j < edges.size(); ++j) {
                distance[i][j] = std::min(distance[i][j], distance[i][k] + distance[k][j]);
            }
        }
    }

    return distance[u][v] < infinity;
}
