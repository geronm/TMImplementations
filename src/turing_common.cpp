#include "turing_common.hpp"
#include <iostream>
#include <memory>
#include <utility>
#include <vector>

TuringMachine::TuringMachine(
        std::vector<std::shared_ptr<std::string> > alphabet,
        std::vector<std::shared_ptr<tmRule> > rules) : alphabet(alphabet), rules(rules), states() {
    std::cout << "Begin TuringMachine constructor." << std::endl;

    // Extract unique states, deriving a canonical ordering for them.
    for (int i = 0; i < this->rules.size(); i++) {
        bool already_added = false;
        std::string string_to_add = this->rules[i]->state_from;
        for (int j = 0; j < this->states.size(); j++) {
            if (string_to_add == *(this->states[j])) {
                already_added = true;
                break;
            }
        }

        if (!already_added) {
            this->states.push_back(std::make_shared<std::string>(string_to_add));
        }
    }

    // Start state is first mentioned state_from
    this->start_state = this->rules[0]->state_from;

    // Default symbol is first alphabet
    this->default_symbol = *(this->alphabet[0]);

    // Initialize rule mapping. Can allocate on heap given the number of states and symbols
    // TODO this->rule_mapping

    std::cout << "End TuringMachine constructor." << std::endl;
}

void TuringMachine::print_self (void) {
    // Alphabet
    std::cout << "Alphabet (" << alphabet.size() << "):" << std::endl;
    for (int i=0; i < alphabet.size(); i++) {
        std::cout << "  " << (*(alphabet[i])) << std::endl;
    }
    std::cout << std::endl;

    // States
    std::cout << "States (" << states.size() << "):" << std::endl;
    for (int i=0; i < states.size(); i++) {
        std::cout << "  " << (*(states[i])) << std::endl;
    }
    std::cout << std::endl;

    // Rules
    std::cout << "Rules (" << rules.size() << "):" << std::endl;
    for (int i=0; i < rules.size(); i++) {
        std::cout << "  ";
        std::cout << (*(rules[i])).state_from << ", ";
        std::cout << (*(rules[i])).input_from << ", ";
        std::cout << (*(rules[i])).state_to << ", ";
        std::cout << (*(rules[i])).input_to << ", ";
        std::cout << (*(rules[i])).direction << std::endl;
    }

    // Default Symbol
    std::cout << "Default Symbol: " << default_symbol << std::endl;

    // Start State
    std::cout << "Start State: " << start_state << std::endl;
}

TuringMachine::~TuringMachine(void) {
    // Still nothing to do here
}