from penguin_game import *
import math

AT_ICEBREGS = 4
SPREAD = 0
DEFEND = 1
ATTACK = 2
UPGRADE = 3
AMOUNT_TO_CLONE = 1


class MyPlayer:
    def __init__(self):
        self.turn_num = 0
        self.percent = 0.2
        self.game = None
        self.on_the_way = dict()
        self.funcs = {SPREAD: self.spread, DEFEND: self.defend, ATTACK: self.attack, UPGRADE: self.upgrade}

    def set_game(self, game):
        self.game = game

    def do_turn(self):
        self.determine_state()

    def upgrade_icebergs(self):
        my_icebergs = self.game.get_my_icebergs()
        for ice in my_icebergs:
            print(ice.upgrade_cost)
            if ice.can_upgrade() and ice.upgrade_cost <= self.percent * ice.penguin_amount and ice not in \
                    self.game.get_my_icepital_icebergs():
                ice.upgrade()
                print(ice, "upgraded to level", ice.level)
            else:
                cloneberg = self.game.get_cloneberg()
                if self.turn_num % self.game.cloneberg_max_pause_turns == 0:
                    self.send_penguins(AMOUNT_TO_CLONE, ice, cloneberg)

    def upgrade_capital(self):
        my_capital = self.game.get_my_icepital_icebergs()[0]
        if my_capital.can_upgrade() and my_capital.upgrade_cost <= self.percent * my_capital.penguin_amount:
            my_capital.upgrade()
            print(my_capital, "upgraded to level", my_capital.level)
        else:
            cloneberg = self.game.get_cloneberg()
            if self.turn_num % self.game.cloneberg_max_pause_turns == 0:
                self.send_penguins(AMOUNT_TO_CLONE, my_capital, cloneberg)

    def attack(self, list_of_attackers):
        for attacker in list_of_attackers:
            if attacker not in self.game.get_my_icepital_icebergs():
                attacker.send_penguins(self.game.get_enemy_icepital_icebergs()[0], attacker.penguin_anount)
                print(attacker, "sends", (attacker.penguin_anount), "penguins to",
                      self.game.get_enemy_icepital_icebergs()[0])
            else:
                attacker.send_penguins(self.game.get_enemy_icepital_icebergs()[0], attacker.penguin_anount // 2)
                print(attacker, "sends", (attacker.penguin_anount // 2), "penguins to",
                      self.game.get_enemy_icepital_icebergs()[0])

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
                        self.send_penguin(dest.penguin_amount, my_iceberg, dest)

    def optional_dest(self):
        chosen_destinations = []
        if self.game.get_neutral_icebergs():
            for dest in self.game.get_neutral_icebergs():
                if self.on_the_way(dest) == 0:
                    chosen_destinations.append(dest)
        else:
            for dest in self.game.get_enemy_icepital_icebergs():
                if not self.on_the_way(dest):
                    chosen_destinations.append(dest)
        return chosen_destinations


    def spread(self):
        for icepital in self.game.get_my_icepital_icebergs():
            spread_destinations = self.optional_dest()
            chosen_dest = sorted(spread_destinations,
                                             key=lambda dest_iceberg: icepital.get_turns_till_arrival(dest_iceberg))[:1]
            my_iceberg_list = self.game.get_my_icebergs()
            dest_penguin_amount = chosen_dest.penguin_amount
            sum = 0
            for iceberg in my_iceberg_list:
                sum += iceberg.penguin_amount * 0.5
            if sum >= dest_penguin_amount:
                for iceberg in my_iceberg_list:
                    iceberg.send_penguins(chosen_dest, math.ceil(iceberg.penguin_amount * 0.5))

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
            list_of_attackers = self.should_I_attack()
            if list_of_attackers:
                print("All In Attack")
                self.attack(list_of_attackers)
            # If I do not attack, I want to Land & Expand with the icebregs
            else:
                if 2 * self.game.get_my_icebergs() > self.game.get_all_icebergs():
                    print("Upgrade Mode")
                    self.upgrade_icebergs()
                else:
                    print("Land & Exapnd")
                    self.spread()
                self.upgrade_capital()

    def should_I_attack(self):
        """
        check weather attacking now will win
        :return: combination of icbergs from which to attack
        """
        my_icebergs = self.game.get_my_icebergs()
        other_capital = self.game.get_enemy_icepital_icebergs()[0]
        my_icebergs = sorted(my_icebergs, key=lambda iceberg: iceberg.get_turns_till_arrival(other_capital))
        total = 0
        for iceberg, i in enumerate(my_icebergs):
            total += iceberg.penguin_amount
            strength = other_capital.penguin_amount + other_capital.penguins_per_turn * my_icebergs.get_turns_till_arrival(
                other_capital)
            if total > strength:
                return my_icebergs[:i]

    def on_the_way(self, dst):
        count = 0
        for group in self.game.get_my_penguin_groups():
            if group.destination.equals(dst):
                count += group.penguin_amount
        return count

    def send_penguins(self, amount, src, dst):
        print(src, "sends", amount, "penguins to", dst)
        src.send_penguins(dst, amount)
