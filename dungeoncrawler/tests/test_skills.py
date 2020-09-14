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
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest
from unittest import mock
from unittest.mock import MagicMock
from unittest.mock import patch

from dungeoncrawler import skills
from dungeoncrawler import utils


class BaseSkillTest(unittest.TestCase):

    def setUp(self):
        self.fighters = [
            utils.create_neutral_fighter(),
            utils.create_neutral_fighter(),
        ]
        self.ability = skills.Ability

    def test_physical_damage(self):
        _mock = mock.Mock()
        result = self.ability(_mock, _mock).physical_damage(
            self.fighters[0], self.fighters[1], multiplier=1)
        self.assertGreaterEqual(result, 10)

    def test_physical_damage_linear_multiplier(self):
        """Assert that the damage grows linearly with the multiplier argument.

        """
        _mock = mock.Mock()
        _ability = self.ability(_mock, _mock)
        result = [
            _ability.physical_damage(
                self.fighters[0], self.fighters[1], multiplier=1),
            _ability.physical_damage(
                self.fighters[0], self.fighters[1], multiplier=2),
            _ability.physical_damage(
                self.fighters[0], self.fighters[1], multiplier=4),
        ]
        self.assertEqual(result[0] * 2, result[1])
        self.assertEqual(result[1] * 2, result[2])


class ATKTest(unittest.TestCase):
    def setUp(self):
        self.fighters = [
            utils.create_neutral_fighter(),
            utils.create_neutral_fighter(),
        ]
        self.ability = skills.ATTACK

    # unittest.mock.patch slow_type in order to avoid wasting time on
    # visual execution
    @patch('dungeoncrawler.utils.slow_type')
    def test_ATK_effect(self, slow_type):
        world = mock.Mock()
        world.rivals = MagicMock(return_value=(self.fighters[1],))
        world.yourteam = self.fighters
        self.ability(world, self.fighters[0]).effect(self.fighters)
        self.assertGreater(self.fighters[0].mp, 0,
                           "attacker didn't gain mp: %s" % self.fighters[0].mp)
        self.assertGreater(self.fighters[1].mp, 0,
                           "defender didn't gain mp: %s" % self.fighters[0].mp)
        self.assertLess(self.fighters[1].hp_ratio, 100,
                        "defender didn't lose hp: %d/%d" % (
                            self.fighters[1].hp,
                            self.fighters[1].maxHP))


class HealTest(unittest.TestCase):
    def setUp(self):
        self.fighters = [
            utils.create_neutral_fighter(),
            utils.create_neutral_fighter(),
        ]
        self.ability = skills.WellIntentionedWish

    # unittest.mock.patch slow_type in order to avoid wasting time on
    # visual execution
    @patch('dungeoncrawler.utils.slow_type')
    def test_Heal_effect(self, slow_type):
        world = mock.Mock()
        world.yourteam = self.fighters
        self.fighters[1].hp -= 10
        self.ability(world, self.fighters[0]).effect(self.fighters[1:])
        self.assertEqual(self.fighters[0].mp, 0,
                         "healer didn't use mp: %s" % self.fighters[0].mp)
        self.assertEqual(self.fighters[1].hp_ratio, 100,
                         "target didn't gain hp: %s" % self.fighters[0].mp)


class SilentPrayerTest(unittest.TestCase):
    def setUp(self):
        skill = [skills.Ability]
        self.team = [
            utils.create_neutral_hero(skills=skill, name="test-1"),
            utils.create_neutral_hero(skills=skill)
        ]
        self.ability = skills.SilentPrayer

    @patch('dungeoncrawler.utils.slow_type')
    def test_silentprayer_effect(self, slow_type):
        self.team[0].mp += self.team[0].maxMP
        self.assertEqual(self.team[1].mp, 0)
        world = mock.Mock()
        world.yourteam = self.team
        self.ability(world, self.team[0]).effect(self.team)
        self.assertLess(self.team[0].mp, self.team[0].maxMP)
        self.assertEqual(self.team[1].mp_ratio, 100)


