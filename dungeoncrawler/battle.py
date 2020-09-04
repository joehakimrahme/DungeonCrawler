# Copyright 2020 Joe H. Rahme <joehakimrahme@gmail.com>
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import random
import re

from dungeoncrawler import hero


class BadComboInputError(Exception):
    pass


class Battle(object):

    def __init__(self, yourteam, enemyteam):
        self.yourteam = yourteam
        self.enemyteam = enemyteam
        self.status = []

    def rivals(self, hero):
        if hero in self.yourteam:
            return self.enemyteam
        return self.yourteam

    def allies(self, hero):
        if hero in self.yourteam:
            return self.yourteam
        return self.enemyteam

    def weighted_shuffle(self, combo):
        s = []
        while combo:
            t = []
            for h in combo:
                for _ in range(h.SPD):
                    t.append(h)
            random.shuffle(t)
            _next = t[0]
            s.append(_next)
            while _next in combo:
                combo.remove(_next)
        return s

    def check_for_win(self):
        if all(h.hp <= 0 for h in self.yourteam):
            return False
        if not self.enemyteam or all(h.hp <= 0 for h in self.enemyteam):
            return True

    def generate_choices(self, world):
        choices = {}
        for h in self.yourteam + self.enemyteam:
            choices[h.name] = h.choice(world)
        return choices

    def display_choice(self, choices):
        print("-------------\n")
        for i, h in enumerate(self.yourteam):
            print(
                "%d %s, %d/%d, %d/%d, %s" %
                (i + 1, h.name,
                 h.hp, h.maxHP,
                 h.mp, h.maxMP,
                 choices[h.name])
            )
        print('')
        for m in self.enemyteam:
            print(
                "%s %d/%d" % (
                    m.name, m.hp, m.maxHP))

    def generate_combo(self):
        while True:
            try:
                cmd = input("\nPick your combo> ")
                cmd = cmd.strip()
                if cmd == "q":
                    break
                if not re.match(r"^[0-9]{1,3}$", cmd):
                    print(
                        "Malformed input. Please input a proper combo string. "
                        "Examples: '124', '423', '21'.")
                    raise BadComboInputError
                combo = []
                for i in cmd:
                    idx = int(i)
                    if idx <= len(self.yourteam):
                        selected = self.yourteam[idx - 1]
                        if selected.hp <= 0:
                            print("Can't select hero %s" % selected)
                            raise BadComboInputError
                        combo.append(self.yourteam[idx - 1])
            except BadComboInputError:
                continue
            combo += self.enemyteam
            combo = self.weighted_shuffle(combo)
            return combo

    def execute_step(self, combo, choices):
        for h in combo:
            if h.hp:
                choices[h.name].effect(self, h, combo)
            # execute end-of-step
            for mob in self.enemyteam:
                if mob.hp == 0:
                    self.enemyteam.remove(mob)

    def battle_loop(self):
        # Execute start-of-battle
        while True:
            win = self.check_for_win()
            if win is not None:
                break
            choices = self.generate_choices(self)
            self.display_choice(choices)
            combo = self.generate_combo()
            self.execute_step(combo, choices)
            for h in self.yourteam:
                h.mp += 20
            # execute end-of-turn
        print("End of Battle. Winner: %s" % ("you" if win else "monsters"))


def main():
    a = Battle(hero.HEROES, hero.MOBS)
    a.battle_loop()


if __name__ == "__main__":
    main()
