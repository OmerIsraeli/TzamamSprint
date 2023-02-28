from penguin_game import *
import math

AT_ICEBREGS = 4
SPREAD = 0
DEFEND = 1
ATTACK = 2
UPGRADE = 3
AMOUNT_TO_CLONE = 2
WAIT_MIN = 5


class MyPlayer:
    def __init__(self):
        self.turn_num = 0
        self.percent = 0.9
        self.game = None

    def set_game(self, game):
        self.game = game

    def do_turn(self):
        self.determine_state()

    def upgrade_icebergs(self):
        my_icebergs = self.game.get_my_icebergs()
        for ice in my_icebergs:
            print(ice.upgrade_cost)
            if ice.can_upgrade() and ice not in self.game.get_my_icepital_icebergs():
                ice.upgrade()
                print(ice, "upgraded to level", ice.level)
            else:
                cloneberg = self.game.get_cloneberg()
                if self.turn_num % max(WAIT_MIN, self.game.cloneberg_max_pause_turns) == 0:
                    self.send_penguins(AMOUNT_TO_CLONE, ice, cloneberg)

    def upgrade_capital(self):
        my_capital = self.game.get_my_icepital_icebergs()[0]
        print("COST OF upgrade:", my_capital.upgrade_cost)
        if my_capital.can_upgrade():
            my_capital.upgrade()
            print(my_capital, "upgraded to level", my_capital.level)
        else:
            cloneberg = self.game.get_cloneberg()
            if self.turn_num % max(WAIT_MIN, self.game.cloneberg_max_pause_turns) == 0:
                self.send_penguins(AMOUNT_TO_CLONE, my_capital, cloneberg)

    def attack_dst(self, list_of_attackers, dst):
        for attacker in list_of_attackers:
            if attacker not in self.game.get_my_icepital_icebergs():
                attacker.send_penguins(dst, attacker.penguin_amount)
                print(attacker, "sends", (attacker.penguin_amount), "penguins to", dst)
            else:
                attacker.send_penguins(dst, attacker.penguin_amount // 2)
                print(attacker, "sends", (attacker.penguin_amount // 2), "penguins to", dst)

    def attack(self, list_of_attackers):
        self.attack_dst(list_of_attackers, self.game.get_enemy_icepital_icebergs()[0])
        # for attacker in list_of_attackers:
        #     if attacker not in self.game.get_my_icepital_icebergs():
        #         attacker.send_penguins(self.game.get_enemy_icepital_icebergs()[0], attacker.penguin_amount)
        #         print(attacker, "sends", (attacker.penguin_amount), "penguins to",
        #               self.game.get_enemy_icepital_icebergs()[0])
        #     else:
        #         attacker.send_penguins(self.game.get_enemy_icepital_icebergs()[0], attacker.penguin_amount // 2)
        #         print(attacker, "sends", (attacker.penguin_amount // 2), "penguins to",
        #               self.game.get_enemy_icepital_icebergs()[0])

    def defend(self):
        my_icegergs = self.game.get_my_icebergs()
        destination = self.game.get_my_icepital_icebergs()[0]
        for iceberg in my_icegergs:
            if destination:
                print(iceberg, "sends", (iceberg.penguin_amount), "penguins to", destination)
                iceberg.send_penguins(destination, iceberg.penguin_amount)

    def initial_spread(self):
        # If there are any neutral icebergs.
        for my_iceberg in self.game.get_my_icepital_icebergs():
            if self.game.get_neutral_icebergs():
                spread_destinations = self.game.get_neutral_icebergs()  # type: List
                spread_destinations = sorted(spread_destinations,
                                             key=lambda dest_iceberg: my_iceberg.get_turns_till_arrival(dest_iceberg))[
                                      :2]
                for dest in spread_destinations:
                    if self.on_the_way(dest) == 0:
                        self.send_penguins(dest.penguin_amount + 1, my_iceberg, dest)

    def spread_to_neutral(self):
        chosen_destinations = []
        for dest in self.game.get_neutral_icebergs():
            if self.on_the_way(dest) == 0:
                chosen_destinations.append(dest)
        chosen_dest = sorted(chosen_destinations,
                             key=lambda dest_iceberg: dest_iceberg.penguin_amount)[0]
        dest_penguin_amount = chosen_dest.penguin_amount
        my_iceberg_list = self.game.get_my_icebergs()
        my_iceberg_list.remove(self.game.get_my_icepital_icebergs()[0])
        sum = 0
        for iceberg in my_iceberg_list:
            sum += iceberg.penguin_amount - 1
        if sum >= dest_penguin_amount + 1:
            for iceberg in my_iceberg_list:
                iceberg.send_penguins(chosen_dest, iceberg.penguin_amount - 1)

    def spread_to_enemy(self):
        chosen_destinations = []
        for dest in self.game.get_enemy_icebergs():
            if self.on_the_way(dest) == 0:
                chosen_destinations.append(dest)
            attackers = self.should_I_attack(dest, False)

            chosen_dest = sorted(chosen_destinations,
                                 key=lambda dest_iceberg: dest_iceberg.penguin_amount)[0]

    def spread(self):
        if self.game.get_enemy_icebergs():
            print("spread to enemy")
            self.spread_to_enemy()
        else:
            print("spread_to_neutral")
            self.spread_to_neutral()

    def determine_state(self):
        """
           Makes decisions of the states.

           :param self: the current game state.
           :type self: MyPlayer
        """
        # If I want to spread
        print(self.turn_num)
        self.turn_num += 1
        # Initial play -  here we want to spread quicly
        if len(self.game.get_my_icebergs()) < 3:
            print("Initial Spreading")
            self.initial_spread()
        else:

            # Here I check if I want to attack
            if self.game.get_enemy_icepital_icebergs():
                list_of_attackers = self.should_I_attack(self.game.get_enemy_icepital_icebergs()[0])
                if list_of_attackers:
                    print("All In Attack")
                    self.attack(list_of_attackers)
                # If I do not attack, I want to Land & Expand with the icebregs
                else:
                    if 2 * len(self.game.get_my_icebergs()) > len(self.game.get_all_icebergs()):
                        print("Upgrade Mode")
                        self.upgrade_icebergs()
                    else:
                        print("Land & Exapnd")
                        self.spread()
                    self.upgrade_capital()

    def should_I_attack(self, dst, all_in=True):
        """
        check weather attacking now will win
        :return: combination of icbergs from which to attack
        """
        if self.game.get_enemy_icepital_icebergs():
            my_icebergs = self.game.get_my_icebergs()
            other_capital = dst
            my_icebergs = sorted(my_icebergs, key=lambda iceberg: iceberg.get_turns_till_arrival(other_capital))
            if not all_in:
                my_icebergs.remove(self.game.get_my_icepital_icebergs()[0])
            total = 0
            for i, iceberg in enumerate(my_icebergs):
                if iceberg == self.game.get_my_icepital_icebergs()[0]:
                    total += iceberg.penguin_amount // 2
                elif not all_in:
                    total += iceberg.penguin_amount // 2
                else:
                    total += iceberg.penguin_amount
                strength = other_capital.penguin_amount + other_capital.penguins_per_turn * iceberg.get_turns_till_arrival(
                    other_capital) + 10
                if total > strength:
                    return my_icebergs[:i + 1]

    def on_the_way(self, dst):
        count = 0
        for group in self.game.get_my_penguin_groups():
            if group.destination.equals(dst):
                count += group.penguin_amount
        return count

    def is_under_attack(self, dst):
        count = 0
        for group in self.game.get_enemy_penguin_groups():
            if group.destination.equals(dst):
                count += group.penguin_amount
        return count

    def send_penguins(self, amount, src, dst):
        print(src, "sends", amount, "penguins to", dst)
        src.send_penguins(dst, amount)
