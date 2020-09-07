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

from dungeoncrawler import utils


class Ability(object):

    def __init__(self, name, mp_cost=0):
        self.name = name
        self.mp_cost = mp_cost

    def __repr__(self):
        return self.name

    def __eq__(self, ability):
        return self.name == ability.name

    def effect(self, world, main, combo):
        utils.slow_type("%s: %s\n" % (main.name, self.name))

    def physical_damage(self, source, target, multiplier):
        return int((source.ATK**2) / target.DEF * multiplier)

    def healing_damage(self, source, multiplier):
        return int(source.SPR / 1.3 * multiplier)

    def hybrid_damage(self, source, target, multiplier):
        _a = self.physical_damage(source, target, multiplier)
        _b = self.magical_damage(source, target, multiplier)
        return int((_a + _b) / 2)

    def magical_damage(self, source, target, multiplier):
        return int(source.MAG**2 / target.SPR * multiplier)

    def predicate(self, world):
        return True


class ATK(Ability):
    def __init__(self):
        super(ATK, self).__init__(name='ATTACK')

    def effect(self, world, main, combo):
        _targets = []
        _combo_targets = set(world.rivals(main)) & {h for h in combo if h.hp}
        if _combo_targets:
            sorted_hp = sorted(_combo_targets, key=lambda x: x.hp)
            if len(sorted_hp) > 1:
                _targets.append(random.choice(sorted_hp[:2]))
            if len(sorted_hp) == 1:
                _targets.append(sorted_hp[0])
        dmg = 0
        for _t in _targets:
            dmg = self.physical_damage(main, _t, 1)
            _oldt = _t.hp
            _t.hp -= dmg

            # coloring
            if main in world.yourteam:
                color = utils.color_green
            else:
                color = utils.color_red

            utils.slow_type("%s: swings at %s dealing %s dmg. (%d -> %d)\n" % (
                utils.bold(color(main.name)),
                _t.name, utils.bold(str(dmg)), _oldt, _t.hp))
            _mp_gain = dmg * 0.3
            if _t.hp:
                _t.mp += 60 if _mp_gain > 60 else _mp_gain
            main.mp += 40 if _mp_gain > 40 else _mp_gain


class Heal(Ability):
    def __init__(self):
        super(Heal, self).__init__(name='A Well Intentioned Wish', mp_cost=70)

    def effect(self, world, main, combo):
        _targets = []
        _combo_targets = [h for h in world.yourteam if h.hp]
        if _combo_targets:
            main.mp = 0
            _targets.append(min(_combo_targets, key=lambda x: x.hp_ratio))

        for _t in _targets:
            dmg = self.healing_damage(main, 3)
            _oldt = _t.hp
            _t.hp += dmg
            utils.slow_type("%s: [%s] on %s for %sHP. (%d -> %d)\n" % (
                utils.bold(utils.color_green(main.name)),
                utils.color_yellow(self.name),
                _t.name, utils.bold(str(dmg)), _oldt, _t.hp))


class ThousandFists(Ability):
    def __init__(self):
        super(ThousandFists, self).__init__(name="A Thousand Fists",
                                            mp_cost=120)

    def effect(self, world, main, combo):
        _targets = []
        _combo_targets = set(world.rivals(main)) & {h for h in combo if h.hp}
        if _combo_targets:
            main.mp = 0
            sorted_hpdef = sorted(_combo_targets,
                                  key=lambda x: x.hp_ratio / (5 * x.DEF))
            if sorted_hpdef:
                _targets.append(sorted_hpdef[-1])
        for _t in _targets:
            dmg = self.physical_damage(main, _t, 3)
            _oldt = _t.hp
            _t.hp -= dmg
            utils.slow_type(
                "%s: [%s] on %s dealing %s dmg"
                ". (%d -> %d)\n" % (
                    utils.bold(utils.color_green(main.name)),
                    utils.color_yellow(self.name),
                    _t.name, utils.bold(str(dmg)), _oldt, _t.hp))


class SilentPrayer(Ability):
    def __init__(self):
        super(SilentPrayer, self).__init__(name="A Silent Prayer", mp_cost=70)

    def effect(self, world, main, combo):
        _targets = set(world.yourteam) & {h for h in combo if h.hp}
        _t = min(_targets, key=lambda x: x.mp_ratio)
        _t.mp += _t.maxMP
        utils.slow_type(
            "%s: [%s] on %s restoring full MP.\n" % (
                utils.bold(utils.color_green(main.name)),
                utils.color_yellow(self.name), _t.name))
        main.mp = 0


class NovaBlast(Ability):
    def __init__(self):
        super(NovaBlast, self).__init__(name="Supernova Blast",
                                        mp_cost=120)

    def effect(self, world, main, combo):
        _targets = world.enemyteam
        for _t in _targets:
            main.mp = 0
            dmg = self.magical_damage(main, _t, 3.5)
            _oldt = _t.hp
            _t.hp -= dmg
            utils.slow_type(
                "%s: [%s] on %s dealing %s dmg. (%d -> %d)\n" % (
                    utils.bold(utils.color_green(main.name)),
                    utils.color_yellow(self.name),
                    _t.name, utils.bold(str(dmg)), _oldt, _t.hp))


class Focus(Ability):
    def __init__(self):
        super(Focus, self).__init__(name="Sharp Focus", mp_cost=120)

    def effect(self, world, main, combo):
        main.mp = 60
        main.MAG *= 1.5
        main.SPD *= 1.5
        utils.slow_type("%s: [%s] on self increasing MAG/SPD.\n" % (
            utils.bold(utils.color_green(main.name)),
            utils.color_yellow(self.name)))


