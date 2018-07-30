#ifndef TuringModuleH
#define TuringModuleH

#include <vector>
#include <string>
#include <memory>

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

    TuringMachine(
        std::vector<std::shared_ptr<std::string> > alphabet,
        std::vector<std::shared_ptr<tmRule> > rules);

    ~TuringMachine(void);

    void print_self (void);

    private:

    std::vector<std::shared_ptr<std::string> > alphabet;
    std::vector<std::shared_ptr<tmRule> > rules;
    std::vector<std::shared_ptr<std::string> > states;
    std::string start_state;
    std::string default_symbol;
    std::vector<std::vector<int> > new_state_map; // array mapping to new state index
    std::vector<std::vector<int> > new_input_map; // array mapping to new input index
    std::vector<std::vector<tmDirection> > direction_map; // array mapping to new state

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