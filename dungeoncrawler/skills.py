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

import abc
import random

from dungeoncrawler import utils


class Ability(abc.ABC):
    mp_cost = 100

    def __init__(self, world, caster):
        self.world = world
        self.caster = caster

    def __repr__(self):
        return str(type(self).__name__)

    def predicate(self, world):
        return True

    def effect(self, combo):
        raise NotImplementedError()

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


class ATTACK(Ability):
    mp_cost = 0

    def effect(self, combo):
        _targets = []
        _rivals_set = set(self.world.rivals(self.caster))
        _alive_in_combo_set = {h for h in combo if h.hp}
        _combo_targets = _rivals_set & _alive_in_combo_set
        if _combo_targets:
            sorted_hp = sorted(_combo_targets, key=lambda x: x.hp)
            if len(sorted_hp) > 1:
                _targets.append(random.choice(sorted_hp[:2]))
            if len(sorted_hp) == 1:
                _targets.append(sorted_hp[0])
        dmg = 0
        for _t in _targets:
            dmg = self.physical_damage(self.caster, _t, 1)
            _oldt = _t.hp
            _t.hp -= dmg

            # coloring
            if self.caster in self.world.yourteam:
                color = utils.color_green
            else:
                color = utils.color_red

            utils.slow_type("%s: swings at %s dealing %s dmg. (%d -> %d)\n" % (
                utils.bold(color(self.caster.name)),
                _t.name, utils.bold(str(dmg)), _oldt, _t.hp))
            _mp_gain = dmg * 0.3
            if _t.hp:
                _t.mp += 60 if _mp_gain > 60 else _mp_gain
            self.caster.mp += 30 if _mp_gain > 30 else _mp_gain


class WellIntentionedWish(Ability):
    mp_cost = 70

    def effect(self, combo):
        _targets = []
        _combo_targets = []
        for h in self.world.yourteam:
            if h in combo and h.hp:
                _combo_targets.append(h)
        if not _combo_targets:
            _combo_targets = self.world.yourteam

        if _combo_targets:
            self.caster.mp = 0
            _targets.append(min(_combo_targets, key=lambda x: x.hp_ratio))

        for _t in _targets:
            dmg = self.healing_damage(self.caster, 3)
            _oldt = _t.hp
            _t.hp += dmg
            utils.slow_type("%s: [%s] on %s for %s HP. (%d -> %d)\n" % (
                utils.bold(utils.color_green(self.caster.name)),
                utils.color_yellow(str(self)),
                _t.name, utils.bold(str(dmg)), _oldt, _t.hp))


class ThousandFists(Ability):
    mp_cost = 120

    def effect(self, combo):
        _targets = []
        _combo_targets = (h for h in self.world.enemyteam if h.hp)
        if _combo_targets:
            self.caster.mp = 0
            sorted_hpdef = sorted(_combo_targets,
                                  key=lambda x: x.hp_ratio / (5 * x.DEF))
            if sorted_hpdef:
                _targets.append(sorted_hpdef[-1])
        for _t in _targets:
            dmg = self.physical_damage(self.caster, _t, 3)
            _oldt = _t.hp
            _t.hp -= dmg
            utils.slow_type(
                "%s: [%s] on %s dealing %s dmg"
                ". (%d -> %d)\n" % (
                    utils.bold(utils.color_green(self.caster.name)),
                    utils.color_yellow(str(self)),
                    _t.name, utils.bold(str(dmg)), _oldt, _t.hp))


class SilentPrayer(Ability):
    mp_cost = 70

    def effect(self, combo):
        _targets = set(self.world.yourteam) & {h for h in combo if h.hp}
        _t = min(_targets, key=lambda x: x.mp_ratio)
        self.caster.mp = 0
        _t.mp += _t.maxMP
        utils.slow_type(
            "%s: [%s] on %s restoring full MP.\n" % (
                utils.bold(utils.color_green(self.caster.name)),
                utils.color_yellow(str(self)), _t.name))


class NovaBlast(Ability):
    mp_cost = 120

    def effect(self, combo):
        _targets = self.world.enemyteam
        for _t in _targets:
            self.caster.mp = 0
            dmg = self.magical_damage(self.caster, _t, 3.5)
            _oldt = _t.hp
            _t.hp -= dmg
            utils.slow_type(
                "%s: [%s] on %s dealing %s dmg. (%d -> %d)\n" % (
                    utils.bold(utils.color_green(self.caster.name)),
                    utils.color_yellow(str(self)),
                    _t.name, utils.bold(str(dmg)), _oldt, _t.hp))


class Focus(Ability):
    mp_cost = 120

    def effect(self, combo):
        self.caster.mp = 60
        self.caster.MAG *= 1.5
        self.caster.SPD *= 1.5
        utils.slow_type("%s: [%s] on self increasing MAG/SPD.\n" % (
            utils.bold(utils.color_green(self.caster.name)),
            utils.color_yellow(str(self))))


