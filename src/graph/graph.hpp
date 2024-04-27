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
        size_t size() const { return edges.size(); }


        /* overload << operator */
        friend std::ostream & operator << (std::ostream & out, const Graph & graph) {
            out << "[";
            for (size_t i = 0; i < graph.edges.size(); ++i) {
                // print connected nodes
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


        /**
        * @brief PATH(u, v) using Floyd-Warshall
        */
        bool path_fw(int u, int v) const;


        /* K-CLIQUE implementations */

        /**
         * @brief checks if there is a complete subgraph of size k
        */
        bool k_clique(int k) const;


    protected:  // can be accessed by children
        std::vector<std::vector<int>> edges;  // adjacency matrix (1 = edge, 0 = no edge)

        bool _path_dfs(int u, int v, std::set<int> & visited) const;


        /* K-CLIQUE implementations */

        bool _k_clique(int i, std::vector<int> & list, int k) const;

        /**
         * @brief checks if a subgraph is complete
        */
        bool is_clique(std::vector<int> & list) const;

        /**
         * @brief checks if a node i is connected to the rest of nodes in the list
        */
        bool is_connected(int i, std::vector<int> & list) const;

        /**
         * @brief computes the degree of a node
        */
        inline int degree(int i) const;

};



class RandomUndirectedGraph : public Graph {
    public:
        RandomUndirectedGraph(
            int n,  // number of nodes
            float prob_edge  // probability of an edge in between two nodes
            // edges is already initialized by the constructor of the parent class
        ) {
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