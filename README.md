Dungeon Crawler
===============

A text-based dungeon crawling game, in which you bring a party of
heroes through a series of fights. Unlike traditional games of the
genre, in this game your heroes are an opinionated bunch and will make
some of decisions for themselves.

The game is at a very early stage of development and as of this
prototype, there's only a single fight to be had.

Rules
=====

Main Battle Loop
----------------

1. In DungeonCrawler, you start with a party of 5 heroes facing an
   enemy party of 3 mobs.
2. A battle is a succession of turns in which units can take actions
   that affect the battle state (do damage, restore HP, modify stats,
   restore MP, ...)
3. A party loses when all of its member have their HP reduced
   to 0. The battle keeps going until one party loses.

Flow of a turn
--------------

At the beginning of the turn your party announces what they chose to
do this turn, and displays it like this:

```
------------------------------------------------------------------------------------------
# NAME                     HIT POINTS             MANA POINTS          CHOICE

1 wizard           297/700 ▰▰▰▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱ - ▰▰▰▰▰▰▰▱▱▱ 84/120    ATTACK
2 cleric           750/750 ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ - ▰▰▰▰▰▰▰▰▰▰ 70/70     Wishful Intention
3 monk             542/650 ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▱▱▱▱ - ▰▰▰▰▰▱▱▱▱▱ 60/120    ATTACK
4 ninja            416/850 ▰▰▰▰▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱ - ▰▰▰▰▰▰▰▰▰▰ 100/100   Booty Trap
5 knight         1100/1100 ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰ - ▰▰▰▰▰▰▰▰▰▰ 100/100   Righteous Inspiration
```

Here we can see one line per party member, in the following format:

```
[combo-number] [name], [HP]/[maxHP], [MP]/[maxMP], [choice]
```

In other words, this turn, the `wizard` has:

* 297 HP, 700 maxHP
* 84 MP, 120 maxMP
* Declared ATTACK as a choice

The beginning of turn screen will also display the current state of
the enemy party:

```
Charging Drunk A   269/900 ▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
Charging Drunk B   136/900 ▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
Crazed Bartender 1713/2000 ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▱▱▱
```

Notice how the enemies don't announce their choices.

The game will then ask you to input a combo:

```
[5] Pick your combo>
```

A **combo** is a group of 1, 2 or 3 heroes that will take action this
turn. The action they take consist of the **choice** they announced at
the beginning of the turn.

You select the heroes by giving their number. In the example above,
the combo `345` will pick:

* monk/ATTACK
* ninja/Booty Trap
* knight/Righteous Inspiration

Note that the order won't matter, so `345` and `435` are equivalent.

Once the combo is selected, the **turn resolution** starts. Each unit
in your combo, as well each mob in the enemy party, will be added to
the **turn order** list. This list will then be sorted
semi-randomly. Units with high SPD usually go first, however some
units can be stubborn and it's usually not posisble to predict exactly
the order of resolution.

Then, going through the **turn order** list, every unit will execute
their action. When taking its action, the unit **picks a target for
itself**. You as a player have no say in who should be targeted.

However, there is _some_ order to this madness, as units are (usually)
consistent with their targetting decisions. The more you play with
them, the more you'll learn to anticipate ability targets.

As units execute their turns, the game will display what's being
modified. Like this:

```
Charging Drunk A: injures wizard dealing 272 dmg. (297 -> 25)
Charging Drunk B: injures wizard dealing 272 dmg. (25 -> 0)
ninja: [Booty Trap] on Charging Drunk A dealing 173 dmg. (269 -> 96)
ninja: [Booty Trap] on Charging Drunk A decreasing DEF/SPR.
cleric: [Wishful Intention] on ninja for 346 HP. (416 -> 762)
Crazed Bartender: [Bubbly Pick-me-up] on Charging Drunk A healing for 100. (96 -> 196)
Crazed Bartender: [Bubbly Pick-me-up] on Charging Drunk B healing for 100. (136 -> 236)
Crazed Bartender: [Bubbly Pick-me-up] on Crazed Bartender healing for 100. (1713 -> 1813)
```


End of turn.


Choices, Abilities and MP
-------------------------

The main factor a unit takes into account when deciding their
**choice** is their current MP. As long as their MP is below their
maxMP, heroes only declare ATTACK as an action. Once their MP is full,
they will declare one of their 2 abilities as a choice.

MP starts at 0 at the beginning of the fight and is regenerated slowly
and passively each turn, however there are ways to boost the regen:

* ATTACKing an enemy will regenerate some MP proportional to the
  damage done.

* Receiving damage will regenerate some MP proportional to the damage
  received.

* Some abilities, like the Knight's Righteous Inspiration, will
  restore MP to the party.


Heroes
------

Here are the available heroes:

| hero   | description             | ability #1                                                 | ability #2                                                     |
|--------|-------------------------|------------------------------------------------------------|----------------------------------------------------------------|
| wizard | glass cannon dps        | **Nova Blast**: AoE damage                                 | **Focus**: Buff self MAG/SPD                                   |
| cleric | healer of the party     | **Heal**: restores mp to one ally                          | **Silent Prayer**: fill mp gauge for one ally                  |
| monk   | durable dps             | **Thousand Fists**: massive single target damage           | **Burning Qi**: buff self ATK/DEF                              |
| ninja  | unpredictable trickster | **Curious Box**: deal random damage to random enemies      | **Booty Trap**: single target damage + DEF/SPR debuff          |
| knight | durable support         | **Chivalrous Protection**: buff DEF/SPR to the whole party | **Righteous Inspiration**: restores some MP to the whole party |


Quickstart
==========

There are many ways to launch Dungeon Crawler. Get the latest version
of the game from Github:

	$ git clone https://github.com/joehakimrahme/DungeonCrawler
	$ cd DungeonCrawler

The easiest way to launch the game is by using `tox`:

	$ tox -e dc

Alternatively, you'll need to install the current package and launch
the executable `dcbattle`. Here are some sample instructions to
install in a virtualenv:

	$ virtualenv .venv
	$ source .venv/bin/activate
	$ pip install .
	$ dcbattle

This should be rather fast, given that, as of now, DC doesn't use any
external dependency.
