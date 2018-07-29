/**
 * Two-state turing machine simulator
 */

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <memory>
#include <utility>

#include "turing_common.hpp"

int main(int argc, char* argv[]) {
    using namespace std;

    ifstream tmInputStream;

    // Open TM file
    if (argc > 1) {
        try {
            tmInputStream.exceptions(cin.failbit);
            tmInputStream.open(argv[1], ios_base::in);

            // Extract first line specially; it contains alphabet
            vector<shared_ptr<string> > alphabet;

            {
                char c;
                shared_ptr<string> next_string(new string(""));
                while (c != '\n' && c != '\r' && tmInputStream.is_open() && !tmInputStream.eof()) {
                    tmInputStream.get(c);

                    if (c == ' ') {
                        if (next_string->size() > 0) {
                            alphabet.push_back(move(next_string));
                        }
                        next_string = make_shared<string>("");
                    } else if (c != '\n' && c != '\r') {
                        next_string->push_back(c);
                    }
                }
                if (next_string->size() > 0) {
                    alphabet.push_back(move(next_string));
                }
                cout << endl;
            }

            // Check Alphabet
            cout << "Alphabet: " << alphabet.size() << endl;
            for (int i=0; i < alphabet.size(); i++) {
                cout << (*(alphabet[i])) << endl;
            }
            cout << endl;

            // Now read rules of Turing Machine, lines of 5 symbols
            // state_from, input_from, state_to, input_to, direction
            vector<shared_ptr<tmRule> > rules;
            while (tmInputStream.is_open() && !tmInputStream.eof()) {
                shared_ptr<tmRule> next_rule (new tmRule());

                tmInputStream >> (next_rule->state_from);
                tmInputStream >> (next_rule->input_from);
                tmInputStream >> (next_rule->state_to);
                tmInputStream >> (next_rule->input_to);
                tmInputStream >> (next_rule->direction);

                rules.push_back(move(next_rule));
            }

            // Check Rules
            cout << "Rules:" << endl;
            for (int i=0; i < rules.size(); i++) {
                cout << (*(rules[i])).state_from << ", ";
                cout << (*(rules[i])).input_from << ", ";
                cout << (*(rules[i])).state_to << ", ";
                cout << (*(rules[i])).input_to << ", ";
                cout << (*(rules[i])).direction << endl;
            }
            cout << endl;

            tmInputStream.close();
        } catch (ios_base::failure &IOError) {
            cerr << "Exception occurred while reading file!" << endl;
            return 1;
        }
    }
    cout << "Successfully loaded TM model!" << endl;

    return 0;
}