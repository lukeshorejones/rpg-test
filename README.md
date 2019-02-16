# RPG Test
A tactical RPG made with Python and Pygame, based on games like Fire Emblem. The player controls a group of units on a variety of maps, the goal being to defeat all of the enemy units. You can play singleplayer against an AI opponent, or multiplayer against a friend. The game also supports custom units, weapons and maps without any coding knowledge required.

# User Guide
Run main.pyw to play the game. You will need to install some external modules, which are listed in the Dependencies section.

You can then edit the files in the content folder to change some configuration options and add your own custom content such as characters, weapons and maps.

# Dependencies
You'll need Python 3, and the below modules. Add Python to PATH, then in command prompt type `pip install X`, once each for all of:
 - numpy
 - pygame
 - pytmx
 - ruamel.yaml

# v2.2 Changelog
 - Replaced volume in settings.yml with master volume, music and SFX.
 - Moved settings.yml out of the content folder.
 - Added an options menu to the pause menu and title screen.

# What Did I Learn?
 - How games work!
 - Principles of object-oriented programming.
 - Reading and writing to YAML files in Python.
 - Designing algorithms, such as a recursive algorithm to determine the tiles a unit can move to.
 - Writing a convincing enemy AI which makes reasonable decisions.
 - Writing menu items, including sliders with non-linear volume scaling.

# Credits
 - Default unit images, tile images and click sound by Kenney (https://www.kenney.nl/)
 - Default stat and weapon icons - some have been edited - by Kyrise (https://kyrise.itch.io)
 - Default footsteps by HaelDB (https://opengameart.org/users/haeldb)
 - Default attack and healing sounds by Sound Effect Lab (http://en.soundeffect-lab.info/)
 - Default music by David Vitas (http://www.davidvitas.com)
