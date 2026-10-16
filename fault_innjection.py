
def inject_fault(speed, distance):
    """
    Educational simulation only.
    Intentionally introduces a braking fault
    for regression testing.
    """

    if distance is None or speed is None:
        return "SENSOR_FAULT"

    if distance < 0 or speed < 0:
        return "INVALID_INPUT"

    # INTENTIONAL FAULT:
    # Emergency braking is incorrectly disabled.
    if distance < 10 and speed > 0:
        return "CONTINUE"

    return "CONTINUE"


def run_fault_demo():
    speed = 40
    distance = 5

    result = inject_fault(speed, distance)

    expected = "BRAKE"

    print("=== FAULT INJECTION DEMO ===")
    print(f"Speed: {speed} km/h")
    print(f"Obstacle distance: {distance} m")
    print(f"Expected result: {expected}")
    print(f"Faulty result: {result}")

    if result != expected:
        print("TEST RESULT: FAIL")
        print("OTA STATUS: BLOCKED")
    else:
        print("TEST RESULT: PASS")


if __name__ == "__main__":
    run_fault_demo()
