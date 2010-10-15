Introduction
============

Gomill is a suite of tools, and a Python library, for use in developing and
testing Go-playing programs. It is based around the Go Text Protocol
(:term:`GTP`) and the Smart Game Format (:term:`SGF`).

.. todo: refs for GTP and SGF.

The principal tool is the :dfn:`ringmaster`, which plays programs against each
other and keeps track of the results.

Ringmaster features include:

- testing multiple pairings in one run
- playing multiple games in parallel
- displaying live results
- engine configuration by command line options or |gtp| commands
- a protocol for per-move engine diagnostics in |sgf| output
- automatically tuning player parameters based on game results
  (**experimental**)

.. contents:: Contents
   :local:
   :backlinks: none


Ringmaster example
------------------

.. todo:: brief link to install docs at this point

Create a file called :file:`demo.ctl`, with the following contents::

  competition_type = 'playoff'

  board_size = 9
  komi = 7.5

  players = {
      'gnugo-l1' : Player('gnugo --mode=gtp --level=1'),
      'gnugo-l2' : Player('gnugo --mode=gtp --level=2'),
      }

  matchups = [
      Matchup('gnugo-l1', 'gnugo-l2',
              alternating=True,
              number_of_games=5),
      ]

(If you don't have :program:`gnugo` installed, change the Players to use a
command line for whatever |gtp| engine you have available.)

Then run ::

  $ ringmaster demo.ctl

The ringmaster will run five games between the two players, showing a summary
of the results on screen, and then exit.

The final display should be something like this::

  playoff: demo

  gnugo-l1 v gnugo-l2 (5/5 games)
  board size: 9   komi: 7.5
             wins              black        white      avg cpu
  gnugo-l1      2 40.00%       1 33.33%     1 50.00%      1.23
  gnugo-l2      3 60.00%       1 50.00%     2 66.67%      1.39
                               2 40.00%     3 60.00%

  player gnugo-l1: GNU Go:3.8
  player gnugo-l2: GNU Go:3.8

The ringmaster will create several files named like :file:`demo.{xxx}` in the
same directory as :file:`demo.ctl`, including a :file:`demo.sgf` directory
containing game records.


Other tools
-----------

.. todo:: refer to the page about them, brief summary here.


The Python library
------------------

.. todo:: say the API isn't stable as of Gomill |version|, refer to page about
          it.