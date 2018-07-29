#include "turing_common.hpp"
#include <iostream>
#include <memory>
#include <vector>

TuringMachine::TuringMachine(
        std::vector<std::shared_ptr<std::string> > alphabet,
        std::vector<std::shared_ptr<tmRule> > rules) {
    std::cout << "TuringMachine constructor placeholder" << std::endl;
}

