import common.core as core
import argparse


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action='store', dest='filename', help='filename')
    return parser


def main():
    parser = init_parser()
    args = parser.parse_args()
    table = core.create_table_from_file(args.filename)
    print(table)


if __name__ == '__main__':
    main()
