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

    def predicate(self):
        return self.caster.mp == self.caster.maxMP

    def effect(self, combo):
        self.opening_words()
        _targets = self.targets(combo)
        if _targets:
            self.caster.mp -= self.mp_cost
            for _t in _targets:
                _dmg, _old, _new = self.single_effect(_t)
                self.log_skill(_dmg, _t, _old, _new)
        self.closing_words()

    def targets(self, combo):
        raise NotImplementedError

    def single_effect(self, target):
        raise NotImplementedError

    def log_skill(self, amount, target, old_value, new_value):
        raise NotImplementedError

    def opening_words(self):
        pass

    def closing_words(self):
        pass

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

    def predicate(self):
        return True

    def targets(self, combo):
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
        return _targets

    def single_effect(self, target):
        dmg = self.physical_damage(self.caster, target, 1)
        _oldt = target.hp
        target.hp -= dmg

        mp_received = 0.3 * dmg
        target.mp += mp_received if mp_received < 60 else 60
        self.caster.mp += mp_received if mp_received < 30 else 30
        return (dmg, _oldt, target.hp)

    def log_skill(self, amount, target, old_value, new_value):
        # coloring
        if self.caster in self.world.yourteam:
            color = utils.color_green
        else:
            color = utils.color_red

        description_low = [
            "punches", "kicks", "throws a pebble at"
        ]
        description_mid = [
            "lands a blow on", "hits", "swings at"
        ]
        description_high = [
            "lands a powerful blow on", "injures", "maims"
        ]

        _ratio = amount / old_value
        if _ratio < 0.1:
            description = description_low
        elif 0.1 <= _ratio < 0.25:
            description = description_mid
        else:
            description = description_high

        utils.slow_type("%s: %s %s dealing %s dmg. (%d -> %d)\n" % (
            utils.bold(color(self.caster.name)),
            random.choice(description),
            target.name, utils.bold(str(amount)),
            old_value, new_value))


class WellIntentionedWish(Ability):
    mp_cost = 70

    def targets(self, combo):
        _targets = []
        for unit in combo:
            if unit in self.world.yourteam and 0 < unit.hp_ratio < 100:
                _targets.append(unit)
        if not _targets:
            for unit in self.world.yourteam:
                if unit.hp_ratio < 100:
                    _targets.append(unit)
        if not _targets:
            _targets.append(self.caster)

        return [min(_targets, key=lambda x: x.hp_ratio)]

    def single_effect(self, target):
        dmg = self.healing_damage(self.caster, 3)
        _oldt = target.hp
        target.hp += dmg
        return (dmg, _oldt, target.hp)

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type("%s: [%s] on %s for %s HP. (%d -> %d)\n" % (
            utils.bold(utils.color_green(self.caster.name)),
            utils.color_yellow(str(self)),
            target.name, utils.bold(str(amount)), old_value, new_value))


class ThousandFists(Ability):
    mp_cost = 120

    def targets(self, combo):
        _targets = (h for h in self.world.enemyteam if h.hp)
        sorted_hp_def = min(_targets,
                            key=lambda x: x.hp_ratio / (5 * x.DEF))
        return [sorted_hp_def]

    def single_effect(self, target):
        dmg = self.physical_damage(self.caster, target, 3)
        _oldt = target.hp
        target.hp -= dmg
        return (dmg, _oldt, target.hp)

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type(
            "%s: [%s] on %s dealing %s dmg"
            ". (%d -> %d)\n" % (
                utils.bold(utils.color_green(self.caster.name)),
                utils.color_yellow(str(self)),
                target.name, utils.bold(str(amount)),
                old_value, new_value))


class SilentPrayer(Ability):
    mp_cost = 70

    def targets(self, combo):
        _targets = []
        for hero in self.world.yourteam:
            if hero.hp and hero in combo and hero.mp_ratio < 100:
                _targets.append(hero)
        if not _targets:
            _targets.append(self.caster)
        return [min(_targets, key=lambda x: x.mp_ratio)]

    def single_effect(self, target):
        _oldt = target.mp
        target.mp += target.maxMP
        return (target.mp - _oldt, _oldt, target.mp)

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type(
            "%s: [%s] on %s restoring full MP.\n" % (
                utils.bold(utils.color_green(self.caster.name)),
                utils.color_yellow(str(self)), target.name))


