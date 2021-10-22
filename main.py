from expression_parser import parse
from differentiation import differentiate
import argparse


def get_args_parser():
    parser = argparse.ArgumentParser(description='Take math expression derivative')
    parser.add_argument('-e', '--expression', required=True,
                        help='Differentiate given expression')
    return parser


def main():
    parser = get_args_parser()
    args = parser.parse_args()
    root = parse(args.expression)
    print(differentiate(root))


if __name__ == '__main__':
    main()
