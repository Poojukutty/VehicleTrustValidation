
def vehicle_safety_system(speed, obstacle_distance):
    if obstacle_distance is None:
        return "SENSOR_FAULT"

    if not isinstance(speed, (int, float)):
        return "INVALID_INPUT"

    if not isinstance(obstacle_distance, (int, float)):
        return "SENSOR_FAULT"

    if speed < 0 or obstacle_distance < 0:
        return "INVALID_INPUT"

    # Safety logic: apply emergency braking
    if obstacle_distance < 10 and speed > 0:
        return "BRAKE"

    return "CONTINUE"


if __name__ == "__main__":
    result = vehicle_safety_system(40, 5)
    print("Vehicle Decision:", result)
