"""main.py - Main python script to start the client."""

# ---------------------------------------------------------------------------------------------------------------------

import argparse
import sys
from logging import Formatter, StreamHandler, getLogger
from sys import argv

from interfaces.iclient_factory import IClientFactory

# ---------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # init logger.
    consoleHandler = StreamHandler(sys.stdout)
    consoleHandler.setFormatter(Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"))
    rootlogger = getLogger()
    rootlogger.addHandler(consoleHandler)
    # parse arguments.
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="client",
        description="Das Skript startet den angegebenen IClient Handler und fuehrt ihn aus.",
        epilog="Frag den Vortragenden...",
    )
    parser.add_argument(
        "--module-path",
        nargs=1,
        help='Das Pythonmodul in dem die zu verwendende Klasse gesucht werden soll, z.B.: "interfaces.default_client".',
    )
    parser.add_argument(
        "--class-name",
        nargs=1,
        help='Der Name der zu verwendenden Klasse in dem angegebenen Pythonmodul, z.B.: "DefaultClient".',
    )
    parser.add_argument(
        "--log-level",
        nargs=1,
        default="INFO",
        help="Moeglich sind: INFO, WARNING, ERROR, DEBUG, CRITICAL, NOTSET. Default ist: INFO.",
    )
    args = parser.parse_known_args(argv[1 : len(argv)])
    known_args = args[0]
    unknown_args = args[1]
    # reassign loglevel according to arguments.
    rootlogger.setLevel(known_args.log_level if isinstance(known_args.log_level, str) else known_args.log_level[0])
    # start client.
    exit(IClientFactory(rootlogger).create(known_args.module_path[0], known_args.class_name[0]).run(unknown_args))
exit(-1)
# ---------------------------------------------------------------------------------------------------------------------
