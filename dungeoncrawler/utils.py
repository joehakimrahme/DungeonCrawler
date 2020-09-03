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
import sys
import time

from dungeoncrawler import hero


def slow_type(t):
    """Simluates a human typing effect.

     taken from https://stackoverflow.com/q/4099422/403401

    """
    typing_speed = 130
    for letter in t:
        sys.stdout.write(letter)
        sys.stdout.flush()
        if t == " ":
            interval = 50
        else:
            interval = 10
        time.sleep(random.random() * interval / typing_speed)


def create_neutral_fighter(name="test-Fighter"):
    return hero.Fighter(
        name=name,
        attributes={
            'HP': 100,
            'ATK': 30,
            'DEF': 30,
            'MAG': 30,
            'SPR': 30,
            'SPD': 30
        },
        skills=())


def create_neutral_hero(name="test-Hero", skills=None):
    if skills is None:
        skills = ()
    return hero.Hero(
        name=name,
        attributes={
            'HP': 1,
            'ATK': 1,
            'DEF': 1,
            'MAG': 1,
            'SPR': 1,
            'SPD': 1
        },
        skills=skills)


def create_neutral_mob():
    return hero.Mob(
        name="test-Mob",
        attributes={
            'HP': 1,
            'ATK': 1,
            'DEF': 1,
            'MAG': 1,
            'SPR': 1,
            'SPD': 1
        },
        skills=())
