#ifndef GRAPH_HPP
#define GRAPH_HPP


#include <vector>
#include <cassert>
#include <ostream>
#include <iterator>
#include <set>
#include <initializer_list>



class Graph {
    public:
        Graph(): edges {} { }

        /* setup functions */

        /**
        * @brief initializes the graph with the specified adjacency matrix
        */
        void init(std::initializer_list<std::initializer_list<int>> new_nodes);

        /**
        * @brief adds a node to the graph, given the adjacency vector
        */
        void add_node(std::initializer_list<int> node);

        /**
        * @brief clears the graph
        */
        void clear() { edges.clear(); }


        /**
        * @brief returns the number of nodes
        */
        size_t size() { return edges.size(); }


        /* overload << operator */
        friend std::ostream & operator << (std::ostream & out, const Graph & graph) {
            out << "[";
            for (size_t i = 0; i < graph.edges.size(); ++i) {
                // print connected nodes
                // out << i << ": " << "[";
                out << "[";
                size_t j = 0;
                for (auto & node : graph.edges[i]) {
                    out << node;
                    if (j < graph.edges[i].size() - 1) {  // not last element
                        out << ", ";
                    }
                    ++j;
                }
                out << "]";

                if (i < graph.edges.size() - 1) {  // not last element
                    out << ", ";
                }
            }
            out << "]";

            return out;
        }


        /* PATH implementations */

        /**
        * @brief PATH(u, v) using Depth First Search
        */
        bool path_dfs(int u, int v) const;


    protected:  // can be accessed by children
        std::vector<std::vector<int>> edges;  // adjacency matrix (1 = edge, 0 = no edge)

        bool _path_dfs(int u, int v, std::set<int> & visited) const;
};



class RandomUndirectedGraph : public Graph {
    public:
        RandomUndirectedGraph(
            int n,  // number of nodes
            float prob_edge  // probability of an edge in between two nodes
        ) {  // nodes is already initialized by the constructor of the parent class
            assert(n > 0);

            for (int i = 0; i < n; ++i) {
                add_random_node(prob_edge);
            }
        }

        /**
        * @brief adds a randomized node to the graph
        */
        void add_random_node(float prob_edge);

};






#endif