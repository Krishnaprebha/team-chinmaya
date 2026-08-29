import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv


# ==========================================
# AI POOKALABOT - GEMINI VISION
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "❌ GEMINI_API_KEY not found!\n"
        "Check your .env file."
    )

# Connect to Gemini
client = genai.Client(api_key=API_KEY)


# ==========================================
# ANALYZE POOKALAM
# ==========================================

def analyze_pookalam(image_path):

    print("\n📷 Reading image...")

    # Check image exists
    if not os.path.exists(image_path):
        print("❌ Image not found!")
        print("Path:", image_path)
        return None

    # Read image
    with open(image_path, "rb") as file:
        image_data = file.read()

    print("🧠 Sending image to Gemini Vision...")


    # ======================================
    # GEMINI PROMPT
    # ======================================

    prompt = """
You are the AI vision system of an autonomous
Onam Pookalam Robot.

Analyze the provided image of an Onam pookalam.

The robot can use ONLY TWO flower colours:

1. yellow
2. red

Do NOT use white, pink, green, orange, blue,
purple or any other colour.

Analyze the pookalam and identify:

1. Overall style
2. Number of visible layers
3. Main arrangement
4. Centre design
5. Radial symmetry
6. Which areas should contain yellow flowers
7. Which areas should contain red flowers
8. Overall confidence

The robot works on a circular pookalam platform.

Coordinate system:

Centre = (0, 0)

Maximum radius = 180 mm.

Return ONLY valid JSON.

DO NOT use Markdown.

DO NOT use ```json.

DO NOT include explanations.

Use exactly this structure:

{
    "style": "traditional",
    "layers": 4,
    "symmetry": 12,
    "colors": [
        "yellow",
        "red"
    ],
    "center": "yellow",
    "pattern": [
        {
            "layer": 1,
            "radius": 40,
            "color": "yellow"
        },
        {
            "layer": 2,
            "radius": 80,
            "color": "red"
        }
    ],
    "confidence": 0.95
}

RULES:

- layers must be between 1 and 5.
- symmetry must be between 4 and 24.
- Only yellow and red are allowed.
- Every color value must be either "yellow" or "red".
- Radius must be between 20 and 180 mm.
- Keep the design radially symmetrical.
- The centre must be either yellow or red.
- Maximum 5 pattern layers.
- confidence must be between 0 and 1.
"""


    # ======================================
    # SEND IMAGE TO GEMINI
    # ======================================

    response = client.models.generate_content(
        model="gemini-2.5-flash",

        contents=[
            types.Part.from_bytes(
                data=image_data,
                mime_type="image/jpeg"
            ),
            prompt
        ]
    )


    # ======================================
    # GET RESPONSE
    # ======================================

    result = response.text.strip()

    print("\n========== GEMINI RESULT ==========")
    print(result)


    # ======================================
    # CLEAN GEMINI RESPONSE
    # ======================================

    # Gemini may sometimes return:
    #
    # ```json
    # {
    #     ...
    # }
    # ```
    #
    # Remove Markdown code fences.

    if result.startswith("```"):

        result = result.replace("```json", "")
        result = result.replace("```JSON", "")
        result = result.replace("```", "")

        result = result.strip()


    # ======================================
    # CONVERT TO JSON
    # ======================================

    try:

        data = json.loads(result)

    except json.JSONDecodeError:

        print("\n❌ Gemini returned invalid JSON.")

        print("\nRaw response:")
        print(result)

        return None


    # ======================================
    # VALIDATE BASIC FIELDS
    # ======================================

    required_fields = [
        "style",
        "layers",
        "symmetry",
        "colors",
        "center",
        "pattern",
        "confidence"
    ]

    for field in required_fields:

        if field not in data:

            print(
                f"\n❌ Missing field: {field}"
            )

            return None


    # ======================================
    # VALIDATE COLOURS
    # ======================================

    allowed_colors = [
        "yellow",
        "red"
    ]

    # Check main colours
    for color in data["colors"]:

        if color.lower() not in allowed_colors:

            print(
                f"\n❌ Invalid colour detected: {color}"
            )

            return None


    # Check centre colour
    if data["center"].lower() not in allowed_colors:

        print(
            "\n❌ Invalid centre colour:",
            data["center"]
        )

        return None


    # Check pattern colours
    for item in data["pattern"]:

        color = item["color"].lower()

        if color not in allowed_colors:

            print(
                f"\n❌ Invalid pattern colour: {color}"
            )

            return None


    # ======================================
    # SUCCESS
    # ======================================

    print("\n✅ Pookalam successfully analyzed!")


    # ======================================
    # DISPLAY RESULT
    # ======================================

    print("\n🌸 POOKALAM ANALYSIS")
    print("============================")

    print(
        "Style:",
        data["style"]
    )

    print(
        "Layers:",
        data["layers"]
    )

    print(
        "Symmetry:",
        data["symmetry"]
    )

    print(
        "Colours:",
        ", ".join(data["colors"])
    )

    print(
        "Centre:",
        data["center"]
    )

    print(
        "Confidence:",
        data["confidence"]
    )


    # ======================================
    # DISPLAY PATTERN
    # ======================================

    print("\n🌼 FLOWER PATTERN")
    print("============================")

    for item in data["pattern"]:

        print(
            f"Layer {item['layer']} "
            f"→ Radius {item['radius']} mm "
            f"→ {item['color'].upper()}"
        )


    # ======================================
    # SAVE ANALYSIS
    # ======================================

    output_folder = "data/plans"

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    output_file = os.path.join(
        output_folder,
        "pookalam_analysis.json"
    )

    with open(
        output_file,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


    print(
        f"\n💾 Analysis saved to:"
        f"\n{output_file}"
    )


    return data


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("🌼 AI POOKALABOT")
    print("   GEMINI VISION SYSTEM")
    print("==========================================")

    print("\n🌸 Available flowers:")
    print("   🟡 Yellow")
    print("   🔴 Red")


    # Get image path
    image_path = input(
        "\nEnter image path: "
    ).strip()


    # Analyze
    result = analyze_pookalam(
        image_path
    )


    # Final status
    if result:

        print()
        print("==========================================")
        print("✅ AI ANALYSIS COMPLETE")
        print("==========================================")

    else:

        print()
        print("==========================================")
        print("❌ AI ANALYSIS FAILED")
        print("==========================================")