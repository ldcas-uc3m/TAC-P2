# create libraries
add_library(Graph STATIC)


# give every library access to src/
target_include_directories(Graph PUBLIC ${CMAKE_CURRENT_LIST_DIR})


# build libraries
add_subdirectory(graph)


# add compilation target
add_executable(${PROJECT_NAME} "main.cpp")


# link libraries
target_link_libraries (
    ${PROJECT_NAME}
    PUBLIC
        Graph
)

include_directories("graph")