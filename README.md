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
1 wizard, 373/400, 46/100, ATTACK
2 cleric, 379/450, 100/120, Heal
3 monk, 420/650, 120/120, BurstingQi
4 ninja, 850/850, 74/100, ATTACK
5 knight, 1100/1100, 80/80, Righteous Inspiration
```

Here we can see one line per party member, in the following format:

```
[combo-number] [name], [HP]/[maxHP], [MP]/[maxMP], [choice]
```

In other words, this turn, the `wizard` has:

* 373HP, 400maxHP
* 46MP, 100maxMP
* Declared ATTACK as a choice

The beginning of turn screen will also display the current state of
the enemy party:

```

HellHoundA 156/750
HellHoundB 714/750
BeastMaster 1500/1500
```

The game will then ask you to input a combo:

```
Pick your combo>
```

A **combo** is a group of 1, 2 or 3 heroes that will take action this
turn. The action they take consist of the **choice** they announced at
the beginning of the turn.

You select the heroes by giving their number. In the example above, if
you want to combo wizard/ATTACK + monk/BurstingQi +
knight/RighteousIndignation, you would input `135`. (the order doesn't
matter, it could've well been `513`, wouldn't make a difference.)

Once the combo is selected, the **turn resolution**, each unit in your
combo, as well each mob in the enemy party, will be added to the
**turn order** list. This list will then be sorted
semi-randomly. Units with high SPD usually go first, however some
units can be stubborn and it's usually not posisble to predict exactly
the order of resolution.

Then going through the **turn order** list, every unit will execute
their action. When taking its action, the unit **picks a target for
itself**. You as a player have no say in who should be targeted.

However, there is _some_ order to this madness, as units are (usually)
consistent with their targetting decisions. The more you play with
them, the more you'll learn to anticipate which enemies will be
targeted by the ability.

As units execute their turns, the game will display what's being
modified. Like this:

```
monk: THOUSAND FISTS HellHoundB for 768 damage. (714 -> 0)
HellHoundA: ATTACK monk for 115 damage. (535 -> 420)
BeastMaster: NIGHT CALL heals HellHoundA for 150. (156 -> 306)
BeastMaster: NIGHT CALL heals BeastMaster for 150. (1500 -> 1500)
joker: ATTACK HellHoundA for 196 damage. (306 -> 110)
knight: RIGHTEOUS INSPIRATION restored MP of wizard
knight: RIGHTEOUS INSPIRATION restored MP of cleric
knight: RIGHTEOUS INSPIRATION restored MP of monk
knight: RIGHTEOUS INSPIRATION restored MP of joker
knight: RIGHTEOUS INSPIRATION restored MP of knight
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


Hero Stats
----------

Every unit has the following stats:

* maxHP: Hit Points indicate how healthy a hero is. Once it reaches
  zero, the unit dies.
* maxMP: Mana Points indicate the resources needed to cast an
  ability. When MP raches maxMP, the unit stops attacking and starts
  casting abilities.
* ATK: determines the physical damage of ATTACKs and other physical
  abilities.
* DEF: determines the physical damage reduction received from physical abilities.
* MAG: determines the magical damage of some abilities.
* SPR: (spirit) determines the magical damage reduction received from magical
  abilities.
* SPD: Determines the chance of a unit to act early in the turn.


Heroes
------

Here are the current heroes available:

* wizard: Fragile but very powerful, the wizard is a typical glass
  cannon. His defensive stats are horrible, but the damage potential
  from his abilities is very high.
* wizard ability #1, **Nova Blast**: A big explosion that deals
  massive magic damage to all enemies.
* wizard ability #2, **Focus**: Increases own MAG.

* cleric: The white mage of the party, the cleric's role is to provide
  sustain to your party.
* cleric ability #1 **Heal**, as its name suggests, restore HP to an
  ally.
* cleric ability #2 **Silent Prayer** fill the MP gauge of an ally.

* monk: The brawler of the group, he excells at providing sustainable
  physical damage.
* monk ability #1, **Thousand Fists**: deal massive physical damage to
  a single target.
* monk ability #2, **BurningQi**: increases own ATK.

* ninja: A wildcard with solid defensive stats and unpredictable behavior.
* ninja ability #1, **Curious Box**: Deal a random amount of damage to
  a random amount of enemies.
* ninja ability #2, **Booty Trap**: Deals a small amount of damage to
  an enemy as well as reducing their DEF and SPR.

* knight, A tanky support, who makes the rest of his team stronger.
* knight ability #1, **Chivalrous Protection** increases the DEF and
  SPR of the whole party
* knight ability #2, **Righteous Inspiration** restores some MP to the
  whole party.


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