class BurstingQi(Ability):
    def __init__(self):
        super(BurstingQi, self).__init__(name="Bursting Qi", mp_cost=120)

    def effect(self, world, main, combo):
        main.mp = 60
        main.ATK *= 1.2
        main.DEF *= 1.2
        utils.slow_type(
            "%s: [%s] on self increase ATK and DEF.\n" % (
                utils.bold(utils.color_green(main.name)),
                utils.color_yellow(self.name)))


class CuriousBox(Ability):
    def __init__(self):
        super(CuriousBox, self).__init__(name="A Curious Box", mp_cost=100)

    def effect(self, world, main, combo):
        _targets = [m for m in world.enemyteam if m.hp]
        if _targets:
            _t = random.choice(_targets)
            main.mp = 0
            _mult = int((random.random() * random.random() * 3) + 1)
            dmg = self.hybrid_damage(main, _t, _mult)
            _oldt = _t.hp
            _t.hp -= dmg
            utils.slow_type(
                "%s: [%s] on %s dealing %s dmg. (%d -> %d)\n" % (
                    utils.bold(utils.color_green(main.name)),
                    utils.color_yellow(self.name),
                    _t.name, utils.bold(str(dmg)), _oldt, _t.hp))
            if random.random() < 0.6 and any([m.hp for m in world.enemyteam]):
                self.effect(world, main, combo)


class BootyTrap(Ability):
    def __init__(self):
        super(BootyTrap, self).__init__(name="Booby Trap", mp_cost=100)

    def effect(self, world, main, combo):
        _t = max(world.enemyteam, key=lambda x: x.DEF)
        if _t:
            main.mp = 0
            _oldt = _t.hp
            dmg = self.hybrid_damage(main, _t, 1.5)
            _t.hp -= dmg
            utils.slow_type(
                "%s: [%s] on %s dealing %s dmg. (%d -> %d)\n" % (
                    utils.bold(utils.color_green(main.name)),
                    utils.color_yellow(self.name),
                    _t.name, utils.bold(str(dmg)), _oldt, _t.hp))
            _t.DEF *= 0.8
            _t.SPR *= 0.8
            utils.slow_type(
                "%s: [%s] on %s decreases DEF/SPR.\n" % (
                    utils.bold(utils.color_green(main.name)),
                    utils.color_yellow(self.name), _t.name))


class ChivalrousProtection(Ability):
    def __init__(self):
        super(ChivalrousProtection, self).__init__(
            name="Chivalrous Protection", mp_cost=80)

    def effect(self, world, main, combo):
        for _t in world.yourteam:
            if _t.hp:
                main.mp = 0
                _t.DEF *= 1.2
                _t.SPR *= 1.2
                utils.slow_type(
                    "%s: [%s] on %s increases DEF/SPR.\n" % (
                        utils.bold(utils.color_green(main.name)),
                        utils.color_yellow(self.name), _t.name))


class RighteousInspiration(Ability):
    def __init__(self):
        super(RighteousInspiration, self).__init__(
            name="Righteous Inspiration", mp_cost=80)

    def effect(self, world, main, combo):
        for _t in world.yourteam:
            if _t.hp:
                main.mp = 0
                _t.mp *= 2
                utils.slow_type(
                    "%s: [%s] on %s restoring MP.\n" % (
                        utils.bold(utils.color_green(main.name)),
                        utils.color_yellow(self.name), _t.name))


class NightCall(Ability):
    def __init__(self):
        super(NightCall, self).__init__(name="Night Call")

    def predicate(self, world):
        return any((mob.hp_ratio < 60 for mob in world.enemyteam))

    def effect(self, world, main, combo):
        _targets = world.enemyteam
        for _t in _targets:
            dmg = self.healing_damage(main, 1.8)
            _oldt = _t.hp
            _t.hp += dmg
            utils.slow_type(
                "%s: [%s] on %s healing for %s. (%d -> %d)\n" % (
                    utils.bold(utils.color_red(main.name)),
                    utils.color_yellow(self.name),
                    _t.name, utils.bold(str(dmg)), _oldt, _t.hp))


class BloodMoon(Ability):
    def __init__(self):
        super(BloodMoon, self).__init__(name="Blood Moon")

    def predicate(self, world):
        return True

    def effect(self, world, main, combo):
        _targets = world.enemyteam
        for _t in _targets:
            _t.ATK *= 1.35
            utils.slow_type("%s: [%s] on %s increases ATK.\n" % (
                utils.bold(utils.color_red(main.name)),
                utils.color_yellow(self.name), _t.name))


class NatureWrath(Ability):
    def __init__(self):
        super(NatureWrath, self).__init__(name="Nature Wrath")

    def predicate(self, world):
        if len(world.enemyteam) == 1:
            return True

    def effect(self, world, main, combo):
        _targets = [h for h in world.yourteam if h.hp]
        for _t in _targets:
            main.mp = 0
            dmg = self.hybrid_damage(main, _t, 3.5)
            _oldt = _t.hp
            _t.hp -= dmg
            utils.slow_type(
                "%s: [%s] on %s dealing %d dmg. (%d -> %d)\n" % (
                    utils.bold(utils.color_red(main.name)),
                    utils.color_yellow(self.name),
                    _t.name, utils.bold(str(dmg)), _oldt, _t.hp))
        main.ATK *= 1.35
        utils.slow_type(
            "%s: [%s] on self increasing ATK.\n" % (
                utils.bold(utils.color_red(main.name)),
                utils.color_yellow(self.name)))
