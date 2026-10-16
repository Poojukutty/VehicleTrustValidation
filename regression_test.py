
def old_vehicle_software(speed, distance):
    if distance < 10 and speed > 0:
        return "BRAKE"
    return "CONTINUE"


def updated_vehicle_software(speed, distance):
    # Simulated regression: braking is disabled
    return "CONTINUE"


test_cases = [
    ("Emergency braking", 40, 5),
    ("Clear road", 40, 50)
]

print("=== SOFTWARE REGRESSION TEST ===")

regressions = 0

for name, speed, distance in test_cases:
    old_result = old_vehicle_software(speed, distance)
    new_result = updated_vehicle_software(speed, distance)

    print(f"\nTest: {name}")
    print("Version 1.0:", old_result)
    print("Version 1.1:", new_result)

    if old_result != new_result:
        print("REGRESSION DETECTED")
        regressions += 1
    else:
        print("NO BEHAVIOR CHANGE")

print("\n=== RELEASE DECISION ===")

if regressions:
    print("OTA STATUS: BLOCKED")
    print("Regressions found:", regressions)
else:
    print("OTA STATUS: ELIGIBLE FOR FURTHER VALIDATION")
