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
from dungeoncrawler import battle
from dungeoncrawler import hero
from dungeoncrawler import skills
from dungeoncrawler import utils


HEROES = []

wizard_dict = {
    'HP': 1.4,
    'ATK': 0.6,
    'DEF': 0.8,
    'MAG': 1.2,
    'SPR': 1.3,
    'SPD': 7,
}
wizard_skills = [
    skills.NovaBlast,
    skills.Focus,
]
HEROES.append(hero.Hero('wizard', wizard_dict, wizard_skills))

cleric_dict = {
    'HP': 1.5,
    'ATK': 0.5,
    'DEF': 0.8,
    'MAG': 1.1,
    'SPR': 1.5,
    'SPD': 3,
}
cleric_skills = [
    skills.WellIntentionedWish,
    skills.SilentPrayer,
]
HEROES.append(hero.Hero('cleric', cleric_dict, cleric_skills))

monk_dict = {
    'HP': 1.3,
    'ATK': 1.6,
    'DEF': 1.1,
    'MAG': 0.4,
    'SPR': 0.85,
    'SPD': 9,
}
monk_skills = [
    skills.ThousandFists,
    skills.BurstingQi,
]
HEROES.append(hero.Hero('monk', monk_dict, monk_skills))

ninja_dict = {
    'HP': 1.7,
    'ATK': 1.2,
    'DEF': 1,
    'MAG': 1.15,
    'SPR': 1.2,
    'SPD': 5,
}
ninja_skills = [
    skills.CuriousBox,
    skills.BootyTrap,
]
HEROES.append(hero.Hero('ninja', ninja_dict, ninja_skills))

knight_dict = {
    'HP': 2.2,
    'ATK': 1.4,
    'DEF': 1.5,
    'MAG': 0.8,
    'SPR': 1.4,
    'SPD': 4
}
knight_skills = [
    skills.RighteousInspiration,
    skills.ChivalrousProtection,
]
HEROES.append(hero.Hero('knight', knight_dict, knight_skills))


MOBS = []
drunk_dict = {
    'HP': 1.8,
    'ATK': 0.6,
    'DEF': 1.7,
    'MAG': 0.3,
    'SPR': 0.9,
    'SPD': 7
}
drunk_skills = []

bartender_dict = {
    'HP': 4,
    'ATK': 0.3,
    'DEF': 1.7,
    'MAG': 1,
    'SPR': 1.3,
    'SPD': 1
}
bartender_skills = [skills.AngryOwner,
                    skills.BubblyPickMeUp,
                    skills.TemporaryInsanity]

MOBS.append(hero.Mob('Charging Drunk A', drunk_dict, drunk_skills))
MOBS.append(hero.Mob('Charging Drunk B', drunk_dict, drunk_skills))
MOBS.append(hero.Mob("Crazed Bartender", bartender_dict, bartender_skills))

