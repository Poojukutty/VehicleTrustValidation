
import streamlit as st
import pandas as pd
from datetime import datetime
from database import save_regression_results
from database import get_regression_history

st.set_page_config(
    page_title="Vehicle Trust Validation",
    layout="wide"
)


from vehicle import vehicle_safety_system
import os

REPORT_FILE = "regression_reports.csv"


def calculate_ota_trust(rows, fault_results=None):
    """
    Educational simulation only.
    Calculates a test-based OTA trust score.
    """

    if not rows:
        return {
            "score": 0,
            "critical_failure": False,
            "status": "NOT TESTED",
            "passed": 0,
            "failed": 0,
            "total": 0,
        }

    total = len(rows)
    passed = sum(
        row.get("Test Result") == "PASS"
        for row in rows
    )
    failed = total - passed

    critical_scenarios = {
        "Emergency Braking",
        "Sudden Obstacle",
    }

    critical_failure = any(
        row.get("Scenario") in critical_scenarios
        and row.get("Test Result") != "PASS"
        for row in rows
    )

    # Include fault-injection failures in the OTA decision
    fault_failed = 0
    if fault_results is not None:
        fault_failed = sum(
            row.get("Test Result") == "FAIL"
            for row in fault_results
        )

    score = round((passed / total) * 100)

    if critical_failure or failed > 0 or fault_failed > 0:
        status = "BLOCKED"
    else:
        status = "READY"

    return {
        "score": score,
        "critical_failure": critical_failure,
        "status": status,
        "passed": passed,
        "failed": failed,
        "total": total,
        "fault_failed": fault_failed,
    }




def save_regression_report(rows):
    if not rows:
        return

    df = pd.DataFrame(rows)

    if os.path.exists(REPORT_FILE):
        df.to_csv(
            REPORT_FILE,
            mode="a",
            header=False,
            index=False
        )
    else:
        df.to_csv(REPORT_FILE, index=False)



def load_regression_report():
    if os.path.exists(REPORT_FILE):
        try:
            return pd.read_csv(REPORT_FILE)
        except pd.errors.ParserError:
            st.warning(
                "Saved report has mixed column formats. "
                "Using the latest valid report is recommended."
            )
            return pd.DataFrame()

    return pd.DataFrame()


# ---------------- LIGHT BLUE AUTOMOTIVE THEME ----------------


