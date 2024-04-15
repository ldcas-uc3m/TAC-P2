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
        Graph(): nodes {} { }

        /* setup functions */

        /**
        * @brief initializes the graph with the specified nodes and edges
        */
        void init(std::initializer_list<std::initializer_list<int>> new_nodes);

        /**
        * @brief adds a node to the graph
        */
        void add_node(std::initializer_list<int> node);

        /**
        * @brief clears the graph
        */
        void clear() { nodes.clear(); }


        /* overload << operator */
        friend std::ostream & operator << (std::ostream & out, Graph const & graph) {
            out << "{";
            for (size_t i = 0; i < graph.nodes.size(); ++i) {
                // print connected nodes
                out << i << ": " << "[";
                size_t j = 0;
                for (auto & node : graph.nodes[i]) {
                    out << node;
                    if (j < graph.nodes[i].size() - 1) {  // not last element
                        out << ", ";
                    }
                    ++j;
                }
                out << "]";

                if (i < graph.nodes.size() - 1) {  // not last element
                    out << ", ";
                }
            }
            out << "}";

            return out;
        }


        /* PATH implementations */

        /**
        * @brief PATH(u, v) using Depth First Search
        */
        bool path_dfs(int u, int v);


    protected:  // can be accessed by children
        std::vector<std::set<int>> nodes;  // list of adjacent nodes (for each node)

        bool _path_dfs(int u, int v, std::set<int> & visited);
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