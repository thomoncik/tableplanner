import argparse
import logging
import sys

import genetic
import genetic.crossovers
import genetic.mutations
import genetic.selections
import numpy as np
import pandas as pd

from tableplanner import __version__

__author__ = "Tomasz Homoncik"
__copyright__ = "Tomasz Homoncik"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def optimize_guest_seating(guestsCsvFile, seatsCsvFile):
    """Optimize guest seating trying to maximize sum of their preferences

    Args:
        guestsCsvFile (file): csv containig matrix of guest preferences
                              (the bigger the number the more they want to sit near)
        seatsCsvFile (file): csv containing matrix representing layout of tables

    Returns:
        list((int, string)): list of pairs (seat_id, guest_name)
    """
    guests = pd.read_table(guestsCsvFile, sep=",", index_col=0)
    guest_names = guests.columns.values
    seats = pd.read_table(seatsCsvFile, sep=",", index_col=0, dtype=int)

    first_generation = [
        np.random.permutation(range(len(guest_names))) for _ in range(10)
    ]

    def fitness_score(chromosome):
        score = 0
        for i, x in enumerate(chromosome):
            for j, y in enumerate(chromosome):
                score += guests[guest_names[x]][guest_names[y]] * seats[str(i)][j]
        return score

    seating, score = genetic.optimize(
        first_generation,
        genetic.selections.elite_selection,
        genetic.crossovers.order_crossover,
        genetic.mutations.swap_mutation,
        fitness_score,
        100,
        0.3,
    )

    _logger.info("Resulting score: %s", score)
    return [(i, guest_names[seating[i]]) for i in range(len(seating))]


# ---- CLI ----


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Create a table seat planner")
    parser.add_argument(
        "--version",
        action="version",
        version="tableplanner {ver}".format(ver=__version__),
    )
    parser.add_argument(
        dest="guests",
        help="file with guests and relationships description",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        dest="layout", help="file with layout description", type=argparse.FileType("r")
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """
    Wrapper allowing :func:`optimize_guest_seating`
    to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`optimize_guest_seating`
    it prints the result to the ``stdout`` in a nicely formated message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "data/guests.csv", "data/seats.csv"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")

    guest_seating = optimize_guest_seating(args.guests, args.layout)
    print("The result is {}".format(guest_seating))

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