st.markdown("""
<style>
/* LIGHT BACKGROUND */
.stApp,
[data-testid="stAppViewContainer"] {
    background-color: #B8D4F0 !important;
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
    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
            "Run Time": run_time,
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
    save_regression_report(rows)
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
    st.subheader("OTA Trust Score")

    regression_rows = st.session_state.regression_rows

    if regression_rows is None:
        st.info("Run Regression Testing to calculate the OTA Trust Score.")
    else:
        fault_results = st.session_state.get("fault_results")
        trust = calculate_ota_trust(regression_rows, fault_results)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("OTA Trust Score", f"{trust['score']}%")
        col2.metric("Total Tests", trust["total"])
        col3.metric("Tests Passed", trust["passed"])
        col4.metric("Tests Failed", trust["failed"])

        st.progress(trust["score"] / 100)

        if trust["status"] == "BLOCKED":
            st.error("🚫 Simulated OTA Status: BLOCKED")
        else:
            st.success("✓ Simulated OTA Status: READY")

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
    st.write("DEBUG — First regression row:", st.session_state.regression_rows[0])
    save_regression_results(st.session_state.regression_rows)
    st.success("Regression results saved to database!")

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
    saved_reports = load_regression_report()

    if rows is None and not saved_reports.empty:
        rows = saved_reports.to_dict("records")

    before_results = {
        "Emergency Braking": "FAIL",
        "Sudden Obstacle": "FAIL",
        "Missing Sensor Data": "PASS",
        "Invalid Negative Distance": "PASS",
        "Clear Road": "PASS",
    }

    comparison_rows = []

    if rows is not None:
        for row in rows:
            scenario = row.get("Scenario", "Unknown")
            after = row.get("Test Result", "NOT TESTED")
            before = before_results.get(scenario, "NOT TESTED")

            if before == "PASS" and after == "FAIL":
                change = "NEW FAILURE"
            elif before == "FAIL" and after == "PASS":
                change = "FIXED"
            elif before == after:
                change = "NO CHANGE"
            else:
                change = "NEEDS REVIEW"

            comparison_rows.append({
                "Scenario": scenario,
                "Baseline Version": "v1.0",
                "Updated Version": "v2.0",
                "Before Fix": before,
                "After Fix": after,
                "Change": change,
            })

    comparison = pd.DataFrame(comparison_rows)
    st.divider()
    st.subheader("📚 Regression Test History")

    history = get_regression_history()

    if history:
        history_df = pd.DataFrame(
            history,
            columns=[
                "ID",
                "Run Time",
                "Scenario",
                "Expected",
                "Actual",
                "Test Result",
                "Version",
            ],
        )

        st.dataframe(
            history_df,
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("No saved regression history yet. Run the tests first.")


    if not comparison.empty:
        st.dataframe(
            comparison,
            width="stretch",
            hide_index=True,
        )

        st.subheader("Regression Pass Rate Comparison")

        before_pass = (comparison["Before Fix"] == "PASS").sum()
        before_fail = (comparison["Before Fix"] == "FAIL").sum()
        after_pass = (comparison["After Fix"] == "PASS").sum()
        after_fail = (comparison["After Fix"] == "FAIL").sum()

        chart = pd.DataFrame({
            "Version": ["Before Fix", "After Fix"],
            "Passed Scenarios": [before_pass, after_pass],
            "Failed Scenarios": [before_fail, after_fail],
        }).set_index("Version")

        st.bar_chart(chart, height=300)
    else:
        st.info("Run Regression Tests first to generate a comparison.")

    if rows is not None and len(rows) > 0:
        csv_data = pd.DataFrame(rows).to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇ Download Regression Report",
            data=csv_data,
            file_name="vehicle_regression_report.csv",
            mime="text/csv",
        )

    st.divider()
    st.subheader("Advanced Fault Injection Results")

    from fault_innjection import inject_fault

    fault_cases = [
        {
            "Scenario": "Braking Failure",
            "Speed": 40,
            "Distance": 5,
            "Fault": "BRAKING_FAILURE",
            "Expected": "BRAKE",
        },
        {
            "Scenario": "Sensor Failure",
            "Speed": 30,
            "Distance": None,
            "Fault": "SENSOR_FAILURE",
            "Expected": "BRAKE",
        },
        {
            "Scenario": "Delayed Response",
            "Speed": 50,
            "Distance": 3,
            "Fault": "DELAYED_RESPONSE",
            "Expected": "BRAKE",
        },
        {
            "Scenario": "Normal Operation",
            "Speed": 40,
            "Distance": 20,
            "Fault": "NORMAL",
            "Expected": "CONTINUE",
        },
    ]

    fault_rows = []

    for case in fault_cases:
        actual = inject_fault(
            case["Speed"],
            case["Distance"],
            case["Fault"],
        )

        fault_rows.append({
            "Scenario": case["Scenario"],
            "Expected": case["Expected"],
            "Actual": actual,
            "Test Result": (
                "PASS" if actual == case["Expected"] else "FAIL"
            ),
        })

    fault_df = pd.DataFrame(fault_rows)

    st.dataframe(
        fault_df,
        width="stretch",
        hide_index=True,
    )

    fault_passed = (fault_df["Test Result"] == "PASS").sum()
    fault_failed = (fault_df["Test Result"] == "FAIL").sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Fault Tests", len(fault_df))
    col2.metric("Passed", int(fault_passed))
    col3.metric("Failed", int(fault_failed))

    fault_csv = fault_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download Fault Report",
        data=fault_csv,
        file_name="vehicle_fault_report.csv",
        mime="text/csv",
    )


    

# ---------------- FAULT INJECTION PAGE ----------------
# ---------------- FAULT INJECTION PAGE ----------------

if st.session_state.current_page == "Fault Injection":
    import pandas as pd
    from fault_innjection import inject_fault

    st.title("⚠️ Fault Injection")
    st.write(
        "Demonstrate how intentional software faults "
        "are detected during regression validation."
    )

    test_cases = [
        {
            "Scenario": "Braking Failure",
            "Speed": 40,
            "Distance": 5,
            "Fault": "BRAKING_FAILURE",
            "Expected": "BRAKE",
        },
        {
            "Scenario": "Sensor Failure",
            "Speed": 30,
            "Distance": None,
            "Fault": "SENSOR_FAILURE",
            "Expected": "BRAKE",
        },
        {
            "Scenario": "Delayed Response",
            "Speed": 50,
            "Distance": 3,
            "Fault": "DELAYED_RESPONSE",
            "Expected": "BRAKE",
        },
        {
            "Scenario": "Normal Operation",
            "Speed": 40,
            "Distance": 20,
            "Fault": "NORMAL",
            "Expected": "CONTINUE",
        },
    ]

    results = []

    for case in test_cases:
        actual = inject_fault(
            case["Speed"],
            case["Distance"],
            case["Fault"],
        )

        passed = actual == case["Expected"]

        results.append({
            "Scenario": case["Scenario"],
            "Speed (km/h)": case["Speed"],
            "Distance (m)": (
                case["Distance"]
                if case["Distance"] is not None
                else "Missing"
            ),
            "Expected": case["Expected"],
            "Actual": actual,
            "Test Result": "PASS" if passed else "FAIL",
        })

    st.subheader("Advanced Fault Scenarios")
    results_df = pd.DataFrame(results)

    st.session_state.fault_results = results

    st.download_button(
        label="⬇️ Download Fault Report",
        data=results_df.to_csv(index=False).encode("utf-8"),
        file_name="vehicle_fault_report.csv",
        mime="text/csv",
    )

    st.dataframe(
        results_df,
        width="stretch",
        hide_index=True,
    )

    passed_count = sum(
        row["Test Result"] == "PASS" for row in results
    )
    failed_count = len(results) - passed_count
    pass_rate = (passed_count / len(results)) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tests", len(results))
    col2.metric("Passed", passed_count)
    col3.metric("Failed", failed_count)

    st.progress(pass_rate / 100)
    st.caption(f"Pass rate: {pass_rate:.0f}%")

    st.subheader("Simulated OTA Decision")

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

        fault_failures = [
            row for row in results
            if row["Test Result"] != "PASS"
        ]

        if critical_failures or fault_failures:
            st.warning("SIMULATED OTA STATUS: BLOCKED")
            st.write(
                "Reason: One or more critical regression or "
                "fault-injection tests failed."
            )
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
