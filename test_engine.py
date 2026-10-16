
from vehicle import vehicle_safety_system

def run_test(name, speed, distance, expected):
    actual = vehicle_safety_system(speed, distance)

    if actual == expected:
        print(f"PASS: {name}")
        return True
    else:
        print(f"FAIL: {name}")
        print(f"  Expected: {expected}")
        print(f"  Actual:   {actual}")
        return False


print("=== VEHICLE SAFETY TEST REPORT ===")

results = []

results.append(
    run_test("Nearby obstacle", 40, 5, "BRAKE")
)

results.append(
    run_test("Clear road", 40, 50, "CONTINUE")
)

passed = sum(results)
failed = len(results) - passed

print("\n=== SUMMARY ===")
print("Total tests:", len(results))
print("Passed:", passed)
print("Failed:", failed)

if failed > 0:
    print("VERDICT: UPDATE BLOCKED")
else:
    print("VERDICT: TESTS PASSED")

