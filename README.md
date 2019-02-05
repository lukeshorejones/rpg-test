# RPG Test
A tactical RPG made with Python and Pygame, based on games like Fire Emblem.

# User Guide
Run the main file to play the game - pretty simple. See the Dependencies section for what you'll need to install first.

You can then edit the files in the content folder to change settings and add your own custom content such as characters, weapons and maps.

# Dependencies
You'll need Python 3, and the below modules. Add Python to PATH, then in command prompt type `pip install X`, once each for all of:
 - numpy
 - pygame
 - pytmx
 - pyyaml

# v2.0 Changelog
 - Added a changelog!
 - Made some big optimisation and coding style improvements.
 - Added a GUI in-game which displays detailed stats of hovered and selected units.
 - Tweaked window size for the new GUI.
 - Added the desert single player map, and the pole multiplayer map.
 - Added the tome, a ranged healing weapon which restores allies' health. AI enemies are capable of using this tome properly.
 - Added the pause menu! Hit Escape to pause the game, where you can choose to surrender. More options soon! (hopefully...)
 - Reworked weapons.yml to include healing values and the pool of sprites used for randomised AI units per weapon type.
 - Increased default unit health to 50, and decreased default weapon power ratings (power is renamed damage in weapons.yml).
 - Removed some boring/redundant weapons (also because I have a limited number of sprites for the new GUI).
 - When hovering over units, the tiles showing their range now also appear under their allied units in that range.
 - Improved the algorithm controlling the camera on the enemy's turn in single player. It should move around less often.
 - Maps are now stored in individual folders with their own unique tilesets, background tiles and music tracks.
 - Removed the basecontent folder and backup systems. This will be reworked.
 - Recoded title screen to work better for larger display sizes.
 - AI enemies which refuse to attack lethal targets no longer approach those targets.

# Credits
 - Default unit images, tile images and click sound by Kenney (https://www.kenney.nl/)
 - Default stat and weapon icons - some have been edited - by Kyrise (https://kyrise.itch.io)
 - Default footsteps by HaelDB (https://opengameart.org/users/haeldb)
 - Default attack and healing sounds by Sound Effect Lab (http://en.soundeffect-lab.info/)
 - Default music by David Vitas (http://www.davidvitas.com)
