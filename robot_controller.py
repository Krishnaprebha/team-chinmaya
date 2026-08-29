import json
import time

PLAN_FILE = "data/plans/robot_plan.json"


def move_to(x, y):
    print(f"🤖 MOVE → X: {x} mm | Y: {y} mm")
    time.sleep(0.2)


def select_flower(color):
    print(f"🌸 SELECT → {color.upper()}")
    time.sleep(0.2)


def dispense():
    print("🌼 DISPENSE → Petals released")
    time.sleep(0.4)


def execute_position(position):

    x = position["x"]
    y = position["y"]
    color = position["color"]

    move_to(x, y)

    select_flower(color)

    dispense()


def run_plan():

    print("\n================================")
    print("🌼 AI POOKALABOT")
    print("ROBOT SIMULATION")
    print("================================")

    with open(PLAN_FILE, "r") as file:
        plan = json.load(file)

    commands = plan["commands"]

    print(f"\n📍 Total positions: {len(commands)}")

    for number, position in enumerate(commands, start=1):

        print(f"\n[{number}/{len(commands)}]")

        execute_position(position)

    print("\n================================")
    print("✅ POOKALAM PLAN COMPLETE")
    print("================================")


if __name__ == "__main__":
    run_plan()