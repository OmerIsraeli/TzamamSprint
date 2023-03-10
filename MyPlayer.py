from penguin_game import *
import math

AT_ICEBREGS = 4
SPREAD = 0
DEFEND = 1
ATTACK = 2
UPGRADE = 3
AMOUNT_TO_CLONE = 1
WAIT_MIN = 5
ALL_IN_ADDITION = 20
ATTACK_FACTOR = 0.7
INITIAL_CONST = 3
CLONE_FACTOR = 0.75
RECEIVE_FROM_CLONE = 1


class MyPlayer:
    def __init__(self):
        self.turn_num = 0
        self.stage = 1
        self.percent = 0.75
        self.game = None
        self.my_capital = None
        self.enemy_capital = None

    def set_game(self, game):
        self.game = game
        self.my_capital = self.game.get_my_icepital_icebergs()[0]
        if game.get_enemy_icepital_icebergs():
            self.enemy_capital = game.get_enemy_icepital_icebergs()[0]

    def do_turn(self):
        self.determine_state()

    def determine_state(self):
        """
           Makes decisions of the states.

           :param self: the current game state.
           :type self: MyPlayer
        """
        # At the beginning we spread to 3 icebergs

        clone = self.game.get_cloneberg()
        print(self.turn_num, self.stage)
        icebergs = self.game.get_all_icebergs()
        icebergs.remove(self.enemy_capital)
        self.turn_num += 1
        if self.turn_num < 3:
            my_capital = self.game.get_my_icepital_icebergs()[0]
            print(my_capital.upgrade_cost)
            if my_capital.can_upgrade():
                my_capital.upgrade()
        elif self.stage == 1:
           self.stage1(clone,icebergs)
        # Initial play -  here we want to spread quicly
        else:
            self.handle_clone(clone, icebergs)
            if (len(self.game.get_my_icebergs()) + self.we_are_attacking()) < INITIAL_CONST + 1:
                print("Initial Spreading")
                self.initial_spread()
            else:
                if self.game.get_enemy_icepital_icebergs():
                    # Most important is to defend the capital
                    if self.is_under_attack(self.game.get_my_icepital_icebergs()[0]):
                        self.defend(self.game.get_my_icepital_icebergs()[0])
                    # Here I check if I want to attack
                    list_of_attackers = self.should_I_attack(self.game.get_enemy_icepital_icebergs()[0])
                    if list_of_attackers:
                        print("All In Attack")
                        self.attack(list_of_attackers)
                    # If I do not attack, I want to Land & Expand with the icebergs
                    else:
                        print("Spreading or Upgrading")
                        self.spread()
                        self.upgrade_icebergs()
                        if not self.is_under_attack(self.game.get_my_icepital_icebergs()[0]):
                            self.upgrade_capital()

    def handle_clone(self, clone, icebergs):
        if clone:
            minimal_to_clone = min(icebergs, key=lambda iceberg: iceberg.get_turns_till_arrival(clone))
            self.send_penguins(minimal_to_clone.penguin_amount * CLONE_FACTOR, minimal_to_clone, clone)
            for berg in self.game.get_my_icebergs():
                self.send_penguins(RECEIVE_FROM_CLONE, minimal_to_clone, berg)

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
        print("COST OF upgrade:", my_capital.upgrade_cost, "min:", self.percent * my_capital.penguin_amount)
        if my_capital.can_upgrade() and my_capital.upgrade_cost < self.percent * my_capital.penguin_amount:
            my_capital.upgrade()
            print(my_capital, "upgraded to level", my_capital.level)
        # else:
        #     cloneberg = self.game.get_cloneberg()
        #     if self.turn_num % max(WAIT_MIN, self.game.cloneberg_max_pause_turns) == 0:
        #         self.send_penguins(my_capital.level, my_capital, cloneberg)

    def attack_dst(self, list_of_attackers, dst, all_in=True):
        FACTOR = 1 if all_in else ATTACK_FACTOR
        for attacker in list_of_attackers:
            if attacker not in self.game.get_my_icepital_icebergs():
                self.send_penguins(attacker.penguin_amount * FACTOR,attacker,dst)
            else:
                self.send_penguins(attacker.penguin_amount // 2,attacker,dst)
                print(attacker, "sends", (attacker.penguin_amount // 2), "penguins to", dst)

    def attack(self, list_of_attackers):
        self.attack_dst(list_of_attackers, self.game.get_enemy_icepital_icebergs()[0], True)
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
                self.send_penguins(iceberg.penguin_amount,iceberg,destination)

    def initial_spread(self):
        # If there are any neutral icebergs.
        if len(self.game.get_neutral_icebergs()) - self.we_are_attacking_neutral(0):
            self.initial_spread_to_neutral()
        else:
            self.spread_to_enemy(True)

    def spread_to_neutral(self):
        chosen_destinations = []
        my_capitpal = self.game.get_my_icepital_icebergs()[0]
        for dest in self.game.get_neutral_icebergs():
            if self.on_the_way(dest) == 0:
                chosen_destinations.append(dest)
        chosen_dest = sorted(chosen_destinations,
                             key=lambda dest_iceberg: my_capitpal.get_turns_till_arrival(dest_iceberg))[0]
        dest_penguin_amount = chosen_dest.penguin_amount
        my_iceberg_list = self.game.get_my_icebergs()
        my_iceberg_list.remove(self.game.get_my_icepital_icebergs()[0])
        sum = 0
        for iceberg in my_iceberg_list:
            sum += iceberg.penguin_amount - 1
        if sum >= dest_penguin_amount + 1:
            for iceberg in my_iceberg_list:
                self.send_penguins( iceberg.penguin_amount - 1,iceberg,chosen_dest)

    def spread_to_enemy(self, all_in=False):
        chosen_destinations = []
        my_capitpal = self.game.get_my_icepital_icebergs()[0]
        enemy_icebergs = sorted(self.game.get_enemy_icebergs(), key=lambda dest_iceberg:
        my_capitpal.get_turns_till_arrival(dest_iceberg))
        for dest in enemy_icebergs:
            if self.on_the_way(dest) == 0:
                chosen_destinations.append(dest)
            attackers = self.should_I_attack(dest, all_in)
            if (attackers):
                self.attack_dst(attackers, dest)

    def spread(self):
        if self.game.get_enemy_icebergs():
            print("spread to enemy")
            self.spread_to_enemy()
        else:
            print("spread_to_neutral")
            self.spread_to_neutral()

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
                    total += iceberg.penguin_amount * ATTACK_FACTOR
                else:
                    total += iceberg.penguin_amount
                strength = other_capital.penguin_amount + other_capital.penguins_per_turn * iceberg.get_turns_till_arrival(
                    other_capital) + ALL_IN_ADDITION
                if total > strength:
                    return my_icebergs[:i + 1]

    def defend(self, under_attack):
        attackers = self.is_under_attack(under_attack)
        my_icebergs = self.game.get_my_icebergs()
        my_icebergs.remove(self.game.get_my_icepital_icebergs()[0])
        sum = 0
        max_time = 0
        for ice in my_icebergs:
            sum += ice.penguin_amount
            max_time = max(ice.get_turns_till_arrival(under_attack), max_time)
        Y = attackers - (under_attack.penguin_amount + under_attack.penguins_per_turn * max_time + self.on_the_way(
            under_attack))
        x = max(Y, 0)

        for i, iceberg in enumerate(my_icebergs):
            amount_to_send = (x * iceberg.penguin_amount) / sum
            self.send_penguins(amount_to_send, iceberg, under_attack)

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
        if not src.is_under_siege:
            print(src, "sends", amount, "penguins to", dst)
            src.send_penguins(dst, amount)

    def initial_spread_to_neutral(self):
        chosen_destinations = []
        my_capitpal = self.game.get_my_icepital_icebergs()[0]
        for dest in self.game.get_neutral_icebergs():
            if self.on_the_way(dest) == 0:
                chosen_destinations.append(dest)
        chosen_dest = sorted(chosen_destinations,
                             key=lambda dest_iceberg: my_capitpal.get_turns_till_arrival(dest_iceberg))[0]
        dest_penguin_amount = chosen_dest.penguin_amount
        my_iceberg_list = self.game.get_my_icebergs()
        sum = 0
        for iceberg in my_iceberg_list:
            sum += iceberg.penguin_amount - 1
        reduce = dest_penguin_amount + 1
        if sum >= dest_penguin_amount + 1:
            for iceberg in my_iceberg_list:
                if reduce < iceberg.penguin_amount - 1:
                    self.send_penguins(reduce,iceberg,chosen_dest)
                else:
                    self.send_penguins(iceberg.penguin_amount - 1,iceberg,chosen_dest)
                reduce = max(reduce - (iceberg.penguin_amount - 1), 0)

    def initial_spread_to_enemy(self, all_in=False):
        chosen_destinations = []
        my_capitpal = self.game.get_my_icepital_icebergs()[0]
        enemy_icebergs = sorted(self.game.get_enemy_icebergs(), key=lambda dest_iceberg:
        my_capitpal.get_turns_till_arrival(dest_iceberg))
        for dest in enemy_icebergs:
            if self.on_the_way(dest) == 0:
                chosen_destinations.append(dest)
            attackers = self.should_I_attack(dest, all_in)
            if (attackers):
                self.attack_dst(attackers, dest)

    def we_are_attacking(self):
        count = 0
        count = self.we_are_attacking_enemy(count)
        count = self.we_are_attacking_neutral(count)
        return count

    def we_are_attacking_enemy(self, count):
        for iceberg in self.game.get_enemy_icebergs():
            if self.on_the_way(iceberg):
                count += 1
        return count

    def we_are_attacking_neutral(self, count):
        for iceberg in self.game.get_neutral_icebergs():
            if self.on_the_way(iceberg):
                count += 1
        return count

    def stage1(self, clone, icebergs):
        if clone and self.my_capital.penguin_amount > 10:
            minimal_to_clone = sorted(icebergs, key=lambda iceberg: iceberg.get_turns_till_arrival(clone))
            for ice in minimal_to_clone:
                if self.my_capital.penguin_amount > ice.penguin_amount + ice.penguins_per_turn * self.my_capital.get_turns_till_arrival(
                        ice):
                    self.send_penguins(ice.penguin_amount, self.my_capital, ice)