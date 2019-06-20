# RPG Test
A tactical RPG made with Python and Pygame, based on games like Fire Emblem. The player controls a group of units on a variety of maps, the goal being to defeat all of the enemy units. You can play singleplayer against an AI opponent, or multiplayer against a friend. The game also supports the implementation of custom units, weapons and maps without any coding knowledge required.

# User Guide
This project requires Python 3 and pipenv. Once Python is installed (and added to PATH), install pipenv by running ``pip install pipenv``.

Once Python and pipenv are installed, you can navigate to the game files and run ``pipenv install`` there to automatically install all other dependencies.  

Finally, you can simply run run.bat to play the game (or run ``pipenv run python main.pyw`` directly). You can edit the files in the content folder to change some configuration options, change graphics and sounds, and add your own custom content such as new units, weapons and maps.

# v2.4 Changelog (WIP)
 - Started using a virtual environment like a real programmer.
 - Added new "ranged damage" trait type for random unit generation.
 - Added new traits (and moved some trait IDs around).
 - Changed the default trait of the default unit Rosalyn to Pierce.
 - Added new units to units.yml to showcase every trait.

# v2.4 Bugfixes (WIP):
 - Wildfire did not activate during counterattacks.

# What Did I Learn?
 - How games work!
 - Principles of object-oriented programming.
 - Reading and writing to YAML files in Python.
 - Designing algorithms, such as a recursive algorithm to determine the tiles a unit can move to.
 - Writing a convincing enemy AI which makes reasonable decisions.
 - Writing menu items, including sliders with non-linear volume scaling.

# Credits
 - Default unit images, tile images and click sound by Kenney (https://www.kenney.nl/)
 - Default stat, weapon and trait icons - some have been edited - by Kyrise (https://kyrise.itch.io)
 - Default footsteps by HaelDB (https://opengameart.org/users/haeldb)
 - Default attack and healing sounds by Sound Effect Lab (http://en.soundeffect-lab.info/)
 - Default music by David Vitas (http://www.davidvitas.com)
