import pandas as pd
import random
import os

from datetime import datetime, timedelta

# ==========================================================
# Configuration
# ==========================================================

TOTAL_MAINTENANCE_RECORDS = 6000

START_DATE = "2023-01-01"
END_DATE = "2026-06-30"

# Random number generator
rng = random.Random(42)

# ==========================================================
# File Paths
# ==========================================================

BASE_DATA_PATH = (
    "C:/Users/AMITHAB/OneDrive/Documents/"
    "My Project/manufacturing-analytics/data/raw"
)

MACHINES_FILE = os.path.join(
    BASE_DATA_PATH,
    "machines.csv"
)

EMPLOYEES_FILE = os.path.join(
    BASE_DATA_PATH,
    "employees.csv"
)

# ==========================================================
# Verify Files Exist
# ==========================================================

required_files = [
    MACHINES_FILE,
    EMPLOYEES_FILE
]

for file_path in required_files:

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Missing required file: {file_path}"
        )

# ==========================================================
# Load CSV Files
# ==========================================================

machines_df = pd.read_csv(MACHINES_FILE)

employees_df = pd.read_csv(EMPLOYEES_FILE)

print("✓ Reference datasets loaded successfully.")

# ==========================================================
# Validate Required Columns
# ==========================================================

required_machine_columns = {
    "machine_id",
    "machine_type",
    "factory_id",
    "status",
    "installation_date"
}

required_employee_columns = {
    "employee_id",
    "designation",
    "factory_id"
}

if not required_machine_columns.issubset(machines_df.columns):
    raise ValueError(
        "machines.csv is missing one or more required columns."
    )

if not required_employee_columns.issubset(employees_df.columns):
    raise ValueError(
        "employees.csv is missing one or more required columns."
    )

print("✓ Column validation completed successfully.")

# ==========================================================
# Prepare Reference Data
# ==========================================================

# ----------------------------------------------------------
# Convert Installation Date
# ----------------------------------------------------------

machines_df["installation_date"] = pd.to_datetime(
    machines_df["installation_date"]
)

# ----------------------------------------------------------
# Eligible Maintenance Employees
# ----------------------------------------------------------

eligible_designations = [
    "Maintenance Engineer",
    "Technician"
]

maintenance_employees = employees_df[
    employees_df["designation"].isin(
        eligible_designations
    )
].copy()

# ----------------------------------------------------------
# Build Employee Lookup by Factory
# ----------------------------------------------------------

maintenance_employees_by_factory = {}

for factory_id, group in maintenance_employees.groupby("factory_id"):

    maintenance_employees_by_factory[factory_id] = (
        group.to_dict("records")
    )

print("✓ Maintenance employee lookup created successfully.")

# ----------------------------------------------------------
# Cache Machine Records
# ----------------------------------------------------------

machine_records = machines_df.to_dict("records")

print("✓ Machine lookup cache created successfully.")

# ==========================================================
# Business Rules
# ==========================================================

# ----------------------------------------------------------
# Maintenance Type Distribution
# ----------------------------------------------------------

maintenance_types = [
    "Preventive",
    "Corrective",
    "Emergency",
    "Inspection"
]

maintenance_type_weights = [
    55,
    30,
    10,
    5
]

# ----------------------------------------------------------
# Maintenance Interval (Days)
# ----------------------------------------------------------

maintenance_interval_days = {
    "Active": (90, 180),
    "Under Maintenance": (15, 30),
    "Retired": (120, 240)
}

# ----------------------------------------------------------
# Downtime Hours
# ----------------------------------------------------------

downtime_ranges = {
    "Inspection": (1, 3),
    "Preventive": (2, 8),
    "Corrective": (6, 24),
    "Emergency": (12, 48)
}

# ----------------------------------------------------------
# Maintenance Cost (INR)
# ----------------------------------------------------------

maintenance_cost_ranges = {

    "CNC Machine": (10000, 40000),

    "Assembly Robot": (15000, 60000),

    "Injection Molding Machine": (8000, 30000),

    "Laser Cutter": (12000, 45000),

    "Hydraulic Press": (8000, 30000),

    "Packaging Machine": (5000, 15000),

    "Conveyor System": (3000, 8000)
}

