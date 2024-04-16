#include "graph.hpp"

#include <random>
#include <functional>
#include <set>


std::random_device rd;
std::uniform_int_distribution<int> dist(1, 100);
std::mt19937 engine(rd()); // Mersenne twister MT19937
auto generator = std::bind(dist, engine);


inline bool random(float prob) {
    if (prob == 1) return true;
    return (static_cast<float>(generator()) / 100.0) < prob;
}



void Graph::init(std::initializer_list<std::initializer_list<int>> new_nodes) {
    nodes.clear();
    for (auto & node : new_nodes) {
        add_node(node);
    }
}


void Graph::add_node(std::initializer_list<int> node) {
    std::set<int> new_node {node};

    // update nodes
    for (size_t i = 0; i < nodes.size(); ++i) {
        if (new_node.contains(i)) {
            nodes[i].insert(nodes.size());
        }
    }

    nodes.push_back(new_node);
}



void RandomUndirectedGraph::add_random_node(float prob_edge) {
    assert(prob_edge > 0 && prob_edge <= 1);

    // create new empty node
    std::set<int> new_node {};

    // randomly connect nodes to new one
    for (size_t i = 0; i < nodes.size(); ++i) {
        if (random(prob_edge)) {
            nodes[i].insert(nodes.size());
            new_node.insert(i);
        }
    }

    nodes.push_back(new_node);

}


bool Graph::_path_dfs(int u, int v, std::set<int> & visited) const{
    if (nodes[u].contains(v)) return true;
    visited.insert(u);

    // check adjacent nodes 
    for (auto node : nodes[u]) {
        if (!visited.contains(node)) {
            if (_path_dfs(node, v, visited)) return true;
        }
    }

    return false;
}

bool Graph::path_dfs(int u, int v) const {
    // wrapper that initializes the set
    assert(u < static_cast<int>(nodes.size()));
    assert(v < static_cast<int>(nodes.size()));

    std::set<int> visited {};
    return _path_dfs(u, v, visited);
}