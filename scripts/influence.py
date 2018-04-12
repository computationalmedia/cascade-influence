from casIn.user_influence import casIn
import argparse

parser = argparse.ArgumentParser(description='casIn')
parser.add_argument('--cascade_path', type=str)
parser.add_argument('--time_decay', type=float, default=-0.000068)
parser.add_argument('--save2csv', type=bool, default=False)
args = parser.parse_args()

if __name__ == '__main__':
    influence = casIn(args.cascade_path, args.time_decay)
    print(influence)
    if args.save2csv:
        influence.to_csv("result.csv",header=True, index=False)