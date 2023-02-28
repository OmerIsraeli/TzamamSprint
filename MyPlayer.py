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
        self.determine_state()

    def upgrade_icebergs(self):
        my_icebergs = self.game.get_my_icebergs()
        for ice in my_icebergs:
            print(ice.upgrade_cost)
            if ice.can_upgrade() and ice.upgrade_cost <= self.percent * ice.penguin_amount and ice is not in game.get_my_icepital_icebergs():
                ice.upgrade()
                print(ice, "upgraded to level", ice.level)

    def upgrade_capital(self):
        my_capital = self.game.get_my_icepital_icebergs()[0]
        if my_capital.can_upgrade() and my_capital.upgrade_cost <= self.percent * my_capital.penguin_amount:
            my_capital.upgrade()
            print(my_capital, "upgraded to level", my_capital.level)
    def attack(self,list_of_attackers):
        for attacker in list_of_attackers:
            if attacker not in self.game.get_my_icepital_icebergs():
                attacker.send_penguins(self.game.get_enemy_icepital_icebergs()[0], attacker.penguin_anount - 1)
            else:
                attacker.send_penguins(self.game.get_enemy_icepital_icebergs()[0], attacker.penguin_anount // 2)
        print(my_iceberg, "sends", (dest_penguin_amount + 1), "penguins to", dest)


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
        #Initial play -  here we want to spread quicly
        if len(self.game.get_my_icebergs()) < 3:
            print("Initial Spreading")
            self.initial_spread()
        else:

            # Here I check if I want to attack
            list_of_attackers = self.should_I_attack()
            if list_of_attackers:
                print("All In Attack")
                self.attack(list_of_attackers)
            #If I do not attack, I want to Land & Expand with the icebregs
            else:
                if 2 * game.get_my_icebergs() > game.get_all_icebergs():
                    print("Upgrade Mode")
                    self.upgrade_icebergs()
                else:
                    print("Land & Exapnd")
                    self.spread()
                self.upgrade_capital()

