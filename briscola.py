import random
from copy import deepcopy
import itertools
import agents.ISMCTS as ISMCTS

class GameState:
    """ A state of the game, i.e. the game board. These are the only functions which are
        absolutely necessary to implement ISMCTS in any imperfect information game,
        although they could be enhanced and made quicker, for example by using a 
        GetRandomMove() function to generate a random move during rollout.
        By convention the players are numbered 1, 2, ..., self.numberOfPlayers.
    """

    def __init__(self):
        self.numberOfPlayers = 2
        self.playerToMove = 1

    def GetNextPlayer(self, p):
        """ Return the player to the left of the specified player
        """
        return (p % self.numberOfPlayers) + 1

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = GameState()
        st.playerToMove = self.playerToMove
        return st

    def CloneAndRandomize(self, observer):
        """ Create a deep clone of this game state, randomizing any information not visible to the specified observer player.
        """
        return self.Clone()

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerToMove.
        """
        self.playerToMove = self.GetNextPlayer(self.playerToMove)

    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        raise NotImplementedException()

    def GetResult(self, player):
        """ Get the game result from the viewpoint of player. 
        """
        raise NotImplementedException()

    def __repr__(self):
        """ Don't need this - but good style.
        """
        pass


class Card:
    """ A playing card, with rank and suit.
        rank must be an integer between 2 U [4, 12] inclusive (Jack=8, Queen=9, King=10, Tree=11, Ace=12)
        suit must be a string of length 1, one of 'C' (Coppe), 'S' (Spade), 'B' (Bastoni) or 'O' (Ori)
    """

    def __init__(self, rank, suit):
        """ Initialize the card with the specified rank and suit.
        """
        if rank not in Card.GetValidRanks():
            raise Exception("Invalid rank")
        if suit not in Card.GetValidSuits():
            raise Exception("Invalid suit")
        self.rank = rank
        self.suit = suit

    def GetValidRanks():
        """ Return a list of valid ranks.
        """
        return [2] + list(range(4, 12 + 1))

    def GetValidSuits():
        """ Return a list of valid suits.
        """
        return ["O", "B", "S", "C"]

    def GetNewDeck():
        """ Return a list of all cards in a deck (unshuffled).
        """
        return [
            Card(rank, suit) 
            for rank in Card.GetValidRanks()
            for suit in Card.GetValidSuits()
        ]

    def GetPoints(self):
        """ Return the points of the card.
        """
        # J, Q, K are worth 2, 3, 4 points
        if( self.rank >= 8 and self.rank <= 10):
            return self.rank - 6
        # 3 is worth 10 points
        if( self.rank == 11):
            return 10
        # A is worth 11 points
        if( self.rank == 12):
            return 11
        # all other cards are worth 0 points
        return 0

    def __repr__(self):
        return "??2?4567JQK3A"[self.rank] + self.suit

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other):
        return self.rank != other.rank or self.suit != other.suit


class BriscolaState(GameState):
    """ A state of the game of Briscola.
        The game is played with a deck of 40 cards, 4 suits (Cups, Coins, Swords, Clubs) and 10 ranks (Ace-7, Jack, Queen, King).
        The game is for 2-4 players, each of whom is dealt 3 cards.
        Players take turns to play a card, the winner of the trick is the player who played the highest card of the led suit.
        The game is won by the player who wins the majority of the points.
    """
    def __init__(self, n):
        """ Initialize the game state. n is the number of players (2 / 4).
        """
        #super().__init__()
        if(n != 2 and n != 4):
            raise Exception(f"Invalid number of players (must be 2 or 4). Found {n}")

        self.numberOfPlayers = n
        self.playerToMove = 1   # player 1 starts
        self.playerStarting = 1 # player who started the current round
        self.playerHands = {p : [] for p in range(1, self.numberOfPlayers + 1)} # cards held by each player
        self.table = []         # [(player, card)] cards played during this round (shown on the table)
        self.discarded = []     # cards already played during the game 
        self.lastCard = None    # last card of the deck (determines the trump suit)
        self.trumpSuit = None   # suit of the trump (briscola) suit
        self.score = [0, 0]     # scores for the two teams [even, odd]

        self.InitDeal()


    def InitDeal(self):
        """ Deal the cards for the beginning of the game.
        """
        deck = Card.GetNewDeck()
        random.shuffle(deck)
        for p in range(1, self.numberOfPlayers + 1):
            self.playerHands[p] = [deck.pop() for _ in range(3)]
        self.table = []
        self.lastCard = deck.pop()
        self.trumpSuit = self.lastCard.suit

    def DealRound(self):
        """ Deal the cards for the beginning of a round.
        """

        # collect the cards played during the round
        self.discarded += [c for _, c in self.table]
        self.table = []

        # build the deck of cards to be dealt
        cardsAlreadyDealt = self.discarded + [self.lastCard] + list(itertools.chain(*self.playerHands.values()))
        deck = [c for c in Card.GetNewDeck() if c not in cardsAlreadyDealt]
        random.shuffle(deck)

        #if deck is empty exit function
        if(len(deck) == 0):
            return

        # deal the cards to the players
        last_deal = len(deck) + 1 == self.numberOfPlayers

        if(last_deal):
            # if there are only numPlayers card left, the closing player gets the last card
            self.playerHands[self.GetClosingPlayer()].append(self.lastCard)

        for p in range(1, self.numberOfPlayers + 1):
            if(not last_deal or p != self.GetClosingPlayer()):
                self.playerHands[p].append(deck.pop())


    def GetNextPlayer(self, p):
        """ Return the player to the right of the specified player
        """
        return (p % self.numberOfPlayers) + 1

    def GetClosingPlayer(self):
        """ Return the player who will close the current round (to the left of the player who starts the round)
        """
        return ((self.playerStarting - 2) % self.numberOfPlayers) + 1

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = BriscolaState(self.numberOfPlayers)
        st.playerToMove = self.playerToMove
        st.playerHands = deepcopy(self.playerHands)
        st.table = deepcopy(self.table)
        st.discarded = deepcopy(self.discarded)
        st.lastCard = self.lastCard
        st.trumpSuit = self.trumpSuit
        st.score = deepcopy(self.score)
        return st

    def CloneAndRandomize(self, observer):
        """ Create a deep clone of this game state, randomizing any information not visible to the specified observer player.
        """
        st = self.Clone()
        
        # the observer can see his cards, the cards on the table, the last card and the cards already discarded
        seenCards = st.playerHands[observer] + st.discarded + [c for _, c in st.table] + [st.lastCard] 

        #build random set of cards to be dealt to the other players
        unseenCards = [c for c in Card.GetNewDeck() if c not in seenCards]
        random.shuffle(unseenCards)
        unseenCards.append(st.lastCard) # add the last card to the deck

        # assign the cards to the other players
        for p in range(1, self.numberOfPlayers + 1):
            if p != observer:
                st.playerHands[p] = [unseenCards.pop(0) for _ in range(len(self.playerHands[p]))]

        return st

    def GetMoves(self, play_anyway=True):
        """ Get all possible moves from this state. 
            If play_anyway is True, return cards even if the game is already won/lost
        """
        #if one of the teams has already won, there are no moves
        if (self.score[0] >= 61 or self.score[1] >= 61) and not play_anyway:
            return []
        #otherwise, return all cards in hand
        return self.playerHands[self.playerToMove]

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerToMove.
        """
        self.table.append((self.playerToMove, move))
        self.playerHands[self.playerToMove].remove(move)
        self.playerToMove = self.GetNextPlayer(self.playerToMove)

        #if the table is full, the round is over
        if(len(self.table) == self.numberOfPlayers):
            winner, points = self.ComputeWinner(self.table)
            self.score[winner % 2] += points
            self.playerStarting = winner
            self.playerToMove = winner
            self.DealRound()


    def ComputeWinner(self, table):
        """ Compute the winner of the round and the points won by the winner.
        """

        if(len(self.table) != self.numberOfPlayers):
            raise Exception(f"The round must be over to compute the winner. Found {len(self.table)} cards on the table and {self.numberOfPlayers} players")

        # find the winner of the round
        winner = table[0]
        points = winner[1].GetPoints()
        for p, c in table[1:]:
            points += c.GetPoints()
            if c.suit == self.trumpSuit and winner[1].suit != self.trumpSuit:
                winner = (p, c)
            if c.suit == winner[1].suit and (c.rank > winner[1].rank):
                winner = (p, c)

        return winner[0], points

    def GetResult(self, player, get_points=True):
        """ Get the game result from the viewpoint of player. 
            If get_points is True, return the points difference between the player and opponents,
            otherwise return 1 if the player wins and 0 otherwise.
        """
        if get_points:
            return self.score[player % 2] - self.score[(player + 1) % 2]
        else:
            return self.score[player % 2] > self.score[(player + 1) % 2]

    def __repr__(self):
        """ Return a string representation of the state.
        """
        s = "Score: " + str(self.score) + "\n"
        s += "Trump: " + str(self.trumpSuit) + "\n"
        s += "Table: " + str(self.table) + "\n"
        s += "Hands: " + str(self.playerHands) + "\n"
        s += "Player to move: " + str(self.playerToMove) + "\n"
        return s

def PlayGame(n, agents, verbose=False):
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

    someoneWon = False
    for p in range(1, state.numberOfPlayers + 1):
        if state.GetResult(p, get_points=False) > 0:
            print("Player " + str(p) + " wins!")
            someoneWon = True
    if not someoneWon:
        print("Nobody wins!")

    print(f"Final score: {state.score}")


if __name__ == "__main__":
    agents = {
        1: lambda s: ISMCTS.ISMCTS(rootstate=s, itermax=1000, verbose=False),
        2: lambda s: ISMCTS.ISMCTS(rootstate=s, itermax=100, verbose=False),
        3: lambda s: ISMCTS.ISMCTS(rootstate=s, itermax=100, verbose=False),
        4: lambda s: ISMCTS.ISMCTS(rootstate=s, itermax=100, verbose=False),
    }
    PlayGame(4, agents)
