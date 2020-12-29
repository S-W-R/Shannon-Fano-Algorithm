from fs_operator.fs_operator import FSOperator
import argparse


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode',
                        action='store',
                        choices=['code', 'decode'],
                        help='mode')
    parser.add_argument('input',
                        action='store',
                        help='input filename')
    parser.add_argument('output',
                        action='store',
                        help='output filename')
    parser.add_argument('-e',
                        action='store',
                        dest='encoding',
                        default='utf8',
                        help='encoding for input file\n default: utf8')
    return parser


def main():
    parser = init_parser()
    args = parser.parse_args()
    fs_operator = FSOperator()
    if args.mode == 'code':
        fs_operator.code_file(args.input, args.output, args.encoding)
    elif args.mode == 'decode':
        fs_operator.decode_file(args.input, args.output, args.encoding)


if __name__ == '__main__':
    main()
