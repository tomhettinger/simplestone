## Introduction

`simplestone` A Card Collecting Game similar to Blizzard's Hearthstone (okay its a clone).  The reason I wrote this simplified version of Hearthstone was mainly to see if I could build a competitive AI opponent.

![screen](https://raw.githubusercontent.com/tomhettinger/simplestone/master/screens/screen.png)


## Running the game

To play against the AI:
```sh
$ python game.py
```

To play with two humans on the same screen:
```sh
$ python game.py vs
```

To watch the CPU AIs play each other:
```sh
$ python game.py cpu
```


## Rules

Kill the opponent by attacking them directly, and bringing their HP down to 0.  It may be wise to manage enemy minions on the board.

Each turn, your mana pool increases by one and is reset to full.  Use these mana points to play cards onto the field.  Use your minions to attack the enemy (must wait one turn).

Enemy minions with taunt  \ minion / must be killed before attacking another enemy character.
Enemy minions with divine shield ( minion ) receive one free hit before taking damage.
Enemy minions with charge can attack on the same turn they are played form the hand.


## The AI

During the AI's turn, it decides what to do by looking at every possible set of actions for this turn.  As the number of possibilities increases factorially, the AI is limited to only looking 3 actions ahead (re-evaluated after the every action), even with the multi-threading implemented.  This turns out to be enough look-ahead for the AI to be competitive.  At each node in the tree, a copy of the gamestate is made and the proposed action is taken.  The win strength of the state is determined by a value determined by one of any algorithms (AI personalities and stategies can be modified and inserted here; see strategy.py), such as aggressive or board control oriented.

The best AI should balance 3 resources (board control, player HPs, and card count).  My AI implements HP and board control only at the moment.

