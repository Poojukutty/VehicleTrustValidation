
def inject_fault(speed, distance, fault_type="BRAKING_FAILURE"):
    """
    Educational simulation only.
    Simulates different faults for regression testing.
    """

    if speed is None or distance is None:
        return "SENSOR_FAULT"

    if not isinstance(speed, (int, float)):
        return "INVALID_INPUT"

    if not isinstance(distance, (int, float)):
        return "SENSOR_FAULT"

    if speed < 0 or distance < 0:
        return "INVALID_INPUT"

    # Simulated fault types
    if fault_type == "BRAKING_FAILURE":
        if distance < 10 and speed > 0:
            return "CONTINUE"  # Intentional fault

    elif fault_type == "SENSOR_FAILURE":
        return "SENSOR_FAULT"

    elif fault_type == "DELAYED_RESPONSE":
        if distance < 10 and speed > 0:
            return "CONTINUE"  # Simulates delayed braking

    elif fault_type == "NORMAL":
        if distance < 10 and speed > 0:
            return "BRAKE"
        return "CONTINUE"

    return "CONTINUE"


def run_fault_demo():
    test_cases = [
        {
            "name": "Braking Failure",
            "speed": 40,
            "distance": 5,
            "fault": "BRAKING_FAILURE",
            "expected": "BRAKE"
        },
        {
            "name": "Sensor Failure",
            "speed": 30,
            "distance": None,
            "fault": "SENSOR_FAILURE",
            "expected": "BRAKE"
        },
        {
            "name": "Delayed Response",
            "speed": 50,
            "distance": 3,
            "fault": "DELAYED_RESPONSE",
            "expected": "BRAKE"
        },
        {
            "name": "Normal Operation",
            "speed": 40,
            "distance": 20,
            "fault": "NORMAL",
            "expected": "CONTINUE"
        }
    ]

    print("=== ADVANCED FAULT INJECTION ===")

    for case in test_cases:
        result = inject_fault(
            case["speed"],
            case["distance"],
            case["fault"]
        )

        passed = result == case["expected"]

        print(f"\nScenario: {case['name']}")
        print(f"Expected: {case['expected']}")
        print(f"Actual: {result}")
        print(f"Test Result: {'PASS' if passed else 'FAIL'}")

        if not passed:
            print("Simulated OTA Status: BLOCKED")


if __name__ == "__main__":
    run_fault_demo()
