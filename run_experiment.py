import agents.ISMCTS as ISMCTS
from briscola import BriscolaState
import time

def PlayGame(n, agents, winners, scores, verbose=False):
    """ Play a sample game between two ISMCTS players.
    """
    state = BriscolaState(n)

    while state.GetMoves() != []:
        if verbose:
            print(str(state))
        # Use different numbers of iterations (simulations, tree nodes) for different players
        m = agents[state.playerToMove](state)
        if verbose:
            print("Best Move: " + str(m) + "\n")
        state.DoMove(m)

    for p in range(1, state.numberOfPlayers + 1):
        if state.GetResult(p, get_points=False) > 0:
            winners[p] += 1
        scores[p] += state.GetResult(p, get_points=True)
    if verbose:
        print(f"Final score: {state.score}")


def run_experiment(agents, n_games=100, verbose=False):
    NPLAYERS = len(agents)

    winners = {p: 0 for p in range(1, NPLAYERS + 1)}
    scores = {p: 0 for p in range(1, NPLAYERS + 1)}

    print(f"Starting {n_games} games...")

    start_time = time.time()
    for i in range(n_games):
        if(i % 20 == 0):
            print(f"  {i}/{n_games} games completed")
        PlayGame(4, agents, winners, scores)
        

    print(f"Time taken: {time.time() - start_time}")

    if verbose:
        print(f"Player 1-3 wins: {winners[1]}")
        print(f"Player 2-4 wins: {winners[2]}")
        print(f"Player 1-3 avg score: {scores[1] / n_games}")
        print(f"Player 2-4 avg score: {scores[2] / n_games}")

    return winners, scores

if __name__ == "__main__":
    agents = {
        1: lambda s: ISMCTS.ISMCTS(rootstate=s, timed=False, itermax=100, thinking_time=5, verbose=0, consider_points=True),
        2: lambda s: ISMCTS.ISMCTS(rootstate=s, timed=False, itermax=100, thinking_time=5, verbose=0, consider_points=False),
        3: lambda s: ISMCTS.ISMCTS(rootstate=s, timed=False, itermax=100, thinking_time=5, verbose=0, consider_points=True),
        4: lambda s: ISMCTS.ISMCTS(rootstate=s, timed=False, itermax=100, thinking_time=5, verbose=0, consider_points=False),
    }
    run_experiment(agents, n_games=200, verbose=True)