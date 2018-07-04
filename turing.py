#!/usr/bin/env python

#
# Class to run a Turing machine on an input string. Python 2.
#

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

    def print_tape_state(self, cur_tm_state, cur_tm_head_pos, tape_state, tape_lo, tape_hi):
        head_msg = '^ %s ' % (cur_tm_state)
        max_inp_symbol_length = max(max(len(sym) for sym in self.alphabet), len(head_msg)+1)

        alphabet_to_padded = {sym:(sym + ' '*(max_inp_symbol_length - len(sym))) for sym in self.alphabet}

        # First, print the tape symbols.
        PREFIX='... '
        SUFFIX='... '
        tape_print = '%s%s%s' % (PREFIX, ' '.join([alphabet_to_padded[self.default_input]] + [alphabet_to_padded[sym] for sym in tape_state] + [alphabet_to_padded[self.default_input]]), SUFFIX)
        print (tape_print)

        # Next, print 0-position and head position + state
        desc_char_array = [' '] * len(tape_print)
        for i in range(tape_lo-1, tape_hi+1):
            index_i = len(PREFIX) + ((-tape_lo + i + 1) * (1+max_inp_symbol_length))
            if index_i > 0 and index_i < len(tape_print):
                desc_char_array[index_i] = str(i)[0]
                if len(str(i)) > 1:
                    desc_char_array[index_i+1] = str(i)[1]

        index_head = len(PREFIX) + ((-tape_lo + cur_tm_head_pos + 1) * (1+max_inp_symbol_length)) + 2
        for i in range(len(head_msg)):
            index_write = index_head + i
            if index_write > 0 and index_write < len(tape_print):
                desc_char_array[index_write] = head_msg[i]
        desc_char_str = ''.join(desc_char_array)
        print (desc_char_str)


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
                # print tape_state[:-tape_lo], tape_state[-tape_lo:]
                self.print_tape_state(cur_tm_state, cur_tm_head_pos, tape_state, tape_lo, tape_hi)

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
            # print tape_state[:-tape_lo], tape_state[-tape_lo:]
            self.print_tape_state(cur_tm_state, cur_tm_head_pos, tape_state, tape_lo, tape_hi)

        return accepted, (cur_tm_state, cur_tm_head_pos, tape_state, tape_lo, tape_hi)
