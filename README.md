# Hive

Semester project for ALP (Algorithms and Programming). Game engine for board
game [Hive](<https://en.wikipedia.org/wiki/Hive_(game)>)

There are few seemingly strange decision in the design of this, but most of them
are due to having to work around a given interface with the submission system.
For example the code is in Python 3.12, but the system only accepts five years old
3.7, so `strip.py` strips out all the incompatible features like type hints and
dataclasses.

## Structure

Main file is `player.py`, here happens all the decision logic and is the only file
submitted.

It imports from `base.py`, that is during submission provided by the system.

`runner.py` is just a simple script that runs the game locally during development.
