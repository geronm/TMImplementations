#include "turing_common.hpp"
#include <iostream>
#include <vector>

// enum tmDirection {left, right, noop, halt_accept, halt_reject};

// struct tmRule {
//     std::string state_from;
//     std::string input_from;
//     std::string state_to;
//     std::string input_to;
//     std::string direction;
// };

TuringMachine::TuringMachine(std::vector<std::string> alphabet,
                  std::vector<tmRule> rules) {
        std::cout << "Here we are" << std::endl;
}



// class TuringMachine {

//     public:

//     TuringMachine(std::vector<std::string> alphabet,
//                   std::vector<tmRule> rules) {
//         std::cout << "Here we are" << std::endl;
//     }

//     // private:

//     // std::vector<std::string> alphabet;
//     // std::vector<tmRule> rules;
//     // std::vector<std::string> states;
//     // std::vector<std::string> start_state;
//     // std::vector<std::string> rule_dict;

//     // alphabet = list(alphabet)
//     // default_input = alphabet[0]
//     // states = list(set([rule[0] for rule in rules]))
//     // start_state = rules[0][0]
//     // rules = list(rules)
//     // rule_dict = {}


// };