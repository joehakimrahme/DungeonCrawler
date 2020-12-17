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

from dungeoncrawler import utils


class BadComboInputError(Exception):
    pass


class Battle(object):

    def __init__(self, yourteam, enemyteam, intro="", outro="", logo=""):
        self.yourteam = yourteam
        self.enemyteam = enemyteam
        self.intro = intro
        self.status = []
        self.turn = 1  # start counting from 1. Like normal people!
        self.outro_win = outro
        self.logo = logo
        self.outro_loss = """


                                                  @@@@@@@@
                                                @@@@@@@@@@@@
                    /@@@@@@@@@*              @@@@@@@@@@@@@@@@@@
               /@@@@@@@@@@@@@@@@@          @@@@@            @@@@@
             @@@@@@@@@@@@@@@@@@@@       @@@@@                  @@@@@
          *@@@@@@@@@@@@@@@@@@@@@@     @@@@@                      @@@@@
        @@@@@@@@@@@@(    #@@@@@@@     @@@@@     @@        @@     @@@@@
     ,@@@@@@@               @@@@@     @@     @@@@@@@@  @@@@@@@@     @@
   @@&                      @@@@@     @@     @@@@@@@@  @@@@@@@@     @@
                            @@@@@     @@@@@     @@        @@     @@@@@
                            @@@@@     @@@@@@@        @@        @@@@@@@
                            @@@@@     @@@@@@@@@@@@        @@@@@@@@@@
                         #@@@@@@@          @@@@@@@        @@@@@@@
                         #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                         #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                            @@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@
                            @@@@@          @@@@@@@@@@@@@@@@@@@@@@
                            @@@@@          @@@@@@@@@@@@@@@@@@@@@@
                            @@@@@          @@@@@@@@@@@@@@@@@@@@@@
                            @@@@@          @@@@@@@@@@@@@@@@@@@@@@
                            @@@@@            @@@@@@@@@@@@@@@@@@
                            @@@@@            @@@@@@@@@@@@@@@@@@
                            @@@@@       @@@@@@@@@@@@@@@@@@@@@@@@@@@@
                            @@@@@  &@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                            @@@@@@@.  @@   @@@@@  @@@@@@@@  @@@@@   @@   @@
                                   &@@  @@@  @@@     @@     @@@       @@@


You dead. You lose. Try to do better next time.
"""

    def outro(self, cond):
        if cond:
            return self.outro_win
        return self.outro_loss

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
                for _ in range(int(h.SPD**2)):
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
        print("-" * 90)
        print("%s %-24s %-22s %-19s  %-s" % (
            "#", "NAME", "HIT POINTS", "MANA POINTS", "CHOICE")
        )
        print()
        for i, h in enumerate(self.yourteam):
            if h.hp:
                _c = choices[h.name]
                if h.mp_ratio == 100:
                    _c = utils.color(str(_c), 'bold')
                print(
                    "%d %-22s %s %s" %
                    (i + 1, utils.color(h.name, 'bold'),
                     h.bars(), _c)
                )
        print()
        for m in self.enemyteam:
            print(
                "%-15s %9s %s" % (
                    m.name, "/".join((str(int(m.hp)), str(int(m.maxHP)))),
                    m.hp_bars()))
        print("-" * 90)
        print()

    def generate_combo(self):
        while True:
            try:
                cmd = input("[%s] Pick your combo> " % self.turn)
                cmd = cmd.strip()
                if cmd == "q":
                    break  # need to do this!
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
            print()
            return combo

    def execute_step(self, combo, choices):
        for h in combo:
            if h.hp:
                choices[h.name].effect(combo)
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
            self.turn += 1
        print(self.outro(win))
        input()
        return win


def display_stats(heroes):
    def print_bar(stat, ratio):
        print("%3s: %s" % (
            stat, utils.bars(size=20, color_fill="white", ratio=ratio * 100)))
    _maxHP = max((h.maxHP for h in heroes))
    _maxMP = max((h.maxMP for h in heroes))
    _maxATK = max((h.ATK for h in heroes))
    _maxMAG = max((h.MAG for h in heroes))
    _maxDEF = max((h.DEF for h in heroes))
    _maxSPR = max((h.SPR for h in heroes))
    _maxSPD = max((h.SPD for h in heroes))
    for h in heroes:
        print()
        print(h.name)
        print_bar('HP', h.maxHP / _maxHP)
        print_bar('MP', h.maxMP / _maxMP)
        print_bar('ATK', h.ATK / _maxATK)
        print_bar('MAG', h.MAG / _maxMAG)
        print_bar('DEF', h.DEF / _maxDEF)
        print_bar('SPR', h.SPR / _maxSPR)
        print_bar('SPD', h.SPD / _maxSPD)