# ----------------------------------------------------------
# Emergency Cost Multiplier
# ----------------------------------------------------------

EMERGENCY_COST_MULTIPLIER = 1.50

# ----------------------------------------------------------
# Date Objects
# ----------------------------------------------------------

START_DATE_OBJ = datetime.strptime(
    START_DATE,
    "%Y-%m-%d"
)

END_DATE_OBJ = datetime.strptime(
    END_DATE,
    "%Y-%m-%d"
)

print("✓ Business rules loaded successfully.")

# ==========================================================
# Helper Functions
# ==========================================================

# ----------------------------------------------------------
# Random Maintenance Date
# ----------------------------------------------------------

def random_maintenance_date():

    total_days = (END_DATE_OBJ - START_DATE_OBJ).days

    random_days = rng.randint(0, total_days)

    return START_DATE_OBJ + timedelta(days=random_days)


# ----------------------------------------------------------
# Select Maintenance Type
# ----------------------------------------------------------

def generate_maintenance_type():

    return rng.choices(
        maintenance_types,
        weights=maintenance_type_weights,
        k=1
    )[0]


# ----------------------------------------------------------
# Generate Downtime
# ----------------------------------------------------------

def generate_downtime(maintenance_type):

    min_hours, max_hours = downtime_ranges[
        maintenance_type
    ]

    return round(
        rng.uniform(min_hours, max_hours),
        2
    )


# ----------------------------------------------------------
# Generate Maintenance Cost
# ----------------------------------------------------------

def generate_maintenance_cost(
    machine_type,
    maintenance_type
):

    min_cost, max_cost = maintenance_cost_ranges[
        machine_type
    ]

    cost = rng.randint(
        min_cost,
        max_cost
    )

    if maintenance_type == "Emergency":
        cost *= EMERGENCY_COST_MULTIPLIER

    return round(cost, 2)


# ----------------------------------------------------------
# Validate Maintenance Date
# ----------------------------------------------------------

def get_valid_maintenance_date(
    installation_date
):

    maintenance_date = random_maintenance_date()

    while maintenance_date < installation_date:

        maintenance_date = random_maintenance_date()

    return maintenance_date

    # ==========================================================
# Generate One Maintenance Record
# ==========================================================

def generate_maintenance_record():

    # ----------------------------------------------------------
    # Select Machine
    # ----------------------------------------------------------

    machine = rng.choice(machine_records)

    machine_id = machine["machine_id"]
    machine_type = machine["machine_type"]
    factory_id = machine["factory_id"]
    machine_status = machine["status"]
    installation_date = machine["installation_date"]

    # ----------------------------------------------------------
    # Select Maintenance Employee
    # ----------------------------------------------------------

    employee = rng.choice(
        maintenance_employees_by_factory[factory_id]
    )

    employee_id = employee["employee_id"]

    # ----------------------------------------------------------
    # Generate Maintenance Type
    # ----------------------------------------------------------

    maintenance_type = generate_maintenance_type()

    # ----------------------------------------------------------
    # Generate Maintenance Date
    # ----------------------------------------------------------

    maintenance_date = get_valid_maintenance_date(
        installation_date
    )

    # ----------------------------------------------------------
    # Adjust Date Based On Machine Status
    # ----------------------------------------------------------

    if machine_status == "Under Maintenance":

        maintenance_date = END_DATE_OBJ - timedelta(
            days=rng.randint(0, 30)
        )

    elif machine_status == "Retired":

        maintenance_date = END_DATE_OBJ - timedelta(
            days=rng.randint(365, 730)
        )

        while maintenance_date < installation_date:
            maintenance_date = get_valid_maintenance_date(
                installation_date
            )

    # ----------------------------------------------------------
    # Generate Cost & Downtime
    # ----------------------------------------------------------

    maintenance_cost = generate_maintenance_cost(
        machine_type,
        maintenance_type
    )

    downtime_hours = generate_downtime(
        maintenance_type
    )

    # ----------------------------------------------------------
    # Return Record
    # ----------------------------------------------------------

    return {
        "maintenance_date": maintenance_date.date(),
        "machine_id": machine_id,
        "employee_id": employee_id,
        "maintenance_type": maintenance_type,
        "maintenance_cost": maintenance_cost,
        "downtime_hours": downtime_hours
    }

