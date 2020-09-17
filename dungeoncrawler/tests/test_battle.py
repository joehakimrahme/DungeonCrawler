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
import unittest
from unittest.mock import patch

from dungeoncrawler import battle
from dungeoncrawler import hero
from dungeoncrawler import skills
from dungeoncrawler import utils


class BattleTest(unittest.TestCase):

    def setUp(self):
        self.team = [
            utils.create_neutral_hero(skills=[skills.WellIntentionedWish]),
            utils.create_neutral_hero(skills=[skills.WellIntentionedWish]),
        ]
        self.mobs = [
            utils.create_neutral_mob(),
            utils.create_neutral_mob(),
        ]
        self.battle = battle.Battle(self.team, self.mobs)

    def test_rivals(self):
        result = self.battle.rivals(self.team[0])
        self.assertEqual(self.mobs, result)
        result = self.battle.rivals(self.mobs[0])
        self.assertEqual(self.team, result)

    def test_allies(self):
        result = self.battle.allies(self.team[0])
        self.assertEqual(self.team, result)
        result = self.battle.allies(self.mobs[0])
        self.assertEqual(self.mobs, result)

    def test_weighted_shuffle(self):
        _combo = self.team + self.mobs
        # the _combo variable will be mutated by the weighted_shuffle
        # method. We preemptively copy it to check the result later.
        _combo_copy = _combo[:]
        result = self.battle.weighted_shuffle(_combo)
        self.assertEqual(set(_combo_copy), set(result))

    def test_check_for_win(self):
        result = self.battle.check_for_win()
        self.assertIsNone(result)
        for f in self.battle.yourteam:
            f.hp = 0
        result = self.battle.check_for_win()
        self.assertFalse(result)
        for f in self.battle.yourteam:
            f.hp += f.maxHP
        for f in self.battle.enemyteam:
            f.hp = 0
        result = self.battle.check_for_win()
        self.assertTrue(result)

    def test_generate_choice_zero_mp(self):
        result = self.battle.generate_choices(self.battle)
        for key in result:
            self.assertIsInstance(result[key], skills.ATTACK, (result, key))

    def test_generate_choice_full_mp(self):
        for f in self.battle.yourteam:
            f.mp += f.maxMP
        result = self.battle.generate_choices(self.battle)
        for key in self.battle.yourteam:
            self.assertIsInstance(result[key.name], skills.WellIntentionedWish,
                                  (result, key))
        for key in self.battle.enemyteam:
            self.assertIsInstance(result[key.name], skills.ATTACK,
                                  (result, key))

    def test_generate_choice_mob(self):
        self.battle.enemyteam[0].skills = [skills.BubblyPickMeUp]
        self.battle.enemyteam[1].skills = [skills.BubblyPickMeUp]
        self.battle.enemyteam[1].hp -= 300
        result = self.battle.generate_choices(self.battle)
        self.assertIsInstance(
            result[self.battle.enemyteam[0].name], skills.BubblyPickMeUp)
        self.battle.enemyteam[1].hp += 300
        result = self.battle.generate_choices(self.battle)
        self.assertIsInstance(
            result[self.battle.enemyteam[0].name], skills.ATTACK)

    @patch('dungeoncrawler.battle.input')
    def test_generate_combo(self, mock_input):
        mock_input.return_value = "1"
        result = self.battle.generate_combo()
        self.assertIn(self.team[0], result)
        self.assertNotIn(self.team[1], result)

    @patch('dungeoncrawler.utils.slow_type')
    def test_execute_step(self, slow_type):
        combo = [self.team[0], self.mobs[0]]
        choices = {
            combo[0].name: skills.ATTACK(self.battle, combo[0]),
            combo[1].name: skills.ATTACK(self.battle, combo[1]),
        }
        _ = self.battle.execute_step(combo, choices)
        self.assertLess(self.team[0].hp_ratio, 100)
        self.assertLess(self.mobs[0].hp_ratio, 100)


def random_input(prompt=None):
    alphabet = [
        '1', '12', '123', '124', '125', '13', '134', '135', '14', '145', '15',
        '2', '23', '234', '235', '24', '245', '25', '3', '34', '345', '35',
        '4', '45', '5',
    ]
    return random.choice(alphabet)


class RandomBattlesTest(unittest.TestCase):

    @patch('builtins.input', random_input)
    @patch('builtins.print')
    @patch('dungeoncrawler.utils.slow_type')
    def test_100random_battle(self, print, slow_type):
        sample = 100
        wins = 0
        for _ in range(sample):
            _heroes = [
                hero.Hero('wizard', hero.wizard_dict, hero.wizard_skills),
                hero.Hero('cleric', hero.cleric_dict, hero.cleric_skills),
                hero.Hero('monk', hero.monk_dict, hero.monk_skills),
                hero.Hero('ninja', hero.ninja_dict, hero.ninja_skills),
                hero.Hero('knight', hero.knight_dict, hero.knight_skills)
            ]
            _mobs = [
                hero.Mob('Charging Drunk A', hero.drunk_dict,
                         hero.drunk_skills),
                hero.Mob('Charging Drunk B', hero.drunk_dict,
                         hero.drunk_skills),
                hero.Mob('Crazed Bartender', hero.bartender_dict,
                         hero.bartender_skills)
            ]
            if battle.Battle(_heroes, _mobs).battle_loop():
                wins += 1
