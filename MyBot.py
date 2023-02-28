"""
This is an example for a bot.
"""
from penguin_game import *
from MyPlayer import MyPlayer

player = MyPlayer()

def do_turn(game):
    """
    Makes the bot run a single turn.

    :param game: the current game state.
    :type game: Game
    """
    player.set_game(game)
    player.do_turn()
