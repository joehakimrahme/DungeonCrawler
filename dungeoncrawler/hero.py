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

from dungeoncrawler import skills
from dungeoncrawler import utils


attack_ability = skills.ATTACK


class Fighter(object):

    def __init__(self, name, attributes, skills):
        self.name = name
        self.maxHP = attributes['HP']
        self.ATK = attributes['ATK']
        self.DEF = attributes['DEF']
        self.MAG = attributes['MAG']
        self.SPR = attributes['SPR']
        self.SPD = attributes['SPD']
        self.skills = skills
        self._hp = self.maxHP
        self._mp = 0

    def __repr__(self):
        return self.name

    @property
    def maxMP(self):
        if hasattr(self, 'skills') and self.skills:
            return max([s.mp_cost for s in self.skills])
        else:
            # mobs don't really have skills so we assign an
            # arbitrarily high number for maxMP
            return 999

    @property
    def mp(self):
        return self._mp

    @mp.setter
    def mp(self, value):
        switch = {
            True: value,
            value > self.maxMP: self.maxMP,
            value < 0: 0}

        self._mp = switch[True]

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        switch = {
            True: value,
            value > self.maxHP: self.maxHP,
            value < 0: 0}

        self._hp = switch[True]

    @property
    def hp_ratio(self):
        return self.hp / self.maxHP * 100

    @property
    def mp_ratio(self):
        return self.mp / self.maxMP * 100

    def hp_bars(self):
        return utils.bars(
            size=20, color_fill="red", ratio=self.hp_ratio)

    def mp_bars(self):
        return utils.bars(
            size=10, color_fill="blue", ratio=self.mp_ratio)

    def bars(self):
        _currentHP = str(int(self.hp))
        _maxHP = str(int(self.maxHP))
        _currentMP = str(int(self.mp))
        _maxMP = str(int(self.maxMP))

        return "%9s %s - %s %-9s" % (
            "/".join((_currentHP, _maxHP)),
            self.hp_bars(),
            self.mp_bars(),
            "/".join((_currentMP, _maxMP)))


class Hero(Fighter):

    def __init__(self, name, attributes, skills):
        super(Hero, self).__init__(name, attributes, skills)
        self.maxHP *= 500
        self._hp = self.maxHP
        self.ATK *= 100
        self.DEF *= 100
        self.MAG *= 100
        self.SPR *= 100

    def choice(self, world):
        _c = []
        for skill in self.skills:
            if skill(world, self).predicate():
                _c.append(skill(world, self))
        if not _c:
            return attack_ability(world, self)
        return random.choice(_c)


class Mob(Fighter):
    def __init__(self, name, attributes, skills):
        super(Mob, self).__init__(name, attributes, skills)
        self.maxHP *= 500
        self._hp = self.maxHP
        self.ATK *= 100
        self.DEF *= 100
        self.MAG *= 100
        self.SPR *= 100
        self.skills = skills

    def choice(self, world):
        for s in self.skills:
            _candidate = s(world, self)
            if _candidate.predicate():
                return _candidate
        return attack_ability(world, self)

    def bars(self):
        _currentHP = str(int(self.hp))
        _maxHP = str(int(self.maxHP))

        return "%9s %s" % (
            "/".join((_currentHP, _maxHP)),
            self.hp_bars())
