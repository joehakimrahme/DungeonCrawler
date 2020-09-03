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

from dungeoncrawler import hero
from dungeoncrawler import skills


class FighterTest(unittest.TestCase):

    def setUp(self):
        self.fighter = hero.Fighter(
            name="test-Fighter",
            attributes={
                'HP': 10,
                'ATK': 1,
                'DEF': 1,
                'MAG': 1,
                'SPR': 1,
                'SPD': 1
            },
            skills=(skills.Heal(),))

    def test_fighter_maxMP(self):
        """maxMP is equal the highest mp_cost of a fighter's skills. Or 999 if
        no skills are found.

        """
        _cost = skills.Heal().mp_cost
        self.assertEqual(self.fighter.maxMP, _cost)

        _old_skills = self.fighter.skills
        self.fighter.skills = ()
        self.assertEqual(self.fighter.maxMP, 999)
        self.fighter.skills = _old_skills

    def test_fighter_hp(self):
        """A fighter's HP should start at maxHP, never go below 0 or over
        maxHP.

        """
        self.assertEqual(self.fighter.hp, self.fighter.maxHP)
        self.fighter.hp -= self.fighter.maxHP + 1
        self.assertEqual(self.fighter.hp, 0)
        self.fighter.hp += self.fighter.maxHP * 2
        self.assertEqual(self.fighter.hp, self.fighter.maxHP)

    def test_fighter_mp(self):
        """MP starts at 0. It should never go below 0 or over maxMP.

        """
        self.assertEqual(self.fighter.mp, 0)
        self.fighter.mp += self.fighter.maxMP * 2
        self.assertEqual(self.fighter.mp, self.fighter.maxMP)
        self.fighter.mp -= self.fighter.maxMP + 1
        self.assertEqual(self.fighter.mp, 0)


class HeroTest(FighterTest):

    def setUp(self):
        self.fighter = hero.Hero(
            name="test-Hero",
            attributes={
                'HP': 10,
                'ATK': 1,
                'DEF': 1,
                'MAG': 1,
                'SPR': 1,
                'SPD': 1
            },
            skills=(skills.Heal(),))


class MobTest(FighterTest):

    def setUp(self):
        self.fighter = hero.Mob(
            name="test-Mob",
            attributes={
                'HP': 10,
                'ATK': 1,
                'DEF': 1,
                'MAG': 1,
                'SPR': 1,
                'SPD': 1
            }, skills=None)

    def test_fighter_maxMP(self):
        """A mob should have no mp-skills.

        """
        self.assertEqual(self.fighter.maxMP, 999)


if __name__ == "__main__":
    unittest.main()
