#!/usr/bin/env python
""" Creates the board and runs the game. Created by Thomas Hettinger.
"""
from gameboard.Hand import Hand
from gameboard.Card import Card
from gameboard.Board import Board
import gameboard.actions as actions
import gameboard.loop as loop

import data.decks as decks
import data.library as library

from ai.AI import AI


def create_game():
    # Create the board
    board = Board()

    # Create the Heros and add to the board
    board.set_hero(library.create_character('rexar'), 'top')
    board.set_hero(library.create_character('anduin'), 'bottom')

    # Add minions to the board
    board.summon_minion(library.create_character('boar'), 'top', 1)
    board.summon_minion(library.create_character('boar'), 'top', 3)
    board.summon_minion(library.create_character('raptor'), 'bottom', 2)
    board.summon_minion(library.create_character('raptor'), 'bottom', 4)

    # Create player decks and shuffle them
    board.set_deck(decks.create_deck('basic'), 'top')
    board.set_deck(decks.create_deck('basic'), 'bottom')
    board.decks['top'].shuffle()
    board.decks['bottom'].shuffle()

    # Create the player's hands
    board.set_hand(Hand(), 'top')
    board.hands['top'].CPU = True
    board.hands['top'].add_card(library.create_card('theCoin'))
    board.set_hand(Hand(), 'bottom')

    # Draw three cards
    for i in range(4):
        actions.draw_card(board, 'top')
        actions.draw_card(board, 'bottom')

    return board


def main():
    board = create_game()
    ai = AI()
    loop.play_loop(board, ai)


if __name__ == "__main__":
    main()
