/**
 * Two-state turing machine simulator
 */

#include <iostream>
#include <fstream>

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
            char c = 0;
            while (c != '\n' && tmInputStream.is_open() && !tmInputStream.eof()) {
                tmInputStream.get(c);
                cout << c;
            }

            // Now read rules of Turing Machine, lines of 5 symbols
            // string state_from;
            // string input_from;
            // string state_to;
            // string input_to;
            // string direction;
            tmRule rule;
            while (tmInputStream.is_open() && !tmInputStream.eof()) {
                tmInputStream >> rule.state_from;
                tmInputStream >> rule.input_from;
                tmInputStream >> rule.state_to;
                tmInputStream >> rule.input_to;
                tmInputStream >> rule.direction;
                
                cout << rule.state_from << " ";
                cout << rule.input_from << " ";
                cout << rule.state_to << " ";
                cout << rule.input_to << " ";
                cout << rule.direction << endl;
                cout << ":)" << endl;
            }

            tmInputStream.close();
        } catch (ios_base::failure &IOError) {
            cerr << "Exception occurred while reading file!" << endl;
            return 1;
        }
    }
    cout << "Hello, World!" << endl;

    return 0;
}