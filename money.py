#!/usr/bin/env python3

import argparse


def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Track your earnings')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    earn_parser = subparsers.add_parser('earn', help='Add earning')
    earn_parser.add_argument('amount', type=float, help='Amount earned')
    earn_parser.add_argument('currency', type=str, help='Currency in which was earned')

    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()
    print(args.command)
    print(args.amount)
    print(args.currency)


if __name__ == "__main__":
    main()
