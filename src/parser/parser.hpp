#ifndef PARSER_HPP
#define PARSER_HPP

#include <string>
#include <vector>
#include <iostream>



#define CHECK(cond, message) \
if (!(cond)) { \
  std::cerr << "\033[1;31m[FATAL ERROR]  " << #cond << " : " << message << "\033[0m" << std::endl << "\t\t" << std::endl; \
  std::abort(); \
}



extern std::string FLAGhelpstring;


#define DEFINE_FLAG(type, flag_name, default_value, description) \
std::string FLAGname_##flag_name = #flag_name; \
std::string FLAGhelp_##flag_name = description; \
std::string FLAGdefaultvalue_##flag_name = #default_value; \
type FLAG_##flag_name = default_value;

#define DEFINE_bool(flag_name, default_value, description) \
DEFINE_FLAG(bool, flag_name, default_value, description)

#define DEFINE_string(flag_name, default_value, description) \
DEFINE_FLAG(std::string, flag_name, default_value, description)

#define DEFINE_float(flag_name, default_value, description) \
DEFINE_FLAG(float, flag_name, default_value, description)

#define DEFINE_int(flag_name, default_value, description) \
DEFINE_FLAG(int, flag_name, default_value, description)

#define DEFINE_vec_float(flag_name, default_value, description) \
DEFINE_FLAG(std::vector<float>, flag_name, default_value, description)

#define REGISTER_FLAG(argc, argv, flag_name) \
FLAGhelpstring.append("\n  --" #flag_name " ["); \
FLAGhelpstring.append(FLAGdefaultvalue_##flag_name); \
FLAGhelpstring.append("]\t"); \
FLAGhelpstring.append(FLAGhelp_##flag_name); \
parseFlag(argc, argv, FLAGname_##flag_name, FLAG_##flag_name);

inline void flaghelp() { std::cout << FLAGhelpstring << std::endl; }


void parseFlag(int argc, char** argv, std::string name, bool & val);

void parseFlag(int argc, char** argv, std::string name, float & val);

void parseFlag(int argc, char** argv, std::string name, int & val);

void parseFlag(int argc, char** argv, std::string name, std::string & val);

void parseFlag(int argc, char** argv, std::string name, std::vector<float> & val);

void parseFlag(int argc, char** argv, std::string name, std::vector<std::string> & val);


#endif