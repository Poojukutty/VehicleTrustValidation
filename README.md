# Vehicle Trust Validation

A Python-based simulation and regression testing project designed to validate vehicle software behavior before and after software updates in Software-Defined Vehicles (SDVs).

## Project Overview

Vehicle Trust Validation simulates vehicle scenarios and checks whether the software responds as expected. It uses automated regression tests to identify failures, detect injected faults, and help determine whether a software update should be accepted or blocked.

## Key Features

- **Driving Scenario Simulation:** Tests vehicle behavior under different road and sensor conditions.
- **Automated Regression Testing:** Compares actual results against expected results.
- **Fault Injection:** Simulates software faults to identify safety-related failures.
- **Test Coverage:** Summarizes the number of scenarios tested.
- **OTA Update Validation:** Uses test results to determine whether an update should be blocked.
- **Interactive Dashboard:** Displays simulation and testing results through Streamlit.

## Technologies Used

- Python
- Streamlit
- Automated Software Testing
- Regression Testing
- Fault Injection
- Git and GitHub

## Test Scenarios

The project includes scenarios such as:

- Emergency braking
- Sudden obstacle detection
- Missing sensor data
- Invalid negative distance
- Clear road conditions

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Poojukutty/VehicleTrustValidation.git
```

### 2. Open the project folder

```bash
cd VehicleTrustValidation
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
python -m streamlit run app.py
```

The dashboard should open in your browser.

## Project Goal

The goal is to demonstrate how automated regression testing can help identify software defects and support safer validation of software updates in Software-Defined Vehicles.

## Future Enhancements

- Integration with a driving simulator
- Expanded vehicle and sensor test scenarios
- Before-and-after software update comparisons
- Detailed test reports and visualizations
- Improved fault detection and validation

## Disclaimer

This is an educational simulation and testing prototype. It is not certified for use in real vehicles and does not replace automotive safety validation.

## Author

Pooja Karthikeyan