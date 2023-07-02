# Connect four

Connect four - the game - implemented in python and dash.  
[Connect four](https://en.wikipedia.org/wiki/Connect_Four) is a simple combinatory puzzle board game.

The project features:
- dash web app to play the game, using the [Skeleton CSS framework](http://getskeleton.com/)
- class for the actual game play (moves, store the status, etc)
- class for a simple heuristic computer enemy. It calculates all possible 3 next moves and chooses the most valuable outcome

## Installation

The package requirements are found in requirements.txt (in a virtual environment):

``pip install -r requirements``

Start the web server which runs dash with:

``gunicorn dashgui:server -b :8000``

The development/debug server starts with:

``python viergewinnt.py``

## Future Features:
- Machine Learning enemy. That was the whole point of this project
