"""Implementation of a default Client which can be used in any situation."""
# ---------------------------------------------------------------------------------------------------------------------
from argparse import ArgumentParser
from logging import Logger
from os import environ
from typing import Dict

from domain.server import IamProviderInfo, IServer, Location, ServerFactory
from interfaces.iclient import IClient
from typing_extensions import Self


# ---------------------------------------------------------------------------------------------------------------------
class MyClient(IClient):
    """Implementation of a default Client.

    Does not execute anything. Just returns 0 and logs its input arguments.
    """

    def __init__(self):
        super().__init__()
        pass

    def render_and_print_location(self, location: Location) -> Self:
        print(f" {location.north} ")
        print(f"{location.west}{location.current}{location.east}")
        print(f" {location.south} ")
        return self

    def run(self, args: Dict[str, str]) -> int:
        """Does nothing."""
        self.logger().info(f"Args: {args}")
        backend_url: str = environ["LABYRINTH_BACKEND_URL"]
        adventurer: str = environ["LABYRINTH_ADVENTURER"]
        iam_url: str = environ["LABYRINTH_IAM_URL"]
        username: str = environ["LABYRINTH_USERNAME"]
        password: str = environ["LABYRINTH_PASSWORD"]
        labyrinths_name: str = "simple"

        parser: ArgumentParser = ArgumentParser()
        parser.add_argument(
            "--direction",
            nargs=1,
            help="Specify the direction to move.",
        )
        known_args = parser.parse_args(args)

        server: IServer = ServerFactory(self.logger()).create(
            backend_url=backend_url,
            adventurer=adventurer,
            labyrinths_name=labyrinths_name,
            iam_info=IamProviderInfo(
                url=iam_url,
                username=username,
                password=password,
            ),
        )

        solved: bool = server.move(known_args.direction[0])
        location: Location = server.where_am_i()

        if solved:
            print("-- Solved -------------")
        else:
            print("-- Unsolved -----------")
        self.render_and_print_location(location)
        print("------------------------")
        return 0

    pass


# ---------------------------------------------------------------------------------------------------------------------
