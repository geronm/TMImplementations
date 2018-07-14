#!/usr/bin/env python

#
# turing_runner
#
# This program runs a Turing machine on an input string. Python 2.
#

import argparse
from turing import TuringMachine


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

    accept, tape, num_steps = tm.simulate(input_list)

    print 'Accepted: %s' % repr(accept)
    print 'Num steps: %d' % num_steps
    print 'Tape state:'
    tape.print_tape()

    # Halt

if __name__ == '__main__':
    main()
