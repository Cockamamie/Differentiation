from expression_parser import parse
from differentiation import differentiate
import argparse


def get_args_parser():
    parser = argparse.ArgumentParser(description='Take math expression derivative')
    parser.add_argument('-e', '--expression', required=True, nargs='*',
                        help='Differentiate given expression.'
                             '\nTo write degree in windows use double "^".'
                             '\nTo use Euler\'s number enter "e" in any case.'
                             '\nTo use Pi enter "pi" in any case.')
    return parser


def main():
    parser = get_args_parser()
    args = parser.parse_args()
    for expression in args.expression:
        root = parse(expression)
        print(differentiate(root))


if __name__ == '__main__':
    main()
