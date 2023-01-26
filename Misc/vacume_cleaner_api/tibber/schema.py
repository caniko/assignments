import logging
import time
from copy import copy
from itertools import combinations, permutations
from typing import Literal

from pydantic import BaseModel, validator
from shapely.geometry import LineString

from tibber import EXAMPLE_REQUEST_TOWARDS_TEST_ENDPOINT

ROOM_HALF_LENGTH = 100000

NANO = 10**9
RANGE_LIMIT = 10**5


logger = logging.getLogger(__file__)
DIRECTION_TO_OPPOSITE_DIRECTION = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
}


class RobotStart(BaseModel):
    x: int
    y: int

    @validator("x")
    def x_range(cls, value: int) -> int:
        if not -RANGE_LIMIT <= value <= RANGE_LIMIT:
            raise ValueError(f"x must be -{RANGE_LIMIT} <= x <= {RANGE_LIMIT}")
        return value

    @validator("y")
    def y_range(cls, value: int) -> int:
        if not -RANGE_LIMIT <= value <= RANGE_LIMIT:
            raise ValueError(f"y must be -{RANGE_LIMIT} <= y <= {RANGE_LIMIT}")
        return value


class RobotCommand(BaseModel):
    direction: Literal["north", "south", "west", "east"]
    steps: int

    @validator("steps")
    def steps_range(cls, value: int) -> int:
        if not 0 < value < RANGE_LIMIT:
            raise ValueError(f"steps must be 0 < steps < {RANGE_LIMIT}")
        return value


class RobotMove(BaseModel):
    start: RobotStart
    commands: list[RobotCommand, ...]

    class Config:
        schema_extra = {"example": EXAMPLE_REQUEST_TOWARDS_TEST_ENDPOINT}

    @validator("commands")
    def less_than_max_commands(cls, value) -> list[RobotCommand, ...]:
        if (length := len(value)) > 10000:
            raise ValueError(f"Maximum number of commands, 10 000, exceeded: {length}")
        return value

    @property
    def n_commands(self) -> int:
        n_commands: int = len(self.commands)
        if n_commands > 10000:
            raise AttributeError(
                f"Maximum number of commands, 10 000, exceeded: {n_commands}"
            )
        return n_commands

    @property
    def visited_pure_python(self) -> set[tuple[int, ...]]:
        """
        Convert direction and steps into a scalar that will be subtracted from the
        position vector. The arithmetic operation depends on the direction:

            north: Add steps to y, or component 1 on the vector
            south: Subtract steps from y, or component 1 on the vector
            west: Subtract steps from x, or component 0 on the vector
            east: Add steps to x, or component 0 on the vector

        The locations are stored in a set meaning we can add the same location many
        times without worrying about pre-existing duplicates.
        """

        location: list[int, int] = [self.start.x, self.start.y]
        logger.debug(f"Starting robot cleaning from location {location}")

        visited: set[tuple[int, ...]] = {tuple(location)}

        for command in self.commands:
            for _ in range(1, command.steps + 1):
                match command.direction:
                    case "north":
                        location[1] += 1
                    case "south":
                        location[1] -= 1
                    case "west":
                        location[0] -= 1
                    case "east":
                        location[0] += 1

                visited.add(tuple(location))

                logger.debug(f"Robot: Moving to {location} for cleaning")

        logger.debug("Robot: Finalized cleaning, what is my purpose?")

        return visited

    @property
    def visited(self):
        location: list[int, int] = [self.start.x, self.start.y]

        visits = 1
        line_strings_for_cross: list[LineString, ...] = []
        line_strings_for_overlap: list[LineString, ...] = []
        for command in self.commands:
            next_location = copy(location)
            line_start = copy(location)
            line_end = copy(location)
            match command.direction:
                case "north":
                    next_location[1] += command.steps
                    line_end[1] += command.steps - 1
                    line_start[1] += 1
                case "south":
                    next_location[1] -= command.steps
                    line_end[1] = line_end[1] - command.steps + 1
                    line_start[1] -= 1
                case "west":
                    next_location[0] -= command.steps
                    line_end[0] = line_end[0] + command.steps + 1
                    line_start[0] -= 1
                case "east":
                    next_location[0] += command.steps
                    line_end[0] += command.steps - 1
                    line_start[0] += 1

            line_strings_for_cross.append(LineString((location, next_location)))
            line_strings_for_overlap.append(LineString((line_start, line_end)))
            location = next_location

            visits += command.steps

        for line_a, line_b in combinations(line_strings_for_cross, 2):
            # We need to remove the extra visits from the crosses
            if line_a.crosses(line_b):
                visits -= 1

        for line_a, line_b in combinations(line_strings_for_overlap, 2):
            if line_a.covers(line_b):
                if line_a.length == line_b.length:
                    visits = visits - line_a.length - 2
                else:
                    visits -= abs(line_a.length - line_b.length)

        return visits

    def info(self) -> dict[str, int | float]:
        """
        The method returns a subset of desired data from the assignment spec:
            - command: Number of commands
            - result: Number of locations visited (not just start and stop, but also points between)
            - duration: Compute time of the before-mentioned values in seconds
        """
        start_time: float = time.time_ns()

        n_visited: int = self.visited

        duration: float = (time.time_ns() - start_time) / NANO

        return {"commands": self.n_commands, "result": n_visited, "duration": duration}
