#ifndef TuringModuleH
#define TuringModuleH

#include <vector>
#include <string>

enum tmDirection {left, right, noop, halt_accept, halt_reject};

struct tmRule {
    std::string state_from;
    std::string input_from;
    std::string state_to;
    std::string input_to;
    std::string direction;
};

class TuringMachine {

    public:

    TuringMachine(std::vector<std::string> alphabet,
                  std::vector<tmRule> rules);

    // private:

    // std::vector<std::string> alphabet;
    // std::vector<tmRule> rules;
    // std::vector<std::string> states;
    // std::vector<std::string> start_state;
    // std::vector<std::string> rule_dict;


    /**
     * Python code for reference:
     *
     * alphabet = list(alphabet) 
     * default_input = alphabet[0]
     * states = list(set([rule[0] for rule in rules]))
     * start_state = rules[0][0]
     * rules = list(rules)
     * rule_dict = {}
     */

};

#endif