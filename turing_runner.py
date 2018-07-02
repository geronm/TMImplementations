#!/usr/bin/env python

#
# turing_runner
#
# This program runs a Turing machine on an input string. Python 2.
#

import argparse
import re
import numpy as np


class TuringMachine():
    def __init__(self, alphabet, rules):
        '''
            Parameters:
            ---
            alphabet - list of TM symbols, as strings

            rules - list of TM rules, as 5-tuples of strings
               specifying (state_from, input_from, state_to, input_to, direction).
               (no wildcards supported here)
        '''
        self.alphabet = list(alphabet)
        self.default_input = self.alphabet[0]
        self.states = list(set([rule[0] for rule in rules]))
        self.start_state = rules[0][0]
        self.rule_dict = {}
        for rule in rules:
            print 'Parsing rule: %s ...' % repr(rule)
            state_from, input_from, state_to, input_to, direction = rule
            self.rule_dict[(state_from, input_from)] = (state_to, input_to, direction)

        print 'Rule dict:'
        print self.rule_dict
        print 'Alphabet:'
        print self.alphabet

        assert all([(state, inp) in self.rule_dict for state in self.states for inp in self.alphabet])
        assert len(self.rule_dict) == len(alphabet) * len(self.states)
        assert all([outcome[0] in self.states for outcome in self.rule_dict.values()])
        assert all([outcome[1] in self.alphabet for outcome in self.rule_dict.values()])
        assert all([outcome[2] in ['left', 'right', 'halt_accept', 'halt_reject', 'noop'] for outcome in self.rule_dict.values()])

    @staticmethod
    def parse_tm_spec_lines(tm_spec_lines):
        assert len(tm_spec_lines) > 2
        alphabet = TuringMachine.parse_input_string(tm_spec_lines[0])
        rules_lines = tm_spec_lines[1:]

        negative_regex = re.compile(' +')
        positive_regex = re.compile('[A-Za-z0-9_]+')

        rules = [negative_regex.split(line.strip()) for line in rules_lines]
        assert all((len(rule) == 5 for rule in rules))
        assert all((all((positive_regex.match(symbol).start() == 0 for symbol in rule)) for rule in rules))
        assert all((all((positive_regex.match(symbol).end()   == len(symbol) for symbol in rule)) for rule in rules))

        return alphabet, rules

    @staticmethod
    def parse_input_string(input_string, alphabet_check=None):
        negative_regex = re.compile(' +')
        positive_regex = re.compile('[A-Za-z0-9_]+')

        input_list = negative_regex.split(input_string.strip())
        assert all((positive_regex.match(symbol).start() == 0 for symbol in input_list))
        assert all((positive_regex.match(symbol).end()   == len(symbol) for symbol in input_list))

        if alphabet_check is not None:
            assert all((symbol in alphabet_check for symbol in input_list))

        return input_list

    def simulate(self, input_symbol_list, print_intermediate_tape=True, max_num_iters=500):
        '''
            Simulate the tm. Pretty straightforward implementation.

            Parameters:
            ---
            input_symbol_list - a list of the input symbols, as strings

            Returns:
            ---
            accepted, state - accepted is whether the TM accepted, state is info about halt state.
        '''
        tape_lo = 0
        tape_hi = len(input_symbol_list)
        tape_state = list(input_symbol_list)
        cur_tm_head_pos = 0
        cur_tm_state = self.start_state

        its = 0
        halted = False
        accepted = None
        print 'Simulating...'
        while its < max_num_iters and not halted:

            if print_intermediate_tape:
                print tape_state[:-tape_lo], tape_state[-tape_lo:]

            tape_state_ind = cur_tm_head_pos - tape_lo

            cur_tape_input = tape_state[tape_state_ind]

            print (cur_tm_state, cur_tape_input)

            state_to, input_to, direction = self.rule_dict[(cur_tm_state, cur_tape_input)]

            cur_tm_state = state_to
            tape_state[tape_state_ind] = input_to

            # Move head
            if direction == 'left':
                cur_tm_head_pos -= 1
            elif direction == 'right':
                cur_tm_head_pos += 1
            elif direction == 'halt_accept':
                halted = True
                accepted = True
            elif direction == 'halt_reject':
                halted = True
                accepted = False
            elif direction == 'noop':
                pass
            else:
                raise Exception('Bad direction: %s' % direction)

            # Lengthen tape if necessary:
            if cur_tm_head_pos < tape_lo:
                tape_lo -= 1
                tape_state.insert(0, self.default_input)
            elif cur_tm_head_pos >= tape_hi:
                tape_hi += 1
                tape_state.insert(0, self.default_input)

            its += 1

        if print_intermediate_tape:
            print tape_state[:-tape_lo], tape_state[-tape_lo:]

        return accepted, (cur_tm_state, cur_tm_head_pos, tape_lo, tape_hi, tape_state)




def main():

    DESCRIPTION = (
        'TM Specification is a bit restrictive, for simpler implementation.\n'
        '\n'
        'List of symbols in the alphabet is provided on the first line,\n'
        'separated by spaces. Next come all state + input combinations\n'
        'for the turing machine, as space-separated 5-tuples:\n'
        '\n'
        '   state_from input_from state_to input_to direction\n'
        '\n'
        '(direction must be one of left, right, halt_accept, halt_reject, or noop). States and\n'
        'symbols must be alphanumericunderscore strings. Whatever symbol\n'
        'comes first on the alphabet line is used as the "default" symbol,\n'
        'populating the non-input portions of the initial tape, and the\n'
        'first state_from from the first TM rule is used as the start\n'
        'state for the Turing Machine. All state-symbol pairs should have\n'
        'specified rules. \n'
        '\n'
        'There is one special character, *, which fills in as\n'
        'input_from representing all inputs. This should be disjoint with all other\n'
        'rules. This is used to make the description of s3 in the example\n'
        'below more terse\n'
        '\n'
        '\n'
        'Example Turing Machine Spec File, for a binary-alphabet turing\n'
        'machine that either prints 3 1\'s and then halts, or just halts,\n'
        'depending on whether the first input symbol is 0 or 1:\n'
        '\n'
        'zero one\n'
        's0 zero s0 zero halt_accept\n'
        's0 one s1 one right\n'
        's1 zero s2 one right\n'
        's1 one s2 one right\n'
        's2 * s2 one halt_accept\n'
        '\n'
        '\n'
        )
    
    ap = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)   

    ap.add_argument('tm_spec_file', help='File specifying the turing machine, according to a specific format.')
    ap.add_argument('input_string_file', help='File specifying the input to the turing machine, in the turing machine '
          'language.')

    args = ap.parse_args()

    tm_spec_lines = []
    with open(args.tm_spec_file, 'r') as tm_spec_file:
        tm_spec_lines = ''.join(l for l in tm_spec_file)
        tm_spec_lines = tm_spec_lines.split('\n')

    input_string = ''
    with open(args.input_string_file, 'r') as input_string_file:
        input_string = [l for l in input_string_file]
        assert len(input_string) == 1
        input_string = input_string[0]

    alphabet, rules = TuringMachine.parse_tm_spec_lines(tm_spec_lines)
    input_list = TuringMachine.parse_input_string(input_string, alphabet_check=alphabet)
    
    tm = TuringMachine(alphabet, rules)

    accept, state = tm.simulate(input_list)

    print 'Accepted: %s' % repr(accept)

    print 'Tape state raw:'
    print state

    # Halt

if __name__ == '__main__':
    main()
