add_library(Parser STATIC)

target_sources (
    Parser

    PUBLIC
        parser.hpp
    PRIVATE
        parser.cpp
)