class BurstingQi(Ability):
    mp_cost = 120

    def effect(self, combo):
        self.caster.mp = 60
        self.caster.ATK *= 1.2
        self.caster.DEF *= 1.2
        utils.slow_type(
            "%s: [%s] on self increase ATK and DEF.\n" % (
                utils.bold(utils.color_green(self.caster.name)),
                utils.color_yellow(str(self))))


class CuriousBox(Ability):
    mp_cost = 100

    def effect(self, combo):
        _targets = [m for m in self.world.enemyteam if m.hp]
        if _targets:
            _t = random.choice(_targets)
            self.caster.mp = 0
            _mult = int((random.random() * random.random() * 3) + 1)
            dmg = self.hybrid_damage(self.caster, _t, _mult)
            _oldt = _t.hp
            _t.hp -= dmg
            utils.slow_type(
                "%s: [%s] on %s dealing %s dmg. (%d -> %d)\n" % (
                    utils.bold(utils.color_green(self.caster.name)),
                    utils.color_yellow(str(self)),
                    _t.name, utils.bold(str(dmg)), _oldt, _t.hp))
            if any([m.hp for m in self.world.enemyteam]):
                if random.random() < 0.6:
                    self.effect((unit for unit in combo if unit.hp))


class BootyTrap(Ability):
    mp_cost = 100

    def effect(self, combo):
        if self.world.enemyteam:
            self.caster.mp = 0
            _t = max(self.world.enemyteam, key=lambda x: x.DEF)
            _oldt = _t.hp
            dmg = self.hybrid_damage(self.caster, _t, 1.5)
            _t.hp -= dmg
            utils.slow_type(
                "%s: [%s] on %s dealing %s dmg. (%d -> %d)\n" % (
                    utils.bold(utils.color_green(self.caster.name)),
                    utils.color_yellow(str(self)),
                    _t.name, utils.bold(str(dmg)), _oldt, _t.hp))
            if _t.hp:
                _t.DEF *= 0.8
                _t.SPR *= 0.8
                utils.slow_type(
                    "%s: [%s] on %s decreases DEF/SPR.\n" % (
                        utils.bold(utils.color_green(self.caster.name)),
                        utils.color_yellow(str(self)), _t.name))


class ChivalrousProtection(Ability):
    mp_cost = 100

    def effect(self, combo):
        for _t in self.world.yourteam:
            if _t.hp:
                self.caster.mp = 0
                _t.DEF *= 1.8
                _t.SPR *= 1.8
                utils.slow_type(
                    "%s: [%s] on %s increases DEF/SPR.\n" % (
                        utils.bold(utils.color_green(self.caster.name)),
                        utils.color_yellow(str(self)), _t.name))


class RighteousInspiration(Ability):
    mp_cost = 100

    def effect(self, combo):
        _targets = [h for h in self.world.yourteam if (h.mp * h.hp)]
        for _t in _targets:
            if _t.hp and _t.mp:
                self.caster.mp = 0
                _t.mp *= 3
                utils.slow_type(
                    "%s: [%s] on %s restoring MP.\n" % (
                        utils.bold(utils.color_green(self.caster.name)),
                        utils.color_yellow(str(self)), _t.name))


class BubblyPickMeUp(Ability):
    def predicate(self, world):
        return any((mob.hp_ratio < 60 for mob in world.enemyteam))

    def effect(self, combo):
        _targets = [m for m in self.world.enemyteam if m.hp]
        for _t in _targets:
            dmg = self.healing_damage(self.caster, 1.8)
            _oldt = _t.hp
            _t.hp += dmg
            utils.slow_type(
                "%s: [%s] on %s healing for %s. (%d -> %d)\n" % (
                    utils.bold(utils.color_red(self.caster.name)),
                    utils.color_yellow(str(self)),
                    _t.name, utils.bold(str(dmg)), _oldt, _t.hp))


class TemporaryInsanity(Ability):
    def predicate(self, world):
        return True

    def effect(self, combo):
        _targets = self.world.enemyteam
        for _t in _targets:
            _t.ATK *= 1.35
            utils.slow_type("%s: [%s] on %s increases ATK.\n" % (
                utils.bold(utils.color_red(self.caster.name)),
                utils.color_yellow(str(self)), _t.name))


class AngryOwner(Ability):

    def predicate(self, world):
        if len(world.enemyteam) == 1:
            return True

    def effect(self, combo):
        _targets = [h for h in self.world.yourteam if h.hp]
        for _t in _targets:
            self.caster.mp = 0
            dmg = self.hybrid_damage(self.caster, _t, 3.5)
            _oldt = _t.hp
            _t.hp -= dmg
            utils.slow_type(
                "%s: [%s] on %s dealing %s dmg. (%d -> %d)\n" % (
                    utils.bold(utils.color_red(self.caster.name)),
                    utils.color_yellow(str(self)),
                    _t.name, utils.bold(str(dmg)), _oldt, _t.hp))
        self.caster.ATK *= 1.35
        utils.slow_type(
            "%s: [%s] on self increasing ATK.\n" % (
                utils.bold(utils.color_red(self.caster.name)),
                utils.color_yellow(str(self))))
