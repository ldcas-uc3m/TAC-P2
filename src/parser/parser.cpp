#include "parser.hpp"

#include <string>
#include <vector>
#include <cstring>
#include <cstdlib>
#include <iostream>


std::string FLAGhelpstring = "";



void parseFlag(int argc, char** argv, std::string name, bool & val) {
  std::string token;
  bool found = false;
  for (int i = 1; i < argc; ++i) {
    token = std::string(argv[i]);
    if (found) {
      if(token.find("--") == 0) {
        val = true;
        return;
      }

      val = (token.compare("true") == 0);
      return;
    }
    if (token.compare("--" + name) == 0) {
      if (i == argc - 1) {
        // If this is the last flag in the list
        val = true;
        return;
      }
      found = true;
    }
    if (token.compare("--no" + name) == 0) {
      val = false;
      return;
    }
  }
}


void parseFlag(int argc, char** argv, std::string name, float & val) {
  std::string token;
  bool found = false;
  for (int i = 1; i < argc; ++i) {
    token = std::string(argv[i]);
    if (found) {
      val = std::atof(argv[i]);
      return;
    }
    if (token.contains("--" + name)) {
      if (token.contains("=")) {  // check for arg=value
        val = std::stof(token.substr(token.find("=") + 1));
        return;
      }
      found = true;
    }
  }
}


void parseFlag(int argc, char** argv, std::string name, int & val) {
  std::string token;
  bool found = false;
  for (int i = 1; i < argc; ++i) {
    token = std::string(argv[i]);
    if (found) {
      val = std::atoi(argv[i]);
      return;
    }
    if (token.contains("--" + name)) {
      if (token.contains("=")) {  // check for arg=value
        val = std::stoi(token.substr(token.find("=") + 1));
        return;
      }
      found = true;
    }
  }
}


void parseFlag(int argc, char** argv, std::string name, std::string & val) {
  std::string token;
  bool found = false;
  for (int i = 1; i < argc; ++i) {
    token = std::string(argv[i]);
    if (found) {
      val = token;
      return;
    }
    if (token.contains("--" + name)) {
      if (token.contains("=")) {  // check for arg=value
        val = token.substr(token.find("=") + 1);
        return;
      }
      found = true;
    }
  }
}


void parseFlag(int argc, char** argv, std::string name, std::vector<float> & val) {
  std::string token;
  bool found = false;
  for (int i = 1; i < argc; ++i) {
    token = std::string(argv[i]);
    if (found) {
      char* tk = std::strtok(argv[i], ":");
      while (tk != NULL) {
        val.push_back(std::atof(tk));
        tk = strtok(NULL, ":");
      }
      return;
    }
    if (token.compare("--" + name) == 0) {
      found = true;
    }
  }
}


void parseFlag(int argc, char** argv, std::string name, std::vector<std::string> & val) {
  std::string token;
  bool found = false;
  for (int i = 1; i < argc; ++i) {
    token = std::string(argv[i]);
    if (found) {
      char* tk = std::strtok(argv[i], ":");
      while (tk != NULL) {
        val.push_back(std::string(tk));
      }
      return;
    }
    if (token.compare("--" + name) == 0) {
      found = true;
    }
  }
}