# ==========================================================
# Generator Validation
# ==========================================================

print("\nRunning maintenance generator validation...")

for _ in range(10):

    record = generate_maintenance_record()

    assert record["maintenance_cost"] > 0

    assert record["downtime_hours"] > 0

    assert record["maintenance_date"] >= START_DATE_OBJ.date()

    assert record["maintenance_date"] <= END_DATE_OBJ.date()

print("✓ Maintenance generator validation passed.")

# ==========================================================
# Generate Maintenance Records
# ==========================================================

print("\nGenerating maintenance records...")

maintenance_records = []

# ----------------------------------------------------------
# Ensure Every Machine Has At Least One Record
# ----------------------------------------------------------

for machine in machine_records:

    machine_id = machine["machine_id"]
    machine_type = machine["machine_type"]
    factory_id = machine["factory_id"]
    machine_status = machine["status"]
    installation_date = machine["installation_date"]

    employee = rng.choice(
        maintenance_employees_by_factory[factory_id]
    )

    employee_id = employee["employee_id"]

    maintenance_type = generate_maintenance_type()

    maintenance_date = get_valid_maintenance_date(
        installation_date
    )

    if machine_status == "Under Maintenance":

        maintenance_date = END_DATE_OBJ - timedelta(
            days=rng.randint(0, 30)
        )

    elif machine_status == "Retired":

        maintenance_date = END_DATE_OBJ - timedelta(
            days=rng.randint(365, 730)
        )

        while maintenance_date < installation_date:
            maintenance_date = get_valid_maintenance_date(
                installation_date
            )

    maintenance_cost = generate_maintenance_cost(
        machine_type,
        maintenance_type
    )

    downtime_hours = generate_downtime(
        maintenance_type
    )

    maintenance_records.append({
        "maintenance_date": maintenance_date.date(),
        "machine_id": machine_id,
        "employee_id": employee_id,
        "maintenance_type": maintenance_type,
        "maintenance_cost": maintenance_cost,
        "downtime_hours": downtime_hours
    })

# ----------------------------------------------------------
# Generate Remaining Records
# ----------------------------------------------------------

remaining_records = TOTAL_MAINTENANCE_RECORDS - len(machine_records)

for _ in range(remaining_records):

    maintenance_records.append(
        generate_maintenance_record()
    )

print("✓ Maintenance records generated successfully.")

# ==========================================================
# Create DataFrame
# ==========================================================

maintenance_df = pd.DataFrame(maintenance_records)

# ==========================================================
# Arrange Columns
# ==========================================================

maintenance_df = maintenance_df[
    [
        "maintenance_date",
        "machine_id",
        "employee_id",
        "maintenance_type",
        "maintenance_cost",
        "downtime_hours"
    ]
]

# ==========================================================
# Export CSV
# ==========================================================

OUTPUT_FILE = os.path.join(
    BASE_DATA_PATH,
    "maintenance.csv"
)

maintenance_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ==========================================================
# Execution Summary
# ==========================================================

print("\n" + "=" * 60)
print("MAINTENANCE DATASET GENERATED SUCCESSFULLY")
print("=" * 60)

print(f"Total Maintenance Records : {len(maintenance_df):,}")
print(f"Machines Covered          : {maintenance_df['machine_id'].nunique()}")
print(f"Employees Involved        : {maintenance_df['employee_id'].nunique()}")
print(f"Date Range               : {START_DATE} to {END_DATE}")
print(f"Output File              : {OUTPUT_FILE}")

print("=" * 60)
print("CSV READY FOR MYSQL IMPORT")
print("=" * 60)