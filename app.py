
import streamlit as st
import pandas as pd

from vehicle import vehicle_safety_system

st.set_page_config(
    page_title="Vehicle Trust Validation",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- LIGHT BLUE AUTOMOTIVE THEME ----------------


st.markdown("""
<style>
/* LIGHT BACKGROUND */
.stApp,
[data-testid="stAppViewContainer"] {
    background-color: #F5F9FF !important;
    color: #172B4D !important;
}


/* ALL TEXT — BOLD AND CLEAR */
html, body, p, span, label, li, div,
.stMarkdown, .stText,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stWidgetLabel"] p {
    color: #172B4D !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    line-height: 1.65 !important;
    opacity: 1 !important;
}

/* HEADINGS — EXTRA BOLD */
h1 {
    color: #123B63 !important;
    font-size: 40px !important;
    font-weight: 800 !important;
}
h2 {
    color: #174F80 !important;
    font-size: 32px !important;
    font-weight: 800 !important;
}
h3 {
    color: #174F80 !important;
    font-size: 25px !important;
    font-weight: 750 !important;
}

/* BUTTON TEXT — BOLD */
.stButton button,
.stDownloadButton button {
    font-size: 18px !important;
    font-weight: 800 !important;
}


/* HEADINGS */
h1 {
    color: #123B63 !important;
    font-size: 40px !important;
    font-weight: 800 !important;
}
h2 {
    color: #174F80 !important;
    font-size: 32px !important;
    font-weight: 750 !important;
}
h3 {
    color: #174F80 !important;
    font-size: 25px !important;
    font-weight: 700 !important;
}

/* SIDEBAR TEXT, IF SHOWN */
[data-testid="stSidebar"] * {
    color: #172B4D !important;
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #C5DDF5 !important;
    border-radius: 14px !important;
    padding: 22px !important;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #243B53 !important;
    font-size: 17px !important;
}
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #0759A5 !important;
    font-size: 36px !important;
    font-weight: 800 !important;
}

/* BUTTONS */
.stButton button,
.stDownloadButton button {
    background: #DCEEFF !important;
    color: #123B63 !important;
    border: 2px solid #83B5E5 !important;
    border-radius: 10px !important;
    min-height: 52px !important;
    font-size: 18px !important;
    font-weight: 750 !important;
    opacity: 1 !important;
}
.stButton button:hover,
.stDownloadButton button:hover {
    background: #BBDFFF !important;
    color: #102F50 !important;
    border-color: #367DB8 !important;
}

/* PRIMARY BUTTON */
.stButton button[kind="primary"] {
    background: #1769AA !important;
    color: #FFFFFF !important;
    border-color: #1769AA !important;
}

/* SLIDERS AND CHECKBOXES */
[data-testid="stSlider"] *,
[data-testid="stCheckbox"] * {
    color: #172B4D !important;
    font-size: 17px !important;
}

/* TABLE TEXT */
[data-testid="stDataFrame"] {
    background: #FFFFFF !important;
}
[data-testid="stDataFrame"] * {
    font-size: 16px !important;
}

/* REMOVE EXTRA SIDEBAR */
[data-testid="stSidebar"] {
    display: none !important;
}

/* HEADER */
.car-header {
    background: #E6F2FF !important;
    border: 1px solid #BFD9F2 !important;
    border-radius: 16px !important;
    padding: 28px !important;
}

/* ROAD SIMULATION */
.car-road {
    position: relative;
    height: 190px;
    background: #E2EAF3;
    border: 1px solid #B8CDDF;
    border-radius: 14px;
    overflow: hidden;
    margin: 18px 0;
}
.road-line {
    position: absolute;
    top: 92px;
    width: 100%;
    border-top: 3px dashed #FFFFFF;
}

.car {
    position: absolute;
    top: 58px;
    left: 5%;
    font-size: 52px;
    animation: drive 3s ease-in-out infinite alternate;
}

.car.braking {
    animation: brake 0.7s ease-out forwards !important;
    filter: drop-shadow(0 0 8px #E53935);
}

.car-road.brake-mode {
    border: 2px solid #E53935;
}

@keyframes brake {
    from { transform: translateX(100px); }
    to { transform: translateX(15px); }
}

.obstacle {
    position: absolute;
    top: 62px;
    right: 12%;
    font-size: 38px;
}
.road-label {
    position: absolute;
    bottom: 10px;
    left: 14px;
    color: #172B4D !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}
@keyframes drive {
    from { transform: translateX(0); }
    to { transform: translateX(100px); }
}
</style>
""", unsafe_allow_html=True)




# ---------------- REFERENCE SOFTWARE ----------------
def baseline_vehicle_software(speed, distance):
    if distance is None:
        return "SENSOR_FAULT"

    if not isinstance(speed, (int, float)):
        return "INVALID_INPUT"

    if not isinstance(distance, (int, float)):
        return "SENSOR_FAULT"

    if speed < 0 or distance < 0:
        return "INVALID_INPUT"

    if distance < 10 and speed > 0:
        return "BRAKE"

    return "CONTINUE"


# ---------------- TEST SCENARIOS ----------------
scenarios = [
    {
        "name": "Emergency Braking",
        "speed": 40,
        "distance": 5,
        "expected": "BRAKE",
        "priority": "CRITICAL"
    },
    {
        "name": "Sudden Obstacle",
        "speed": 60,
        "distance": 8,
        "expected": "BRAKE",
        "priority": "CRITICAL"
    },
    {
        "name": "Missing Sensor Data",
        "speed": 40,
        "distance": None,
        "expected": "SENSOR_FAULT",
        "priority": "HIGH"
    },
    {
        "name": "Invalid Negative Distance",
        "speed": 40,
        "distance": -5,
        "expected": "INVALID_INPUT",
        "priority": "HIGH"
    },
    {
        "name": "Clear Road",
        "speed": 40,
        "distance": 50,
        "expected": "CONTINUE",
        "priority": "LOW"
    }
]


# ---------------- SESSION STATE ----------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "simulation_result" not in st.session_state:
    st.session_state.simulation_result = None

if "regression_rows" not in st.session_state:
    st.session_state.regression_rows = None
    st.session_state.previous_regression_rows = None


# ---------------- FUNCTIONS ----------------
def execute_regression_tests():
    if st.session_state.regression_rows is not None:
        st.session_state.previous_regression_rows = (
        st.session_state.regression_rows.copy()
    )

    rows = []
    priority_order = {"CRITICAL": 0, "HIGH": 1, "LOW": 2}

    ordered = sorted(
        scenarios,
        key=lambda s: priority_order[s["priority"]]
    )

    for scenario in ordered:
        speed = scenario["speed"]
        distance = scenario["distance"]
        expected = scenario["expected"]

        baseline = baseline_vehicle_software(speed, distance)
        updated = vehicle_safety_system(speed, distance)

        rows.append({
            "Scenario": scenario["name"],
            "Priority": scenario["priority"],
            "Expected": expected,
            "Baseline": baseline,
            "Updated": updated,
            "Test Result": (
                "PASS" if updated == expected else "FAIL"
            ),
            "Regression": (
                "DETECTED" if baseline != updated else "None"
            )
        })

    return rows


def show_metrics(rows):
    total = len(rows)
    passed = sum(r["Test Result"] == "PASS" for r in rows)
    failed = total - passed
    rate = passed / total * 100 if total else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Scenarios", total)
    c2.metric("Tests Passed", passed)
    c3.metric("Tests Failed", failed)
    c4.metric("Pass Rate", f"{rate:.0f}%")

    return total, passed, failed, rate



def show_car(speed, distance, result="READY"):
    obstacle = (
        "🚧"
        if distance is not None and distance < 15
        else "🪧"
    )

    if result == "BRAKE":
        car_class = "car braking"
        road_class = "car-road brake-mode"
    else:
        car_class = "car"
        road_class = "car-road"

    st.markdown(
        f"""
        <div class="{road_class}">
            <div class="road-line"></div>
            <div class="{car_class}">🚘</div>
            <div class="obstacle">{obstacle}</div>
            <div class="road-label">
                SIMULATED VEHICLE · {speed} km/h · STATUS: {result}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



# ---------------- HEADER ----------------
st.markdown("""
<div class="car-header">
    <h1 style="margin:0;">🚘 Vehicle Trust Validation</h1>
    <p style="margin:8px 0 0 0;">
        Driving Simulation · Software Testing · Regression Analysis
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------- PAGE CONTENT ----------------
page = st.session_state.current_page

if page == "Dashboard":
    st.subheader("Dashboard Overview")

    rows = st.session_state.regression_rows

    if rows is None:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Scenarios", len(scenarios))
        c2.metric("Tests Passed", "—")
        c3.metric("Tests Failed", "—")
        c4.metric("Pass Rate", "—")
    else:
        show_metrics(rows)

    st.divider()
    st.subheader("Vehicle Status")

    sim = st.session_state.simulation_result

    if sim is None:
        speed = 40
        distance = 25
        result = "READY"
    else:
        speed = sim["speed"]
        distance = sim["distance"]
        result = sim["actual"]

    left, right = st.columns([1.3, 1])

    with left:
        st.markdown("### Driving Environment")
        show_car(speed, distance,result)

    with right:
        st.markdown("### Current Readings")
        st.metric("Vehicle Speed", f"{speed} km/h")
        st.metric(
            "Obstacle Distance",
            "No sensor data" if distance is None else f"{distance} m"
        )

        if result == "BRAKE":
            st.error("🛑 BRAKE")
        elif result == "SENSOR_FAULT":
            st.warning("Sensor fault detected")
        elif result == "INVALID_INPUT":
            st.warning("Invalid input")
        elif result == "CONTINUE":
            st.success("✓ CONTINUE")
        else:
            st.info("Run the simulator to view a result.")

elif page == "Driving Simulator":
    st.subheader("Driving Simulator")

    controls, visual = st.columns([0.85, 1.4])

    with controls:
        speed = st.slider("Vehicle Speed (km/h)", 0, 120, 40, 5)
        distance = st.slider("Obstacle Distance (m)", 0, 100, 5)
        missing_sensor = st.checkbox("Simulate missing sensor data")

        if st.button("▶ Run Simulation", type="primary",
                     width="stretch"):
            sensor_distance = None if missing_sensor else distance

            expected = baseline_vehicle_software(
                speed, sensor_distance
            )
            actual = vehicle_safety_system(
                speed, sensor_distance
            )

            st.session_state.simulation_result = {
                "speed": speed,
                "distance": sensor_distance,
                "expected": expected,
                "actual": actual
            }

    sim = st.session_state.simulation_result

    with visual:
        st.markdown("### Vehicle Simulation")

        if sim is None:
            shown_speed = speed
            shown_distance = None if missing_sensor else distance
            shown_result = "READY"
        else:
            shown_speed = sim["speed"]
            shown_distance = sim["distance"]
            shown_result = sim["actual"]

        show_car(shown_speed, shown_distance,shown_result)

        st.metric("Vehicle Speed", f"{shown_speed} km/h")
        st.metric(
            "Obstacle Distance",
            "No sensor data" if shown_distance is None
            else f"{shown_distance} m"
        )

        if shown_result == "BRAKE":
            st.error("🛑 BRAKE COMMAND")
        elif shown_result == "SENSOR_FAULT":
            st.warning("Sensor fault")
        elif shown_result == "INVALID_INPUT":
            st.warning("Invalid input")
        elif shown_result == "CONTINUE":
            st.success("✓ CONTINUE")
        else:
            st.info("Run the simulation.")

elif page == "Regression Testing":
    st.subheader("Automated Regression Testing")

    if st.button("▶ Run Full Regression Tests", type="primary"):
        st.session_state.regression_rows = execute_regression_tests()

    rows = st.session_state.regression_rows

    if rows is None:
        st.info("Run the test suite to generate results.")
    else:
        total, passed, failed, rate = show_metrics(rows)

        st.dataframe(
            pd.DataFrame(rows),
            width="stretch",
            hide_index=True
        )

        coverage = len(rows) / len(scenarios) if scenarios else 0

        st.subheader("Scenario Coverage")
        st.progress(coverage)
        st.write(f"{len(rows)} of {len(scenarios)} scenarios executed")

        critical_failure = any(
            r["Priority"] == "CRITICAL"
            and r["Test Result"] == "FAIL"
            for r in rows
        )

        st.subheader("Simulated OTA Decision")

        if critical_failure:
            st.error("BLOCKED — critical test failure.")
        elif failed:
            st.warning("REVIEW REQUIRED — test failures detected.")
        else:
            st.success("All listed tests passed in this simulation.")

        csv_data = pd.DataFrame(rows).to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download CSV Report",
            data=csv_data,
            file_name="vehicle_regression_report.csv",
            mime="text/csv"
        )


elif page == "Reports & Comparison":
    st.subheader("Before vs After Comparison")

    rows = st.session_state.regression_rows
    previous_rows = st.session_state.previous_regression_rows
    before_results = {
        "Emergency Braking": "FAIL",
        "Sudden Obstacle": "FAIL",
        "Missing Sensor Data": "PASS",
        "Invalid Negative Distance": "PASS",
        "Clear Road": "PASS"
    }

    comparison_rows = []

    if rows is not None:
        for row in rows:
            scenario = row.get("Scenario", "Unknown")
            after = row.get("Test Result", "NOT TESTED")
            before = before_results.get(scenario, "NOT TESTED")

            comparison_rows.append({
                "Scenario": scenario,
                "Before Fix": before,
                "After Fix": after
            })
    comparison = pd.DataFrame(comparison_rows)

    st.dataframe(
        comparison,
        width="stretch",
        hide_index=True
    )

    st.subheader("Pass Rate Comparison")

    if not comparison.empty:
        before_pass = (comparison["Before Fix"] == "PASS").sum()
        before_fail = (comparison["Before Fix"] == "FAIL").sum()
        after_pass = (comparison["After Fix"] == "PASS").sum()
        after_fail = (comparison["After Fix"] == "FAIL").sum()

        chart = pd.DataFrame({
            "Version": ["Before Fix", "After Fix"],
            "Passed Scenarios": [before_pass, after_pass],
            "Failed Scenarios": [before_fail, after_fail]
        }).set_index("Version")

        st.bar_chart(chart, height=300)
    else:
        st.info("Run Regression Tests first to generate a comparison.")
    if rows is not None and len(rows) > 0:
        csv_data = pd.DataFrame(rows).to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Latest Report",
            data=csv_data,
            file_name="vehicle_regression_report.csv",
            mime="text/csv"
        )


    

