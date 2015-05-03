import board.loop as loop


class AI(object):
	"""An artificial intellegince for playing out turns in SimpleStone."""
	def play_turn(self, board):
		"""Execute all of the actions on the board for this turn, then end the turn 
		and give the game back to the human."""
		board.set_text('AI is thinking...')
		loop.refresh(board)
		loop.end_turn(board)