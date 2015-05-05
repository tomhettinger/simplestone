MAX_MINIONS = 7
import ai.Action as Action
from Character import Character
from Spell import Spell

class Board(object):
    """Board class which holds minions on it (4 per side) and Heros."""

    def __init__(self, topHero=None, bottomHero=None):
        self.heroes = {'top':topHero, 'bottom':bottomHero}
        self.decks = {'top':None, 'bottom':None}
        self.hands = {'top':None, 'bottom':None}
        self.manaBase = {'top':0, 'bottom':1}
        self.manaCurrent = {'top':0, 'bottom':1} 
        self.minions = {'top':[None, None, None, None, None, None, None], 'bottom':[None, None, None, None, None, None, None]}
        self.playerTurn = 'bottom'
        self.turnCount = 1
        self.log = ["",]


    def set_hand(self, hand, side):
        self.hands[side] = hand
        hand.side = side
        hand.board = self


    def set_deck(self, deck, side):
        self.decks[side] = deck
        deck.side = side


    def set_hero(self, character, side):
        """Set a hero with a given character object."""
        if self.heroes[side] is not None:
            raise Exception
        self.heroes[side] = character
        character.side = side
        character.board = self


    def set_text(self, text):
        """Set the text to be displayed in the output field."""
        self.log.append(text)


    def get_log(self):
        """Return the current text to be displayed."""
        return self.log


    def get_hero(self, side=None):
        """Return one of the heroes (default is the active one)."""
        if side is None:
            side = self.playerTurn
        return self.heroes[side]


    def get_enemy_hero(self):
        """Return the hero from the opposite side."""
        return self.heroes[self.get_enemy_side()]


    def get_minions(self, side=None, valid=False):
        """Return list of minions (default is the active one). Includes None values."""
        if side is None:
            side = self.playerTurn
        minions = self.minions[side]
        if valid:
            return [minion for minion in minions if minion is not None]
        else:
            return minions


    def get_enemy_minions(self, valid=False):
        """Return the minions from the opposite side.  Includes None values."""
        minions = self.minions[self.get_enemy_side()]
        if valid:
            return [minion for minion in minions if minion is not None]
        else:
            return minions


    def get_hand(self, side=None):
        if side is None:
            side = self.get_side()
        return self.hands[side]


    def get_side(self):
        """Return the current playerTurn."""
        return self.playerTurn


    def get_enemy_side(self):
        """Return the side opposite of the given side."""
        if self.playerTurn == 'top':
            return 'bottom'
        elif self.playerTurn == 'bottom':
            return 'top'
        else:
            raise Exception('Invalid side: %s' % side)


    def get_empty_minion_positions(self, *args):
        """Return a list of positions (idx+1) where this side has empty minion slots."""
        if 'enemy' in args:
            side = self.get_enemy_side()
        else:
            side = self.get_side()
        emptyPositions = []
        for i, minion in enumerate(self.minions[side]):
            if minion is None:
                emptyPositions.append(i+1)
        return emptyPositions


    def get_canAttack_characters(self):
        """Return a list of characters that can attack right now."""
        side = self.playerTurn
        canAttackChars = []
        for minion in self.minions[side]:
            if minion is None:
                continue
            if minion.can_attack():
                canAttackChars.append(minion)
        if self.heroes[side].can_attack():
            canAttackChars.append(self.heroes[side])
        return canAttackChars


    def get_canAttack_char_positions(self):
        """Return a list of positions of characters that can attack right now."""
        side = self.playerTurn
        canAttackPos = []
        for i, minion in enumerate(self.minions[side]):
            if minion is None:
                continue
            if minion.can_attack():
                canAttackPos.append(i+1)
        if self.heroes[side].can_attack():
            canAttackPos.append(8)
        return canAttackPos


    def get_character(self, pos, side=None):
        """Return the character at the position specified. Default is current side."""
        if side is None:
            side = self.playerTurn
        if pos < 0 or pos > 8:
            raise Exception("Invalid character position.")
        if pos == 8:
            return self.heroes[side]
        else:
            return self.minions[side][pos-1]


    def get_all_characters(self):
        """Return a list of all characters on the board that aren't None."""
        allChars = []
        for minion in self.minions['top']:
            if minion is None:
                continue
            allChars.append(minion)
        for minion in self.minions['bottom']:
            if minion is None:
                continue
            allChars.append(minion)
        allChars.append(self.heroes['top'])
        allChars.append(self.heroes['bottom'])
        return allChars


    def get_character_by_position(self, pos):
        """Return the character from a position. 1-7 enemy minions, 8 enemy hero, 
        11-17 friendly minions, 18 friendly hero."""
        if pos not in [1,2,3,4,5,6,7,8,11,12,13,14,15,16,17,18]:
            raise Exception("Invalid target position.")
        if pos == 8:
            return self.get_enemy_hero()
        elif pos == 18:
            return self.get_hero()
        elif 1 <= pos <= 7:
            return self.get_enemy_minions()[pos-1]
        elif 11 <= pos <= 17:
            return self.get_minions()[pos-11]


    def get_targetable_characters(self, attacker):
        """Return a list of characters that can be ATTACKED by the attacker.  Check that
        the attacker can target opponent, and that the opponent can be targeted by attacker."""
        enemy_taunts = [minion for minion in self.get_enemy_minions(valid=True) if 'taunt' in minion.status]

        targetableChars = []
        for potentialTarget in self.get_all_characters():
            if attacker.can_target(potentialTarget) and potentialTarget.targetable_by(attacker):
                if len(enemy_taunts) and potentialTarget not in enemy_taunts:
                    continue
                targetableChars.append(potentialTarget)
        return targetableChars


    def get_target_pos(self, targetChar):
        """Determine where the targetChar is on the board and return a position number 
        based on that.  1-7 enemy minions, 8 enemy hero, 11-17 friendly minions, 18 friendly hero.
        Return None if not found."""
        # Check if hero
        if targetChar is self.get_hero():
            return 18
        elif targetChar is self.get_enemy_hero():
            return 8
        elif targetChar in self.get_minions():
            pos = self.get_minions().index(targetChar) + 11
            return pos
        elif targetChar in self.get_enemy_minions():
            pos = self.get_enemy_minions().index(targetChar) + 1
            return pos
        return None

    ######################WIP WIP WIP
    def get_available_actions(self):
        """Find out every possible action for this instant."""
        availableActions = []
        #availableActions.append(Action.DoNothingAction())  # Do nothing.
        availableActions.extend(self.get_card_play_actions())
        availableActions.extend(self.get_attack_actions())
        #availableActions.extend(heroAbilityActions)
        return availableActions


    def get_card_play_actions(self):
        actionList = []
        playableCards = self.get_hand().get_playable_cards()
        if not len(playableCards):
            return []
        emptyPositions = self.get_empty_minion_positions()

        for card in playableCards:
            # Create actions for dropping a minion.
            if isinstance(card.contents, Character) and len(emptyPositions):
                for pos in emptyPositions:
                    actionList.append(Action.PlayMinionAction(card, self.get_side(), pos))

            # Create actions for using a spell
            elif isinstance(card.contents, Spell):
                actionList.append(Action.PlaySpellAction(card))

            # Create actions for equipping a weapon.

        return actionList


    def get_attack_actions(self):
        """Find all possible attack combinations and return a list of them."""
        actionList = []
        potentialAttackers = self.get_canAttack_characters()
        if not len(potentialAttackers):
            return []
        for character in potentialAttackers:
            potentialTargets = self.get_targetable_characters(character)
            if not len(potentialTargets):
                continue
            for target in potentialTargets:
                actionList.append(Action.AttackAction(character, target))
        return actionList
    ######################WIP WIP WIP



    def update_mana(self):
        """Increate the mana base by 1 if less than 10, then refresh
        the mana to full (overload not implemented)."""
        side = self.get_side()
        if self.manaBase[side] < 10:
            self.manaBase[side] += 1
        self.manaCurrent[side] = self.manaBase[side]


    def increment_turn(self):
        """Increment the turn counter."""
        self.turnCount += 1


    def subtract_mana(self, amount, side=None):
        """Subtract mana from current side, unless side is specified."""
        if side is None:
            side = self.get_side()
        self.manaCurrent[side] -= amount
        if self.manaCurrent[side] < 0:
            raise Exception("Mana less than 0.")


    def add_mana(self, amount, side=None):
        """Subtract mana from current side, unless side is specified."""
        if side is None:
            side = self.get_side()
        if self.manaCurrent[side] >= 10:
            return
        else:
            self.manaCurrent[side] += amount


    def change_side(self):
        """Change the current playerTurn to the opposite side."""
        self.playerTurn = self.get_enemy_side()


    def reset_attacksRemaining(self):
        """Reset the remaining attacks for all characters on the current side."""
        side = self.get_side()
        for minion in self.minions[side]:
            if minion is None:
                continue
            minion.attacksRemaining = 1
            if 'windfury' in minion.status:
                minion.attacksRemaining += 1
        hero = self.heroes[side]
        hero.attacksRemaining = 1
        if 'windfury' in hero.status:
            hero.attacksRemaining += 1


    def summon_minion(self, minion, side=None, pos=None):
        """Place a minion on the board given the side and (optional) position. If position
        is not specified, place the minion in lowest available spot (not implemented yet).
        Positions range from 1-7.  Set attacksRemaining to 0, unless charge."""
        if side is None:
            side = self.get_side()
        minion.side = side
        minion.board = self
        idx = pos - 1
        if self.minions[side][idx] is not None:
            raise Exception("Not a free spot.")
        self.minions[side][idx] = minion
        if "charge" in minion.status:
            minion.attacksRemaining = 1
            if "windfury" in minion.status:
                minion.attacksRemaining += 1


    def destroy_minion(self, deadMinion):
        """Destroy the character specified from the field."""
        for side in ['top', 'bottom']:
            for i, minion in enumerate(self.minions[side]):
                if minion is deadMinion:
                    self.minions[side][i] = None
                    deadMinion.deathrattle()
                    del deadMinion
                    return