# ---------------- FAULT INJECTION PAGE ----------------
# ---------------- FAULT INJECTION PAGE ----------------
if st.session_state.current_page == "Fault Injection":
    st.title("⚠️ Fault Injection")
    st.write("Demonstrate how an intentional software fault is detected.")

    speed = 40
    obstacle_distance = 5
    expected = "BRAKE"

    from fault_innjection import inject_fault

    faulty_result = inject_fault(speed, obstacle_distance)

    st.subheader("Test Scenario")
    st.write(f"Speed: {speed} km/h")
    st.write(f"Obstacle distance: {obstacle_distance} m")
    st.write(f"Expected result: {expected}")
    st.write(f"Faulty result: {faulty_result}")

    if faulty_result != expected:
        st.error("TEST RESULT: FAIL")
    else:
        st.success("TEST RESULT: PASS")

    regression_rows = st.session_state.regression_rows

    if regression_rows is None:
        st.info("Run regression tests before deciding OTA status.")
        st.warning("SIMULATED OTA STATUS: BLOCKED")
    else:
        critical_failures = [
            row for row in regression_rows
            if row.get("Priority") == "CRITICAL"
            and row.get("Test Result") != "PASS"
        ]

        if faulty_result != expected or critical_failures:
            st.warning("SIMULATED OTA STATUS: BLOCKED")
        else:
            st.success("SIMULATED OTA STATUS: APPROVED")

    if faulty_result != expected or critical_failures:
        st.warning("SIMULATED OTA STATUS: BLOCKED")
    else:
        st.success("SIMULATED OTA STATUS: APPROVED")


# ---------------- BOTTOM NAVIGATION ----------------
st.divider()
st.markdown("### Navigation")

nav1, nav2, nav3, nav4 ,nav5= st.columns(5)


navigation = [
    ("🏠  Dashboard", "Dashboard", nav1),
    ("🚘  Driving Simulator", "Driving Simulator", nav2),
    ("🧪  Regression Tests", "Regression Testing", nav3),
    ("📊  Reports", "Reports & Comparison", nav4),
    ("⚠️  Fault Injection", "Fault Injection", nav5)
]

for label, page_value, column in navigation:
    with column:
        if st.button(
            label,
            key=f"nav_{page_value}",
            width="stretch",
            type=(
                "primary"
                if st.session_state.current_page == page_value
                else "secondary"
            )
        ):
            st.session_state.current_page = page_value
            st.rerun()

st.caption("Vehicle Trust Validation ·")
