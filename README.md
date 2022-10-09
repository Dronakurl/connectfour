# connectfour
Connect four - the game - implemented in python and dash 

The game should work to play in a browser.
Right now, it's only the interface to the game.

## Future Features:
- Class for the actual gameplay
- Save and load games
- Simple heuristic computer enemy
- Machine Learning enemy
- pysimplegui GUI, since dash is slow: https://www.pysimplegui.org/en/latest/
- refactor dash callbacks to one callback per chip, perhaps thats faster

## Installation
Using the ``environment.yml``-File (edit the environment name first to make sure you don't overwrite your own environment)

``conda env create``

Start the development server with

``python viergewinnt.py``


