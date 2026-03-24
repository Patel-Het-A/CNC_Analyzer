from pipeline.pipeline import CNCPipeline
from utils.helpers import load_gcode_file
import os
from dotenv import load_dotenv

load_dotenv()

gcode = [
    "G21",
"G90",
"G00 Z10",

"G00 X0 Y20",
"G01 Z-2 F300",
"G01 X10 Y20",
"G01 X10 Y0",
"G01 X5 Y0",
"G01 X5 Y5",
"G00 Z10",

"G00 X15 Y20",
"G01 Z-2",
"G01 X25 Y20",
"G01 X15 Y20",
"G01 X15 Y0",
"G01 X25 Y0",
"G00 Z10",

"G00 X15 Y10",
"G01 Z-2",
"G01 X22 Y10",
"G00 Z10",

"G00 X30 Y20",
"G01 Z-2",
"G01 X40 Y20",
"G01 X30 Y20",
"G01 X30 Y0",
"G01 X40 Y0",
"G00 Z10",

"G00 X30 Y10",
"G01 Z-2",
"G01 X37 Y10",
"G00 Z10",

"G00 X45 Y20",
"G01 Z-2",
"G01 X60 Y20",
"G00 Z10",

"G00 X52.5 Y20",
"G01 Z-2",
"G01 X52.5 Y0",
"G00 Z10",

"M30"
]

api_key = os.getenv("GROQ_API_KEY")

pipeline = CNCPipeline(api_key=api_key)
result = pipeline.run(gcode)

print("\n--- ISSUES ---\n")
for issue in result["issues"]:
    print(issue)

print("\n--- METRICS ---\n")

print("Original:")
print(result["metrics"]["original"])

print("\nOptimized:")
print(result["metrics"]["optimized"])

print(f"\nImprovement:{result["metrics"]["improvemnt"]}%")


if result["ai"]:
    print("\n--- AI EXPLANATION ---\n")
    print(result["ai"]["explanation"])

    print("\n--- AI SUGGESTIONS BASED ON ISSUES ---\n")
    if result["issues"]==[]:
        print("No critical issues are found\n")
    else:
        print(result["ai"]["suggestion"])

viz = pipeline.visualizer

viz.show_3d(
    result["toolpath"],
    result["metrics"]["original"]["total"],
    result["optimized_toolpath"],
    result["metrics"]["optimized"]["total"],
    "G21"
)