import json
import math
import os


# ==========================================
# AI POOKALABOT - POOKALAM PLANNER
# ==========================================

INPUT_FILE = "data/plans/pookalam_analysis.json"
OUTPUT_FILE = "data/plans/robot_plan.json"

# Maximum pookalam radius in millimetres
MAX_RADIUS = 180

# Minimum radius allowed
MIN_RADIUS = 20

# Allowed flower colours
ALLOWED_COLORS = {
    "yellow",
    "red"
}


# ==========================================
# LOAD GEMINI ANALYSIS
# ==========================================

def load_analysis():

    if not os.path.exists(INPUT_FILE):

        print("❌ Analysis file not found!")
        print(f"Expected: {INPUT_FILE}")

        return None

    try:

        with open(INPUT_FILE, "r") as file:

            data = json.load(file)

        print("✅ Gemini analysis loaded.")

        return data

    except json.JSONDecodeError:

        print("❌ Analysis file contains invalid JSON.")

        return None


# ==========================================
# VALIDATE COLOUR
# ==========================================

def validate_color(color):

    color = color.lower().strip()

    if color not in ALLOWED_COLORS:

        print(
            f"⚠️ Invalid colour '{color}'. "
            f"Using yellow instead."
        )

        return "yellow"

    return color


# ==========================================
# CREATE CIRCULAR RING
# ==========================================

def create_ring(radius, color, symmetry):

    points = []

    color = validate_color(color)

    # Generate points around the circle
    for i in range(symmetry):

        angle = (
            2 * math.pi * i
        ) / symmetry

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        points.append({
            "x": round(x, 2),
            "y": round(y, 2),
            "color": color
        })

    return points


# ==========================================
# CREATE POOKALAM PLAN
# ==========================================

def create_plan(data):

    print("\n📐 Creating robot movement plan...")

    # Get values from Gemini
    layers = int(data.get("layers", 3))

    symmetry = int(data.get("symmetry", 12))

    center_color = validate_color(
        data.get("center", "yellow")
    )

    pattern = data.get("pattern", [])


    # ======================================
    # SAFETY LIMITS
    # ======================================

    layers = max(
        1,
        min(layers, 5)
    )

    symmetry = max(
        4,
        min(symmetry, 24)
    )


    commands = []


    # ======================================
    # CENTER
    # ======================================

    print(
        f"\n🎯 Center → {center_color.upper()}"
    )

    commands.append({
        "command": "MOVE",
        "x": 0,
        "y": 0
    })

    commands.append({
        "command": "DISPENSE",
        "color": center_color,
        "amount": 20
    })


    # ======================================
    # CREATE LAYERS
    # ======================================

    for layer_number in range(1, layers + 1):

        # Look for Gemini's pattern information
        layer_info = None

        for item in pattern:

            if int(item.get("layer", 0)) == layer_number:

                layer_info = item

                break


        # If Gemini didn't specify this layer,
        # calculate a reasonable radius.
        if layer_info:

            radius = float(
                layer_info.get("radius", 0)
            )

            color = validate_color(
                layer_info.get(
                    "color",
                    "yellow"
                )
            )

        else:

            radius = (
                MAX_RADIUS
                * layer_number
                / (layers + 1)
            )

            # Alternate colours
            if layer_number % 2 == 1:

                color = "yellow"

            else:

                color = "red"


        # Safety limit radius
        radius = max(
            MIN_RADIUS,
            min(radius, MAX_RADIUS)
        )


        print(
            f"\n⭕ Layer {layer_number}"
        )

        print(
            f"   Radius: {radius:.1f} mm"
        )

        print(
            f"   Colour: {color.upper()}"
        )

        print(
            f"   Points: {symmetry}"
        )


        # Generate circular points
        ring_points = create_ring(
            radius,
            color,
            symmetry
        )


        # Convert points into robot commands
        for point in ring_points:

            commands.append({
                "command": "MOVE",
                "x": point["x"],
                "y": point["y"]
            })

            commands.append({
                "command": "DISPENSE",
                "color": point["color"],
                "amount": 20
            })


    # ======================================
    # STOP COMMAND
    # ======================================

    commands.append({
        "command": "STOP"
    })


    # ======================================
    # FINAL PLAN
    # ======================================

    plan = {

        "project": "AI PookalaBot",

        "style": data.get(
            "style",
            "traditional"
        ),

        "layers": layers,

        "symmetry": symmetry,

        "commands": commands
    }


    return plan


# ==========================================
# SAVE PLAN
# ==========================================

def save_plan(plan):

    os.makedirs(
        "data/plans",
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w"
    ) as file:

        json.dump(
            plan,
            file,
            indent=4
        )

    print(
        f"\n💾 Robot plan saved:"
        f"\n{OUTPUT_FILE}"
    )


# ==========================================
# DISPLAY PLAN SUMMARY
# ==========================================

def display_summary(plan):

    commands = plan["commands"]

    move_count = 0

    dispense_count = 0

    for command in commands:

        if command["command"] == "MOVE":

            move_count += 1

        elif command["command"] == "DISPENSE":

            dispense_count += 1


    print("\n==========================================")
    print("🌼 ROBOT PLAN SUMMARY")
    print("==========================================")

    print(
        "Style:",
        plan["style"]
    )

    print(
        "Layers:",
        plan["layers"]
    )

    print(
        "Symmetry:",
        plan["symmetry"]
    )

    print(
        "Movement commands:",
        move_count
    )

    print(
        "Dispensing commands:",
        dispense_count
    )

    print(
        "Total commands:",
        len(commands)
    )

    print("==========================================")


# ==========================================
# MAIN
# ==========================================

def main():

    print("\n")
    print("==========================================")
    print("🌼 AI POOKALABOT")
    print("   POOKALAM ROBOT PLANNER")
    print("==========================================")


    # Load Gemini result
    analysis = load_analysis()

    if analysis is None:

        return


    # Create robot plan
    plan = create_plan(
        analysis
    )


    # Save plan
    save_plan(
        plan
    )


    # Show summary
    display_summary(
        plan
    )


    print(
        "\n✅ ROBOT PLAN READY!"
    )


# ==========================================
# START
# ==========================================

if __name__ == "__main__":

    main()