"""
This is an example for a bot.
"""
from penguin_game import *
from MyPlayer import MyPlayer
from Utils import *


def do_turn(game):
    """
    Makes the bot run a single turn.

    :param game: the current game state.
    :type game: Game
    """

    player = MyPlayer(game)
    player.do_turn()
