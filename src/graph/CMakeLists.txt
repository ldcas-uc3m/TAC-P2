add_library(Graph STATIC)

target_sources (
    Graph

    PUBLIC
        graph.hpp
    PRIVATE
        graph.cpp
)