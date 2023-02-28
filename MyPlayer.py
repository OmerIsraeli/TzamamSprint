from penguin_game import *

AT_ICEBREGS = 4
SPREAD = 0
DEFEND = 1
ATTACK = 2
UPGRADE = 3


class MyPlayer:

    def __init__(self):
        self.turn_num = 0
        self.percent = 0.2
        self.game = None
        self.funcs = {SPREAD: self.spread, DEFEND: self.defend, ATTACK: self.attack, UPGRADE: self.upgrade}

    def set_game(self, game):
        self.game = game

    def do_turn(self):
        self.funcs[self.determine_state()]()

    def upgrade(self):
        my_icebergs = self.game.get_my_icebergs()
        for ice in my_icebergs:
            print(ice.upgrade_cost)
            if ice.can_upgrade() and ice.upgrade_cost <= self.percent * ice.penguin_amount:
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
        destination = self.game.get_my_icepital_icebergs()[0]
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
                                             key=lambda dest_iceberg: my_iceberg.get_turns_till_arrival(dest_iceberg))[
                                      :2]

                for dest in spread_destinations:
                    dest_penguin_amount = dest.penguin_amount
                    print(my_iceberg, "sends", (dest_penguin_amount + 1), "penguins to", dest)
                    my_iceberg.send_penguins(dest, dest_penguin_amount + 1)

    def determine_state(self):
        """
           Makes decisions of the states.

           :param self: the current game state.
           :type self: MyPlayer
        """
        # If I want to spread
        print(self.turn_num)
        self.turn_num += 1
        if len(self.game.get_my_icebergs()) < 3:
            return SPREAD

        # Here I check if I want to attack
        max_dist = 0
        num_of_ping_to_send = 0
        my_iceberg_list = self.game.get_my_icebergs()
        enemy_icepital = self.game.get_enemy_icepital_icebergs()[0]
        for iceberg in my_iceberg_list:
            dist = iceberg.get_turns_till_arrival(enemy_icepital)
            max_dist = max(max_dist, dist)
            num_of_ping_to_send += iceberg.penguin_amount - 1

        if num_of_ping_to_send > max_dist + enemy_icepital.penguin_amount:
            return ATTACK
        return UPGRADE