class FocusTest(unittest.TestCase):
    def setUp(self):
        self.team = [
            utils.create_neutral_fighter()
        ]
        self.ability = skills.Focus

    @patch('dungeoncrawler.utils.slow_type')
    def test_focus_effect(self, slow_type):
        _oldt = self.team[0].MAG
        world = mock.Mock()
        self.ability(world, self.team[0]).effect(self.team)
        self.assertGreater(self.team[0].MAG, _oldt)


class NovaBlastTest(unittest.TestCase):
    def setUp(self):
        self.team = [
            utils.create_neutral_fighter()
        ]
        self.mobs = [
            utils.create_neutral_mob(),
            utils.create_neutral_mob(),
        ]
        self.ability = skills.NovaBlast

    @patch('dungeoncrawler.utils.slow_type')
    @patch('dungeoncrawler.skills.print')
    def test_novablast_effect(self, slow_type, print):
        world = mock.Mock()
        world.enemyteam = self.mobs
        _oldt = [h.hp for h in world.enemyteam]
        self.ability(world, self.team[0]).effect(self.team + self.mobs)
        _newt = [h.hp for h in world.enemyteam]
        self.assertLess(_newt[0], _oldt[0])
        self.assertLess(_newt[1], _oldt[1])


class BurstingQiTest(unittest.TestCase):
    def setUp(self):
        self.team = [
            utils.create_neutral_fighter()
        ]
        self.ability = skills.BurstingQi

    @patch('dungeoncrawler.utils.slow_type')
    def test_burstingqi_effect(self, slow_type):
        world = mock.Mock()
        _oldatk = self.team[0].ATK
        _olddef = self.team[0].DEF
        self.ability(world, self.team[0]).effect(self.team)
        self.assertGreater(self.team[0].ATK, _oldatk)
        self.assertGreater(self.team[0].DEF, _olddef)


class BubblyPickMeUpTest(unittest.TestCase):
    def setUp(self):
        self.fighters = [
            utils.create_neutral_fighter(),
            utils.create_neutral_fighter(),
        ]
        self.mobs = [
            utils.create_neutral_mob(),
            utils.create_neutral_mob()
        ]
        self.ability = skills.BubblyPickMeUp

    # unittest.mock.patch slow_type in order to avoid wasting time on
    # visual execution
    @patch('dungeoncrawler.utils.slow_type')
    def test_bubblyl_effect(self, slow_type):
        world = mock.Mock()
        world.enemyteam = self.mobs
        self.mobs[1].hp -= 300
        self.ability(world, self.mobs[0]).effect(self.fighters + self.mobs)
        self.assertGreater(self.mobs[1].hp_ratio, 40)


class TemporaryInsanityTest(unittest.TestCase):
    def setUp(self):
        self.mobs = [
            utils.create_neutral_mob(),
            utils.create_neutral_mob()
        ]
        self.ability = skills.TemporaryInsanity

    # unittest.mock.patch slow_type in order to avoid wasting time on
    # visual execution
    @patch('dungeoncrawler.utils.slow_type')
    def test_insanity_effect(self, slow_type):
        world = mock.Mock()
        world.enemyteam = self.mobs
        self.ability(world, self.mobs[0]).effect(self.mobs)
        for mob in self.mobs:
            self.assertGreater(mob.ATK, 100)


class AngryOwnertest(unittest.TestCase):
    def setUp(self):
        self.team = [
            utils.create_neutral_hero(),
            utils.create_neutral_hero()
        ]
        self.mobs = [
            utils.create_neutral_mob(),
            utils.create_neutral_mob()
        ]
        self.ability = skills.AngryOwner

    # unittest.mock.patch slow_type in order to avoid wasting time on
    # visual execution
    @patch('dungeoncrawler.utils.slow_type')
    def test_insanity_effect(self, slow_type):
        world = mock.Mock()
        world.yourteam = self.team
        world.enemyteam = self.mobs

        self.ability(world, self.mobs[0]).effect(self.mobs)
        self.assertTrue(all(h.hp_ratio < 100 for h in self.team))
