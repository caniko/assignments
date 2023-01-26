import logging

import pytest
from pydantic import ValidationError

from tibber.schema import RobotCommand, RobotMove, RobotStart

N_STEPS = 10

logging.basicConfig(level=logging.DEBUG)


def test_robot_start():
    RobotStart(x=5, y=10)

    with pytest.raises(ValidationError):
        # x is too big
        RobotStart(x=10**6, y=10)

    with pytest.raises(ValidationError):
        # y is too big
        RobotStart(x=5, y=10**6)


def test_robot_command():
    for direction in ("north", "south", "west", "east"):
        RobotCommand(direction=direction, steps=N_STEPS)

    with pytest.raises(ValidationError):
        # direction has the wrong string
        RobotCommand(direction="up", steps=N_STEPS)

    with pytest.raises(ValidationError):
        # steps is too big
        RobotCommand(direction="north", steps=10**12)


def test_robot_move_validation():
    command = RobotCommand(direction="north", steps=N_STEPS)
    RobotMove(start=RobotStart(x=5, y=10), commands=[command])

    commands = [command] * 10001
    with pytest.raises(ValidationError):
        # There are too many commands, >10000
        RobotMove(start=RobotStart(x=5, y=10), commands=commands)


def test_robot_move_visited_pure_python():
    # north
    command = RobotCommand(direction="north", steps=N_STEPS)
    robot_move = RobotMove(start=RobotStart(x=5, y=10), commands=[command])
    assert robot_move.visited_pure_python == {(5, 10 + n) for n in range(N_STEPS + 1)}

    # south
    command = RobotCommand(direction="south", steps=N_STEPS)
    robot_move = RobotMove(start=RobotStart(x=5, y=10), commands=[command])
    assert robot_move.visited_pure_python == {(5, 10 - n) for n in range(N_STEPS + 1)}

    # east
    command = RobotCommand(direction="east", steps=N_STEPS)
    robot_move = RobotMove(start=RobotStart(x=5, y=10), commands=[command])
    assert robot_move.visited_pure_python == {(5 + n, 10) for n in range(N_STEPS + 1)}

    # west
    command = RobotCommand(direction="west", steps=N_STEPS)
    robot_move = RobotMove(start=RobotStart(x=5, y=10), commands=[command])
    assert robot_move.visited_pure_python == {(5 - n, 10) for n in range(N_STEPS + 1)}


def test_robot_move_visited():
    # north
    command = RobotCommand(direction="north", steps=N_STEPS)
    robot_move = RobotMove(start=RobotStart(x=5, y=10), commands=[command])
    assert robot_move.visited == N_STEPS + 1, robot_move.visited

    # south
    command = RobotCommand(direction="south", steps=N_STEPS)
    robot_move = RobotMove(start=RobotStart(x=5, y=10), commands=[command])
    assert robot_move.visited == N_STEPS + 1, robot_move.visited

    # east
    command = RobotCommand(direction="east", steps=N_STEPS)
    robot_move = RobotMove(start=RobotStart(x=5, y=10), commands=[command])
    assert robot_move.visited == N_STEPS + 1, robot_move.visited

    # west
    command = RobotCommand(direction="west", steps=N_STEPS)
    robot_move = RobotMove(start=RobotStart(x=5, y=10), commands=[command])
    assert robot_move.visited == N_STEPS + 1, robot_move.visited


def test_robot_move_visited_with_cross():
    robot_move = RobotMove(
        start=RobotStart(x=0, y=0),
        commands=[
            RobotCommand(direction="north", steps=N_STEPS),
            RobotCommand(direction="east", steps=N_STEPS),
            RobotCommand(direction="south", steps=N_STEPS - 1),
            RobotCommand(direction="west", steps=N_STEPS - 1),
            RobotCommand(direction="north", steps=N_STEPS),
            RobotCommand(direction="east", steps=N_STEPS),
        ],
    )
    assert robot_move.visited == N_STEPS * 6 - 2, robot_move.visited


def test_robot_move_visited_with_overlap():
    robot_move = RobotMove(
        start=RobotStart(x=0, y=0),
        commands=[
            RobotCommand(direction="north", steps=N_STEPS),
            RobotCommand(direction="east", steps=N_STEPS),
            RobotCommand(direction="south", steps=N_STEPS),
            RobotCommand(direction="west", steps=N_STEPS),
            RobotCommand(direction="north", steps=2 * N_STEPS),
            RobotCommand(direction="south", steps=2 * N_STEPS),
        ],
    )
    assert robot_move.visited == N_STEPS * 5 + 1, robot_move.visited


def test_robot_move_visited_with_cross_and_overlap():
    robot_move = RobotMove(
        start=RobotStart(x=0, y=0),
        commands=[
            RobotCommand(direction="north", steps=N_STEPS),
            RobotCommand(direction="east", steps=N_STEPS),
            RobotCommand(direction="south", steps=N_STEPS),
            RobotCommand(direction="west", steps=N_STEPS),
            RobotCommand(direction="north", steps=2 * N_STEPS),
            RobotCommand(direction="south", steps=2 * N_STEPS),
            RobotCommand(direction="east", steps=1),
            RobotCommand(direction="north", steps=N_STEPS + 1),
        ],
    )
    assert robot_move.visited == N_STEPS * 6 - 2, robot_move.visited


def test_robot_move_info():
    command = RobotCommand(direction="north", steps=N_STEPS)
    robot_move = RobotMove(start=RobotStart(x=5, y=10), commands=[command])

    info = robot_move.info()
    assert info["result"] == 11, info["result"]
    assert info["commands"] == 1, info["commands"]
