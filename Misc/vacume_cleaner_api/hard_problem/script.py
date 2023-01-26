import json

from tibber.schema import RobotMove

with open("RobotCleanerPathHeavy.json", "r") as in_json:
    robot_move_json = json.load(in_json)

# This is the heavy compute
duration = RobotMove(**robot_move_json).info()["result"]

print(f"Result for heavy numpy (result is elapsed time=): {RobotMove(**robot_move_json).info()}")
