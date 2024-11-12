import random

def RandomAgent(state):
    """ A random agent for the game of Briscola.
    """
    return random.choice(state.GetMoves())