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


def color(message, c):
    colors = {
        'black': "\u001b[30m",
        'red': "\u001b[31m",
        'green': "\u001b[32m",
        'yellow': "\u001b[33m",
        'blue': "\u001b[34m",
        'magenta': "\u001b[35m",
        'cyan': "\u001b[36m",
        'white': "\u001b[37m",
        'bold': "\u001b[1m",
        'reset': "\u001b[0m",
    }
    if c in colors:
        return colors[c] + message + colors['reset']
    return message


def slow_type(t):
    """Simluates a human typing effect.

     taken from https://stackoverflow.com/q/4099422/403401

    """
    typing_speed = 150
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
