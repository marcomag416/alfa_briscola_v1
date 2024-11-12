import sys
import os

# Add the directory containing briscola.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import briscola

def testCards():
    card = briscola.Card(2, "B")
    assert str(card) == "2B"

    #check all suits
    card = briscola.Card(10, "C")
    card = briscola.Card(11, "O")
    card = briscola.Card(12, "B")
    card = briscola.Card(11, "S")

    #check aices, tree, and figures are printed correctly
    card = briscola.Card(12, "C")
    assert str(card) == "AC"
    card = briscola.Card(11, "C")
    assert str(card) == "3C"
    card = briscola.Card(9, "C")
    assert str(card) == "QC"
    card = briscola.Card(10, "C")
    assert str(card) == "KC"
    card = briscola.Card(8, "C")
    assert str(card) == "JC"
    #verify that illegal combinations raise an error
    try:
        card = briscola.Card(3, "B")
        card = briscola.Card(1, "B")
        card = briscola.Card(0, "C")
        card = briscola.Card(15, "C")
        card = briscola.Card(15, "a")
        assert False
    except Exception:
        assert True

def testClosingPlayer():
    state = briscola.BriscolaState(4)
    assert state.GetClosingPlayer() == 4
    state.playerStarting = 4
    assert state.GetClosingPlayer() == 3
    state.playerStarting = 1
    assert state.GetClosingPlayer() == 4
    state.playerStarting = 3
    assert state.GetClosingPlayer() == 2

    state = briscola.BriscolaState(2)
    assert state.GetClosingPlayer() == 2
    state.playerStarting = 2
    assert state.GetClosingPlayer() == 1
    state.playerStarting = 1
    assert state.GetClosingPlayer() == 2
    

def main():
    testCards()
    testClosingPlayer()
    print("All tests passed")


main()