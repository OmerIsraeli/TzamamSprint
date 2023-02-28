from penguin_game import *

NAT_ICEBREGS = 4
SPREAD = 0
DEFEND = 1
ATTACK = 2
UPGRADE = 3
funcs = {SPREAD: spread, DEFEND: defend, ATTACK: attack, UPGRADE: upgrade}


def attack_icepital():
    """
    This function attacks the enemys icepital
    :return:
    """
    pass


def determine_state(game):
    """
       Makes decisions of the states.

       :param game: the current game state.
       :type game: Game
       """
    # If I want to spread
    if game.get_neutral_icebergs() and len(game.get_my_icebergs()) < NAT_ICEBREGS:
        # Target a neutral iceberg.
        return SPREAD
    else:
        if game.get_my_icepital_icebergs():
            return ATTACK
        else:
            return DEFEND

    #
    # # The amount of penguins the target has.
    # destination_penguin_amount = destination.penguin_amount  # type: int
    #
    #
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
    #         destination.
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
