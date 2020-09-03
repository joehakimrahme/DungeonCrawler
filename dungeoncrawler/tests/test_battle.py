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
import unittest
from unittest.mock import patch

from dungeoncrawler import battle
from dungeoncrawler import skills
from dungeoncrawler import utils


class BattleTest(unittest.TestCase):

    def setUp(self):
        self.team = [
            utils.create_neutral_hero(skills=[skills.Heal()]),
            utils.create_neutral_hero(skills=[skills.Heal()]),
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
            self.assertEqual(result[key], skills.ATK(), (result, key))

    def test_generate_choice_full_mp(self):
        for f in self.battle.yourteam:
            f.mp += f.maxMP
        result = self.battle.generate_choices(self.battle)
        for key in self.battle.yourteam:
            self.assertEqual(result[key.name], skills.Heal(), (result, key))
        for key in self.battle.enemyteam:
            self.assertEqual(result[key.name], skills.ATK(), (result, key))

    def test_generate_choice_mob(self):
        self.battle.enemyteam[0].skills = [skills.NightCall()]
        self.battle.enemyteam[1].skills = [skills.NightCall()]
        self.battle.enemyteam[1].hp -= 300
        result = self.battle.generate_choices(self.battle)
        self.assertEqual(
            result[self.battle.enemyteam[0].name], skills.NightCall())
        self.battle.enemyteam[1].hp += 300
        result = self.battle.generate_choices(self.battle)
        self.assertEqual(result[self.battle.enemyteam[0].name], skills.ATK())

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
            combo[0].name: skills.ATK(),
            combo[1].name: skills.ATK(),
        }
        _ = self.battle.execute_step(combo, choices)
        self.assertLess(self.team[0].hp_ratio, 100)
        self.assertLess(self.mobs[0].hp_ratio, 100)
