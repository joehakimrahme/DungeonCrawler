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


attack_ability = skills.ATK()


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

    def __repr__(self):
        return self.name


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
            if self.mp >= skill.mp_cost:
                _c.append(skill)
        if not _c:
            return attack_ability
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
            if s.predicate(world):
                return s
        return attack_ability


HEROES = []

wizard_dict = {
    'HP': 0.8,
    'ATK': 0.6,
    'DEF': 0.9,
    'MAG': 1.2,
    'SPR': 1.3,
    'SPD': 7,
}
wizard_skills = [
    skills.NovaBlast(),
    skills.Focus(),
]
HEROES.append(Hero('wizard', wizard_dict, wizard_skills))

cleric_dict = {
    'HP': 1.5,
    'ATK': 0.3,
    'DEF': 0.8,
    'MAG': 1.1,
    'SPR': 1.5,
    'SPD': 3,
}
cleric_skills = [
    skills.Heal(),
    skills.SilentPrayer(),
]
HEROES.append(Hero('cleric', cleric_dict, cleric_skills))

monk_dict = {
    'HP': 1.3,
    'ATK': 1.6,
    'DEF': 1.1,
    'MAG': 0.4,
    'SPR': 0.85,
    'SPD': 9,
}
monk_skills = [
    skills.ThousandFists(),
    skills.BurstingQi(),
]
HEROES.append(Hero('monk', monk_dict, monk_skills))

ninja_dict = {
    'HP': 1.7,
    'ATK': 1.4,
    'DEF': 1.1,
    'MAG': 1.15,
    'SPR': 1.1,
    'SPD': 5,
}
ninja_skills = [
    skills.CuriousBox(),
    skills.BootyTrap(),
]
HEROES.append(Hero('ninja', ninja_dict, ninja_skills))

knight_dict = {
    'HP': 2.2,
    'ATK': 1.15,
    'DEF': 1.5,
    'MAG': 0.8,
    'SPR': 1.4,
    'SPD': 4
}
knight_skills = [
    skills.RighteousInspiration(),
    skills.ChivalrousProtection(),
]
HEROES.append(Hero('knight', knight_dict, knight_skills))


MOBS = []
hound_dict = {
    'HP': 1.5,
    'ATK': 0.5,
    'DEF': 1,
    'MAG': 0.3,
    'SPR': 1.1,
    'SPD': 9
}
hound_skills = []

beastmaster_dict = {
    'HP': 3,
    'ATK': 0.3,
    'DEF': 1.7,
    'MAG': 0.3,
    'SPR': 1.3,
    'SPD': 1
}
beastmaster_skills = [skills.NightCall(),
                      skills.BloodMoon()]

MOBS.append(Mob('HellHoundA', hound_dict, hound_skills))
MOBS.append(Mob('HellHoundB', hound_dict, hound_skills))
MOBS.append(Mob('BeastMaster', beastmaster_dict, beastmaster_skills))
