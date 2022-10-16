# Connect four

Connect four - the game - implemented in python and dash.  
[Connect four](https://en.wikipedia.org/wiki/Connect_Four) is a simple combinatory puzzle board game.

The project features:
- dash web app to play the game, using the [Skeleton CSS framework](http://getskeleton.com/)
- class for the actual game play (moves, store the status, etc)
- class for a simple heuristic computer enemy. It calculates all possible 3 next moves and chooses the most valuable outcome

## Limitation
The dash GUI doesn't store the data in the browser session. I couldn'g get dash.store to work, because my objects don't serialize to json easily. so: Single-user only

## Installation
Using the [``environment.yml``](https://github.com/Dronakurl/connectfour/blob/main/environment.yml)-file (edit the environment name first to make sure you don't overwrite your own environment)

``conda env create``

Alternatively, you can install the packages listed in ``environment.yml``, using pip.

Start the web server which runs dash with:

``gunicorn dashgui:server -b :8000``

The development/debug server starts with:

``python viergewinnt.py``

## Future Features:
- Save and load games
- Machine Learning enemy
- pysimplegui GUI, since dash is slow: https://www.pysimplegui.org/en/latest/
- Performance improvements to the dash app, it's slow
- refactor dash callbacks to one callback per chip, perhaps thats faster
