# build libraries
add_subdirectory(parser)
add_subdirectory(graph)


# add compilation target
add_executable(${PROJECT_NAME} "main.cpp")


# link libraries
target_link_libraries (
    ${PROJECT_NAME}
    PUBLIC
        Parser
        Graph
)

include_directories("graph" "parser")