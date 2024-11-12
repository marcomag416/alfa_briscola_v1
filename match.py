import agents.ISMCTS as ISMCTS
import briscola
import random
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=int, help='number of players (default:4)', default=4, choices=[2, 4])
    parser.add_argument('--seed', type=int, help='random seed (default:None)', default=None)
    parser.add_argument('--repeat', type=int, help='number of games to play', default=1)
    parser.add_argument('--timed', type=bool, help='whether to use itermax(0) or thinking time(1)', default=False)
    parser.add_argument('--points', type=bool, help='whether to consider points(1) or wins(0)', default=False)
    args = parser.parse_args()
    
    random.seed(args.seed)
    agents_iter = {
        1: lambda s: ISMCTS.ISMCTS(rootstate=s, itermax=100, verbose=True, consider_points=args.points),
        2: lambda s: ISMCTS.ISMCTS(rootstate=s, itermax=100, verbose=False, consider_points=args.points),
        3: lambda s: ISMCTS.ISMCTS(rootstate=s, itermax=100, verbose=False, consider_points=args.points),
        4: lambda s: ISMCTS.ISMCTS(rootstate=s, itermax=100, verbose=False, consider_points=args.points),
    }
    agents_timed = {
        1: lambda s: ISMCTS.ISMCTS(rootstate=s, timed=True, thinking_time=5, verbose=False),
        2: lambda s: ISMCTS.ISMCTS(rootstate=s, timed=True, thinking_time=5, verbose=False),
        3: lambda s: ISMCTS.ISMCTS(rootstate=s, timed=True, thinking_time=5, verbose=False),
        4: lambda s: ISMCTS.ISMCTS(rootstate=s, timed=True, thinking_time=5, verbose=False),
    }
    agents = agents_timed if args.timed else agents_iter
    for i in range(args.repeat):
        briscola.PlayGame(args.players, agents, verbose=True)

if __name__ == "__main__":
    main()
