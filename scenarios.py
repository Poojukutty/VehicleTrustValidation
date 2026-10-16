
from vehicle import vehicle_safety_system

scenarios = [
    {
        "name": "Emergency braking",
        "speed": 40,
        "distance": 5,
        "expected": "BRAKE",
        "priority": "CRITICAL"
    },
    {
        "name": "Sudden obstacle",
        "speed": 60,
        "distance": 8,
        "expected": "BRAKE",
        "priority": "CRITICAL"
    },
    {
        "name": "Missing sensor data",
        "speed": 40,
        "distance": None,
        "expected": "SENSOR_FAULT",
        "priority": "HIGH"
    },
    {
        "name": "Invalid negative distance",
        "speed": 40,
        "distance": -5,
        "expected": "INVALID_INPUT",
        "priority": "HIGH"
    },
    {
        "name": "Clear road",
        "speed": 40,
        "distance": 50,
        "expected": "CONTINUE",
        "priority": "LOW"
    }
]

priority_order = {
    "CRITICAL": 3,
    "HIGH": 2,
    "LOW": 1
}

scenarios.sort(
    key=lambda item: priority_order[item["priority"]],
    reverse=True
)

passed = 0
failed = 0

print("=== AUTOMATED SCENARIO TESTING ===")

for scenario in scenarios:
    actual = vehicle_safety_system(
        scenario["speed"],
        scenario["distance"]
    )

    if actual == scenario["expected"]:
        print(f"PASS: {scenario['name']}")
        passed += 1
    else:
        print(f"FAIL: {scenario['name']}")
        print("  Expected:", scenario["expected"])
        print("  Actual:  ", actual)
        failed += 1

print("\n=== FINAL REPORT ===")
print("Total:", passed + failed)
print("Passed:", passed)
print("Failed:", failed)

if failed:
    print("OTA STATUS: BLOCKED")
else:
    print("OTA STATUS: TESTS PASSED")