class NovaBlast(Ability):
    mp_cost = 120

    def opening_words(self):
        print(r"""
  /$$$$$$  /$$   /$$ /$$$$$$$  /$$$$$$$$ /$$$$$$$  /$$   /$$  /$$$$$$  /$$    /$$  /$$$$$$
 /$$__  $$| $$  | $$| $$__  $$| $$_____/| $$__  $$| $$$ | $$ /$$__  $$| $$   | $$ /$$__  $$
| $$  \__/| $$  | $$| $$  \ $$| $$      | $$  \ $$| $$$$| $$| $$  \ $$| $$   | $$| $$  \ $$
|  $$$$$$ | $$  | $$| $$$$$$$/| $$$$$   | $$$$$$$/| $$ $$ $$| $$  | $$|  $$ / $$/| $$$$$$$$
 \____  $$| $$  | $$| $$____/ | $$__/   | $$__  $$| $$  $$$$| $$  | $$ \  $$ $$/ | $$__  $$
 /$$  \ $$| $$  | $$| $$      | $$      | $$  \ $$| $$\  $$$| $$  | $$  \  $$$/  | $$  | $$
|  $$$$$$/|  $$$$$$/| $$      | $$$$$$$$| $$  | $$| $$ \  $$|  $$$$$$/   \  $/   | $$  | $$
 \______/  \______/ |__/      |________/|__/  |__/|__/  \__/ \______/     \_/    |__/  |__/
""")  # noqa: E501

    def targets(self, combo):
        return self.world.enemyteam

    def single_effect(self, target):
        dmg = self.magical_damage(self.caster, target, 3.5)
        _oldt = target.hp
        target.hp -= dmg
        return (dmg, _oldt, target.hp)

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type(
            "%s: [%s] on %s dealing %s dmg. (%d -> %d)\n" % (
                utils.bold(utils.color_green(self.caster.name)),
                utils.color_yellow(str(self)),
                target.name, utils.bold(str(amount)),
                old_value, target.hp))


class Focus(Ability):
    mp_cost = 60

    def targets(self, combo):
        return [self.caster]

    def single_effect(self, target):
        target.MAG *= 1.5
        target.SPD *= 1.5
        return ('', '', '')

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type("%s: [%s] on self increasing MAG/SPD.\n" % (
            utils.bold(utils.color_green(self.caster.name)),
            utils.color_yellow(str(self))))


class BurstingQi(Ability):
    mp_cost = 80

    def targets(self, combo):
        return [self.caster]

    def single_effect(self, target):
        target.ATK *= 1.2
        target.DEF *= 1.2
        return ('', '', '')

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type(
            "%s: [%s] on self increase ATK and DEF.\n" % (
                utils.bold(utils.color_green(self.caster.name)),
                utils.color_yellow(str(self))))


class CuriousBox(Ability):
    mp_cost = (random.random() + 0.5) * 100

    def targets(self, combo):
        _targets = []
        while True:
            _enemies = [m for m in self.world.enemyteam if m.hp]
            _targets.append(random.choice(_enemies))
            if any((m.hp for m in self.world.enemyteam)):
                if random.random() > 0.6:
                    break
        return _targets

    def single_effect(self, target):
        _mult = int((random.random() * random.random() * 3) + 1.3)
        dmg = self.hybrid_damage(self.caster, target, _mult)
        _oldt = target.hp
        target.hp -= dmg
        return (dmg, _oldt, target.hp)

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type(
            "%s: [%s] on %s dealing %s dmg. (%d -> %d)\n" % (
                utils.bold(utils.color_green(self.caster.name)),
                utils.color_yellow(str(self)),
                target.name, utils.bold(str(amount)),
                old_value, new_value))


