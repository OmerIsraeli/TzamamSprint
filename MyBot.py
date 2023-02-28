"""
This is an example for a bot.
"""
from penguin_game import *


def do_turn(game):
    """
    Makes the bot run a single turn.

    :param game: the current game state.
    :type game: Game
    """
    SPREAD = 0
    DEFEND = 1
    ATTACK = 2
    UPGRADE = 3
    funcs = {SPREAD: spread, DEFEND: defend, ATTACK: attack, UPGRADE: upgrade}
    state = 0

    determine_state()





def determine_state():
    pass

def spread():
    pass

def upgrade():
    pass

def attack(game: Game):
    my_icegergs = game.get_my_icebergs()
    destination = game.get_enemy_icepital_icebergs()[0]
    for iceberg in my_icegergs:
        if destination:
            print(iceberg, "sends", (iceberg.penguin_amount), "penguins to", destination)
            iceberg.send_penguins(destination, iceberg.penguin_amount)


def defend(game: Game):
    my_icegergs = game.get_my_icebergs()
    destination: Iceberg = game.get_my_icepital_icebergs()[0]
    for iceberg in my_icegergs:
        if destination:
            print(iceberg, "sends", (iceberg.penguin_amount), "penguins to", destination)
            iceberg.send_penguins(destination, iceberg.penguin_amount)


    # # Go over all of my icepitals and conquer icebergs
    # for my_iceberg in game.get_my_icepital_icebergs():
    #     # The amount of penguins in my iceberg.
    #     my_penguin_amount = my_iceberg.penguin_amount  # type: int
    #
    #     # If there are any neutral icebergs.
    #     if game.get_neutral_icebergs():
    #         # Target a neutral iceberg.
    #         destination = game.get_neutral_icebergs()[0]  # type: Iceberg
    #     else:
    #         # Target an enemy iceberg.
    #         destination = game.get_enemy_icebergs()[0]  # type: Iceberg
    #         destination
    #
    #     # The amount of penguins the target has.
    #     destination_penguin_amount = destination.penguin_amount  # type: int
    #
    #     # If my iceberg has more penguins than the target iceberg.
    #     if my_penguin_amount > destination_penguin_amount:
    #         # Send penguins to the target.
    #         print(my_iceberg, "sends", (destination_penguin_amount + 1), "penguins to", destination)
    #         my_iceberg.send_penguins(destination, destination_penguin_amount + 1)
    #
    # # Go over all of my non icepitals and conquer the enemys's icepital
    # for my_iceberg in game.get_my_icebergs():
    #     if not my_iceberg.is_icepital and game.get_enemy_icepital_icebergs():
    #         destination = game.get_enemy_icepital_icebergs()[0]  # type: Iceberg
    #         destination.
    #         # Send penguins to the target.
    #         print(my_iceberg, "sends", my_iceberg.penguin_amount, "penguins to", destination)
    #         my_iceberg.send_penguins(destination, my_iceberg.penguin_amount)
