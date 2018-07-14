#!/usr/bin/env python

#
# Class to run a Turing machine on an input string. Python 2.
#

import attr
import re
import math
import numpy as np

@attr.s
class TuringTape(object):
    cur_tm_state = attr.ib()
    cur_tm_head_pos = attr.ib()
    tape_state = attr.ib()
    tape_lo = attr.ib()
    tape_hi = attr.ib()
    default_symbol = attr.ib()

    def print_tape(self):
        alphabet = set([self.default_symbol] + self.tape_state)
        head_msg = '^%s' % (self.cur_tm_state)
        max_inp_symbol_length = max(max(len(sym) for sym in self.tape_state), len(head_msg)+1)

        alphabet_to_padded = {sym:(sym + ' '*(max_inp_symbol_length - len(sym))) for sym in alphabet}

        # First, print the tape symbols.
        PREFIX='... '
        SUFFIX=' ...'
        tape_print = '%s%s%s' % (PREFIX, ' '.join([alphabet_to_padded[self.default_symbol]] + [alphabet_to_padded[sym] for sym in self.tape_state] + [alphabet_to_padded[self.default_symbol]]), SUFFIX)
        print (tape_print)

        # Next, print 0-position and head position + state
        desc_char_array = [' '] * len(tape_print)
        for i in range(self.tape_lo-1, self.tape_hi+1):
            index_i = len(PREFIX) + ((-self.tape_lo + i + 1) * (1+max_inp_symbol_length))
            if index_i > 0 and index_i < len(tape_print):
                desc_char_array[index_i] = str(i)[0]
                if len(str(i)) > 1:
                    desc_char_array[index_i+1] = str(i)[1]

        index_head = len(PREFIX) + ((-self.tape_lo + self.cur_tm_head_pos + 1) * (1+max_inp_symbol_length)) + 1
        for i in range(len(head_msg)):
            index_write = index_head + i
            if index_write > 0 and index_write < len(tape_print):
                desc_char_array[index_write] = head_msg[i]
        desc_char_str = ''.join(desc_char_array)
        print (desc_char_str)


class TuringMachine(object):
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
        self.rules = list(rules)
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
        tape = TuringTape(tape_lo=0,
                          tape_hi=len(input_symbol_list),
                          tape_state=list(input_symbol_list),
                          cur_tm_head_pos=0,
                          cur_tm_state=self.start_state,
                          default_symbol=self.default_input)

        its = 0
        halted = False
        accepted = None
        print 'Simulating...'
        while its < max_num_iters and not halted:

            if print_intermediate_tape:
                tape.print_tape()

            tape_state_ind = tape.cur_tm_head_pos - tape.tape_lo

            cur_tape_input = tape.tape_state[tape_state_ind]

            print (tape.cur_tm_state, cur_tape_input)

            state_to, input_to, direction = self.rule_dict[(tape.cur_tm_state, cur_tape_input)]

            tape.cur_tm_state = state_to
            tape.tape_state[tape_state_ind] = input_to

            # Move head
            if direction == 'left':
                tape.cur_tm_head_pos -= 1
            elif direction == 'right':
                tape.cur_tm_head_pos += 1
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
            if tape.cur_tm_head_pos < tape.tape_lo:
                tape.tape_lo -= 1
                tape.tape_state.insert(0, self.default_input)
            elif tape.cur_tm_head_pos >= tape.tape_hi:
                tape.tape_hi += 1
                tape.tape_state.append(self.default_input)

            its += 1

        if print_intermediate_tape:
            tape.print_tape()

        return accepted, tape, its


    def _int_to_binary(self, num, word_size, sym_0, sym_1):
        binary_list = []

        assert word_size >= 1
        num_tmp = num
        while num_tmp > 0 and len(binary_list) < word_size:
            num_tmp_old = num_tmp

            if num_tmp % 2 == 0:
                binary_list = [sym_0] + binary_list
            else:
                binary_list = [sym_1] + binary_list
                num_tmp -= 1
            assert num_tmp % 2 == 0
            num_tmp //= 2

            assert num_tmp < num_tmp_old

        while len(binary_list) < word_size:
            binary_list = [sym_0] + binary_list

        return binary_list


    def to_binary(self):
        '''
            Takes the rules for a Turing Machine and converts
            them to a binary representation
        '''
        # Use first two symbols of alphabet as 0 and 1 bits, respectively.
        bit_syms = tuple(self.alphabet[:2])

        sym_list = []

        # First, write the word size. Need to be able to represent
        # inputs and states in this word size. Then, we write this word
        # size using the following code:
        #
        # 00 = 0
        # 01 = 1
        # 11 = Done
        # 10 unused
        word_size = int(math.ceil(max(math.log(len(self.states), 2),
                                      math.log(len(self.alphabet), 2))))
        assert word_size >= 1
        word_size_tmp = word_size
        while word_size_tmp > 0:
            word_size_tmp_old = word_size_tmp

            if word_size_tmp % 2 == 0:
                sym_list = [bit_syms[0], bit_syms[0]] + sym_list
            else:
                sym_list = [bit_syms[0], bit_syms[1]] + sym_list
                word_size_tmp -= 1
            assert word_size_tmp % 2 == 0
            word_size_tmp //= 2

            assert word_size_tmp < word_size_tmp_old, (word_size_tmp, word_size_tmp_old)

        sym_list += [bit_syms[1], bit_syms[1]]

        # Next write the total number of states in binary. Max length
        # is word_size. All-zero vector would mean max length is
        # 2**word_size
        sym_list += self._int_to_binary(len(self.states), word_size, bit_syms[0], bit_syms[1])

        # Now, write rule list in binary, 5 at a time. For action,
        # use key
        #
        # 000 = left
        # 001 = right
        # 010 = halt_accept
        # 011 = halt_reject
        # 100 = noop
        DIRECTION_TO_CODE = {'left':        [bit_syms[0], bit_syms[0], bit_syms[0]],
                             'right':       [bit_syms[0], bit_syms[0], bit_syms[1]],
                             'halt_accept': [bit_syms[0], bit_syms[1], bit_syms[0]],
                             'halt_reject': [bit_syms[0], bit_syms[1], bit_syms[1]],
                             'noop':        [bit_syms[1], bit_syms[0], bit_syms[0]], }
        assert len(self.rules) == len(self.states) * len(self.alphabet)
        for rule in self.rules:
            state_from, input_from, state_to, input_to, direction = rule

            state_from_code = self._int_to_binary(self.states.index(state_from), word_size, bit_syms[0], bit_syms[1])
            input_from_code = self._int_to_binary(self.alphabet.index(input_from), word_size, bit_syms[0], bit_syms[1])
            state_to_code = self._int_to_binary(self.states.index(state_to), word_size, bit_syms[0], bit_syms[1])
            input_to_code = self._int_to_binary(self.alphabet.index(input_to), word_size, bit_syms[0], bit_syms[1])
            direction_code = DIRECTION_TO_CODE[direction]

            sym_list += (state_from_code + input_from_code + state_to_code + input_to_code + direction_code)
        
        print sym_list

        return sym_list