class BootyTrap(Ability):
    mp_cost = 100

    def targets(self, combo):
        return [max(self.world.enemyteam, key=lambda x: x.DEF)]

    def single_effect(self, target):
        dmg = self.hybrid_damage(self.caster, target, 1.5)
        _oldt = target.hp
        target.hp -= dmg
        target.DEF *= 0.7
        target.SPR *= 0.7
        return (dmg, _oldt, target.hp)

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type(
            "%s: [%s] on %s dealing %s dmg. (%d -> %d)\n" % (
                utils.bold(utils.color_green(self.caster.name)),
                utils.color_yellow(str(self)),
                target.name, utils.bold(str(amount)),
                old_value, target.hp))
        utils.slow_type(
            "%s: [%s] on %s decreases DEF/SPR.\n" % (
                utils.bold(utils.color_green(self.caster.name)),
                utils.color_yellow(str(self)), target.name))


class ChivalrousProtection(Ability):
    mp_cost = 100

    def targets(self, combo):
        return self.world.yourteam

    def single_effect(self, target):
        target.DEF *= 1.8
        target.SPR *= 1.8
        return ('', '', '')

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type(
            "%s: [%s] on %s increases DEF/SPR.\n" % (
                utils.bold(utils.color_green(self.caster.name)),
                utils.color_yellow(str(self)), target.name))


class RighteousInspiration(Ability):
    mp_cost = 100

    def targets(self, combo):
        return [h for h in self.world.yourteam if (h.mp * h.hp)]

    def single_effect(self, target):
        target.mp *= 3
        return ('', '', '')

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type(
            "%s: [%s] on %s restoring MP.\n" % (
                utils.bold(utils.color_green(self.caster.name)),
                utils.color_yellow(str(self)), target.name))


class BubblyPickMeUp(Ability):
    def predicate(self):
        return any((mob.hp_ratio < 60 for mob in self.world.enemyteam))

    def targets(self, combo):
        return [m for m in self.world.enemyteam if m.hp]

    def single_effect(self, target):
        dmg = self.healing_damage(self.caster, 1.8)
        _oldt = target.hp
        target.hp += dmg
        return (dmg, _oldt, target.hp)

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type(
            "%s: [%s] on %s healing for %s. (%d -> %d)\n" % (
                utils.bold(utils.color_red(self.caster.name)),
                utils.color_yellow(str(self)),
                target.name, utils.bold(str(amount)), old_value, new_value))


class TemporaryInsanity(Ability):
    def predicate(self):
        return True

    def targets(self, combo):
        return self.world.enemyteam

    def single_effect(self, target):
        target.ATK *= 1.35
        return ('', '', '')

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type("%s: [%s] on %s increases ATK.\n" % (
            utils.bold(utils.color_red(self.caster.name)),
            utils.color_yellow(str(self)), target.name))


class AngryOwner(Ability):

    def predicate(self):
        if len(self.world.enemyteam) == 1:
            return True

    def opening_words(self):
        utils.slow_type("The Owner's here, and he's not happy!!!\n")

    def closing_words(self):
        self.caster.ATK *= 1.35
        utils.slow_type(
            "%s: [%s] on himself increasing ATK.\n" % (
                utils.bold(utils.color_red(self.caster.name)),
                utils.color_yellow(str(self))))

    def targets(self, combo):
        return (h for h in self.world.yourteam if h.hp)

    def single_effect(self, target):
        dmg = self.hybrid_damage(self.caster, target, 3.5)
        _oldt = target.hp
        target.hp -= dmg
        return (dmg, _oldt, target.hp)

    def log_skill(self, amount, target, old_value, new_value):
        utils.slow_type(
            "%s: [%s] on %s dealing %s dmg. (%d -> %d)\n" % (
                utils.bold(utils.color_red(self.caster.name)),
                utils.color_yellow(str(self)),
                target.name, utils.bold(str(amount)),
                old_value, new_value))