intro = """
You know what you have to do, you've been here before. The fate of the
world depends on you and your friends. You need to go there, you need
to stop Evil. You need to fulfill the prophecy.

But first you need a drink.

You stop at the local tavern, hoping to find good mead, instead you
find a good old fashioned brawl.

And now the drunks are charging at you...
"""
outro = """
                                                                 &
                                                               *@&
                                                             %&&@
                                         (@&&            *&&&&&,
                                    #&@@&      ,%&&&&&&&&&&&%
                                ,&&&&& *&&&&&&&&&&&&&&&#           @
                             /&@&&&&&&&&&&&&&#&&&&&@&&&&&&@&&&&@@&
                       ,#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@&@&(
                         &&&&&&&&&&&&&&&&&&&&&&&&&&&&#*.
                       @&@&&&&@#   &&&&&&&&&&&&&&&&&&&&&&&&@@&,
                 %&&&&&&&&&&&&&%&&&&&&&&&&&&&&&&&&&&&&&&@( /&&&&&
         .@@@&@&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&@@(   &&
       .&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#&&&&&&&&&&&&&&&&@#
     &%&&&&&&&&&&&&&&&@@&, &@@&&&&&&&&&&&&&&&  @&&&&&&&&&&&&&&&@
      @&&&@@&&&&&&&&*@        &&&&&&&&&&&&&&&, /&&&&&&&&&&&&&&&&@
      ,&&&*&& &,&             &&&&&&&&&&&&&&&. ,&&&&&&&&&&&&&&&&@,
       (      % %@#&&&&&&&&&&&&&&&&&&&&&&&&&%  &@&&&&&&&&&&&&(&&&%
           @@&&&&&&&&&&&&&&&&&@&&&&&&&&&&&@   &&&&&&&&&&&&&&&(*@&#
          @ &&&&@&@&*                      ,&&&&&&&&&&&&&&&&&. &@
               *&                      ,&&&&&&&&&&&&&&&&&&&@&  &/
                                    .&&&&&&&&&&&&&&&&&&&&@&@&  %
                                ,@&&&&&&&&&&&&&&&&&&&&&& &&&
                            *@&&&&&&&&&&&&&&&&&&&&&&&&  &&@
                         &@&&&&&&&&&&&&&&&&&&&&&&&&%    &*
                      #@&&&&&&&&&&&&&&&&&&&&&@@&.
                     &&&&&&&&&&&&&&&&&&&&&#
                    @&&&&&&&&&&&&&*
                   &&&&&@&@,
                   &&&&
                   &#


You won the fight. The bar fight. Very glorious. Bunch of trained
soldiers bullying drunk braggarts. You know you're not the most
popular person here.

You won, but you didn't triumph. Oh the tragedy of heroes...

"""
logo = """
                       %%%*
                     (%%%,,,,,,,,,
                     #%%%%%%%%%%%%%%%
                         %%%%&&&&&&&%%%                ###
                         ///////////(((              ########
                         ,(&,,,,,&,,,((        #################
                       ..,/,,,,,,,,,,**,.,,,##############%%%%%%,,
                       ,,/%%%%%%#/,,/%%####################%%%%%%#
                       %%%.,,,,,,%///%%%#####%%%%%%%%%%%#######%##
                     /#%&%%%%%%%%%%%%%%##%%%###########%#%%%%%%%
               ,,,* ##%&&%%%%%%%%%%%&####%., &%%%%%%%%%%####%%#
               ,,,* ##%%#&&&&&&&&&&&%##%((.,,   &%%%%%%%%%%####
                 /,,/////#(((////*(((## *////*,,.         %%%%%%
                  *****   #((//*/((((##     ***,,,*,#((    %#%%%##
                          %#(((((((((##        ,,,((/
                       ##%%#%%%%%%%#####%       (/  /..,
                     /#%%%%%%%%%%%%%%%%%%#           **.*,
                    %%%%%              %%%%%            **..,
                 .#%%%%                 %%%&%,            ***

"""

mobs = MOBS
heroes = HEROES


def main():
    a = battle.Battle(heroes, mobs, intro, outro, logo)
    print(r"""
  888888                  d8b
    "88b                  88P
     888                  8P
     888  .d88b.   .d88b. "  .d8888b
     888 d88""88b d8P  Y8b   88K
     888 888  888 88888888   "Y8888b.
     88P Y88..88P Y8b.            X88
     888  "Y88P"   "Y8888     88888P'
   .d88P
 .d88P"

%s

       8888888b.
       888  "Y88b
       888    888
       888    888 888  888 88888b.   .d88b.   .d88b.   .d88b.  88888b.
       888    888 888  888 888 "88b d88P"88b d8P  Y8b d88""88b 888 "88b
       888    888 888  888 888  888 888  888 88888888 888  888 888  888
       888  .d88P Y88b 888 888  888 Y88b 888 Y8b.     Y88..88P 888  888
       8888888P"   "Y88888 888  888  "Y88888  "Y8888   "Y88P"  888  888
                                         888
                                    Y8b d88P
                                     "Y88P"

              .d8888b.                                888
             d88P  Y88b                               888
             888    888                               888
             888        888d888 8888b.  888  888  888 888  .d88b.  888d888
             888        888P"      "88b 888  888  888 888 d8P  Y8b 888P"
             888    888 888    .d888888 888  888  888 888 88888888 888
             Y88b  d88P 888    888  888 Y88b 888 d88P 888 Y8b.     888
              "Y8888P"  888    "Y888888  "Y8888888P"  888  "Y8888  888
""" % a.logo)
    utils.slow_type(a.intro)
    a.battle_loop()
