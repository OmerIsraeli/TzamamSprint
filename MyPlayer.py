from typing import List

from penguin_game import *
from Utils import *

AT_ICEBREGS = 4
SPREAD = 0
DEFEND = 1
ATTACK = 2
UPGRADE = 3
funcs = {SPREAD: spread, DEFEND: defend, ATTACK: attack, UPGRADE: upgrade}


class MyPlayer:
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()
        self.turn_num = 0

    def upgrade(self, game: Game):
        pass

    def attack(game: Game):
        my_icegergs = game.get_my_icebergs()
        destination = game.get_enemy_icepital_icebergs()[0]
        for iceberg in my_icegergs:
            if destination:
                print(iceberg, "sends", (iceberg.penguin_amount), "penguins to", destination)
                iceberg.send_penguins(destination, iceberg.penguin_amount)

    def defend(self, game: Game):
        my_icegergs = game.get_my_icebergs()
        destination: Iceberg = game.get_my_icepital_icebergs()[0]
        for iceberg in my_icegergs:
            if destination:
                print(iceberg, "sends", (iceberg.penguin_amount), "penguins to", destination)
                iceberg.send_penguins(destination, iceberg.penguin_amount)

    def spread(self, game: Game):
        # If there are any neutral icebergs.
        for my_iceberg in game.get_my_icepital_icebergs():
            if game.get_neutral_icebergs():
                # Target a neutral iceberg.
                spread_destinations = game.get_neutral_icebergs()  # type: List
                for dest in spread_destinations:
                    my_iceberg.get_turns_till_arrival(dest)

                for dest in spread_destinations:
                    destination_penguin_amount = dest.penguin_amount  # type: int
                    # print(my_iceberg, "sends", (destination_penguin_amount + 1), "penguins to", dest)
                    my_iceberg.send_penguins(dest, destination_penguin_amount + 1)

    def determine_state(self, game: Game):
        """
           Makes decisions of the states.

           :param game: the current game state.
           :type game: Game
        """
        # If I want to spread
        if self.turn_num == 0:
            return SPREAD


        # Here I check if I want to attack
        max_dist = 0
        num_of_ping_to_send = 0
        my_iceberg_list : List[Iceberg] = game.get_my_icebergs()
        enemy_icepital : Iceberg = game.get_enemy_icepital_icebergs()[0]
        for iceberg in my_iceberg_list:
            dist = iceberg.get_turns_till_arrival(enemy_icepital)
            max_dist = max(max_dist,dist)
            num_of_ping_to_send += iceberg.penguin_amount - 1

        if num_of_ping_to_send > max_dist + enemy_icepital.penguin_amount:
            return ATTACK
        return UPGRADE
