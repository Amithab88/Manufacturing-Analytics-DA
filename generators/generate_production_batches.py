import pandas as pd
import random
from datetime import datetime, timedelta


# ==========================================================
# Configuration
# ==========================================================

TOTAL_BATCHES = 100000
START_DATE = "2023-01-01"
END_DATE = "2026-06-30"
QUALITY_INSPECTION_RATE = 0.25

import os

# ==========================================================
# Load Reference Data
# ==========================================================

BASE_DATA_PATH = "C:/Users/AMITHAB/OneDrive/Documents/My Project/manufacturing-analytics/data/raw"

EMPLOYEES_FILE = os.path.join(BASE_DATA_PATH, "employees.csv")
MACHINES_FILE = os.path.join(BASE_DATA_PATH, "machines.csv")
PRODUCTS_FILE = os.path.join(BASE_DATA_PATH, "products.csv")
SHIFTS_FILE = os.path.join(BASE_DATA_PATH, "shifts.csv")

# ----------------------------------------------------------
# Verify Files Exist
# ----------------------------------------------------------

required_files = [
    EMPLOYEES_FILE,
    MACHINES_FILE,
    PRODUCTS_FILE,
    SHIFTS_FILE
]

for file_path in required_files:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Missing required file: {file_path}")

# ----------------------------------------------------------
# Load CSV Files
# ----------------------------------------------------------

employees_df = pd.read_csv(EMPLOYEES_FILE)

machines_df = pd.read_csv(MACHINES_FILE)

products_df = pd.read_csv(PRODUCTS_FILE)

shifts_df = pd.read_csv(SHIFTS_FILE)

# ----------------------------------------------------------
# Validate Required Columns
# ----------------------------------------------------------

required_employee_columns = {
    "employee_id",
    "designation",
    "factory_id",
    "shift_id",
    "experience_years"
}

required_machine_columns = {
    "machine_id",
    "machine_type",
    "status",
    "factory_id",
    "installation_date"
}

required_product_columns = {
    "product_id",
    "category"
}

required_shift_columns = {
    "shift_id"
}

if not required_employee_columns.issubset(employees_df.columns):
    raise ValueError("employees.csv is missing one or more required columns.")

if not required_machine_columns.issubset(machines_df.columns):
    raise ValueError("machines.csv is missing one or more required columns.")

if not required_product_columns.issubset(products_df.columns):
    raise ValueError("products.csv is missing one or more required columns.")

if not required_shift_columns.issubset(shifts_df.columns):
    raise ValueError("shifts.csv is missing one or more required columns.")

print("✓ Reference datasets loaded successfully.")