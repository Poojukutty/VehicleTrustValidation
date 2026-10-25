
import sqlite3
from datetime import datetime

DB_NAME = "vehicle_trust.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS regression_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_time TEXT NOT NULL,
                scenario TEXT NOT NULL,
                expected_result TEXT,
                actual_result TEXT,
                test_result TEXT NOT NULL,
                version TEXT DEFAULT 'v2.0'
            )
        """)


def save_regression_results(results):
    with get_connection() as connection:
        for row in results:
            connection.execute("""
                INSERT INTO regression_history (
                    run_time,
                    scenario,
                    expected_result,
                    actual_result,
                    test_result,
                    version
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                row.get("Scenario", "Unknown"),
                row.get("Expected", "Unknown"),
                row.get("Updated", row.get("Actual", "Unknown")),
                row.get("Test Result", "NOT TESTED"),
                "v2.0"
            ))


def get_regression_history():
    with get_connection() as connection:
        return connection.execute("""
            SELECT *
            FROM regression_history
            ORDER BY id DESC
        """).fetchall()


initialize_database()
