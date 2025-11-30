import argparse

def earn(args):
    print("earn")

def report(args):
    print("report")

def get_args():
    parser = argparse.ArgumentParser(
            prog='EarningsTracker',
            description='Earning Tracker CLI')
    subparsers = parser.add_subparsers(dest='command')

    earn_parser = subparsers.add_parser('earn', help='Log an earning')
    earn_parser.add_argument('amount', type=float)
    earn_parser.add_argument('currency', type=str)
    earn_parser.set_defaults(func=earn)

    report_parser = subparsers.add_parser('report', help='Report earnings for period')
    report_parser.add_argument('time_period', type=str, default=None)
    report_parser.set_defaults(func=report)

    return parser.parse_args()

def main():
    args = get_args()
    args.func(args)

if __name__ == "__main__":
    main()
