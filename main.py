from expression_parser import parse
from differentiation import differentiate
import argparse

SUPPORTED = ['Integer numbers, x variable, +, -, *, /, ^, sin, cos, tan, cot']


def get_args_parser():
    parser = argparse.ArgumentParser(description='Take math expression derivative', add_help=True)
    parser.add_argument('-e', '--expression', nargs='*',
                        help='Differentiate given expression.'
                             '\nTo write degree in windows use double "^".'
                             '\nTo use Euler\'s number enter "e" in any case.'
                             '\nTo use Pi enter "pi" in any case.'
                             '\nNote that log(x) means ln(x)')
    parser.add_argument('-s', '--supported', action='store_true',
                        help='Get list of supported number types, variables, operations and functions')
    return parser


def main():
    parser = get_args_parser()
    args = parser.parse_args()
    if args.supported:
        print(SUPPORTED)
    if args.expression:
        for expression in args.expression:
            root = parse(expression)
            print(differentiate(root))


if __name__ == '__main__':
    main()
