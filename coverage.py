
scenarios = [
    {
        "name": "Emergency braking",
        "priority": "CRITICAL",
        "tested": True
    },
    {
        "name": "Clear road driving",
        "priority": "LOW",
        "tested": True
    },
    {
        "name": "Sensor failure",
        "priority": "HIGH",
        "tested": False
    },
    {
        "name": "Sudden obstacle",
        "priority": "CRITICAL",
        "tested": False
    }
]

scenarios.sort(
    key=lambda item: {
        "CRITICAL": 3,
        "HIGH": 2,
        "LOW": 1
    }[item["priority"]],
    reverse=True
)

print("=== PRIORITISED TEST SCENARIOS ===")

for scenario in scenarios:
    status = "TESTED" if scenario["tested"] else "NOT TESTED"

    print(
        scenario["priority"],
        "-",
        scenario["name"],
        "-",
        status
    )

total = len(scenarios)
tested = sum(item["tested"] for item in scenarios)
coverage = (tested / total) * 100

print("\n=== COVERAGE REPORT ===")
print("Total scenarios:", total)
print("Scenarios tested:", tested)
print(f"Scenario coverage: {coverage:.1f}%")
