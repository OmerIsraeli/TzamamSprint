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

    def __new__(cls, game: Game):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, game: Game) -> None:
        super().__init__()
        self.turn_num: int = 0
        self.percent: int = 0.5
        self.game: Game = game

    def do_turn(self):
        funcs[self.determine_state()]()

    def upgrade(self):
        my_icebergs: [Iceberg] = self.game.get_my_icebergs()
        for ice in my_icebergs:
            if ice.can_upgrade() and ice.upgrade_cost() <= self.percent * ice.penguin_amount:
                ice.upgrade()

    def attack(self):
        my_icegergs = self.game.get_my_icebergs()
        destination = self.game.get_enemy_icepital_icebergs()[0]
        for iceberg in my_icegergs:
            if destination:
                print(iceberg, "sends", (iceberg.penguin_amount), "penguins to", destination)
                iceberg.send_penguins(destination, iceberg.penguin_amount)

    def defend(self):
        my_icegergs = self.game.get_my_icebergs()
        destination: Iceberg = self.game.get_my_icepital_icebergs()[0]
        for iceberg in my_icegergs:
            if destination:
                print(iceberg, "sends", (iceberg.penguin_amount), "penguins to", destination)
                iceberg.send_penguins(destination, iceberg.penguin_amount)

    def spread(self):
        # If there are any neutral icebergs.
        for my_iceberg in self.game.get_my_icepital_icebergs():
            if self.game.get_neutral_icebergs():
                spread_destinations = self.game.get_neutral_icebergs()  # type: List
                spread_destinations = sorted(spread_destinations,
                                             key=lambda dest_iceberg: my_iceberg.get_turns_till_arrival(dest_iceberg),
                                             reverse=True)[:3]
                for dest in spread_destinations:
                    print(my_iceberg, "sends", (1), "penguins to", dest)
                    my_iceberg.send_penguins(dest, 1)

    def determine_state(self):
        """
           Makes decisions of the states.

           :param self: the current game state.
           :type self: MyPlayer
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

