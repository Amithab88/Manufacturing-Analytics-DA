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
# Random number generator
rng = random.Random(42)

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


# ----------------------------------------------------------
# Convert Installation Date
# ----------------------------------------------------------

machines_df["installation_date"] = pd.to_datetime(
    machines_df["installation_date"]
)

# ----------------------------------------------------------
# Eligible Employees
# ----------------------------------------------------------

eligible_designations = [
    "Operator"
]

eligible_employees = employees_df[
    employees_df["designation"].isin(eligible_designations)
].copy()

# ----------------------------------------------------------
# Eligible Machines
# ----------------------------------------------------------

eligible_machine_types = [
    "CNC Machine",
    "Assembly Robot",
    "Injection Molding Machine",
    "Laser Cutter",
    "Hydraulic Press",
    "Packaging Machine"
]

eligible_machines = machines_df[
    (machines_df["machine_type"].isin(eligible_machine_types))
    &
    (machines_df["status"] != "Retired")
].copy()

# ----------------------------------------------------------
# Build Employee Lookup by Factory
# ----------------------------------------------------------

employees_by_factory = {}

for factory_id, group in eligible_employees.groupby("factory_id"):
    employees_by_factory[factory_id] = group.to_dict("records")

# ----------------------------------------------------------
# Machine → Product Category Mapping
# ----------------------------------------------------------

machine_product_categories = {
    "CNC Machine": [
        "Engine",
        "Transmission",
        "Steering",
        "Drivetrain"
    ],

    "Assembly Robot": [
        "Braking System",
        "Suspension",
        "Wheels"
    ],

    "Injection Molding Machine": [
        "Fuel System"
    ],

    "Laser Cutter": [
        "Engine",
        "Transmission",
        "Braking System"
    ],

    "Hydraulic Press": [
        "Suspension",
        "Steering",
        "Drivetrain"
    ],

    "Packaging Machine": list(products_df["category"].unique())
}

# ----------------------------------------------------------
# Build Product Lookup by Category
# ----------------------------------------------------------

products_by_category = {}

for category, group in products_df.groupby("category"):
    products_by_category[category] = group.to_dict("records")

# ----------------------------------------------------------
# Verify Product Categories
# ----------------------------------------------------------

missing_categories = []

for categories in machine_product_categories.values():
    for category in categories:
        if category not in products_by_category:
            missing_categories.append(category)

if missing_categories:
    raise ValueError(
        f"Missing product categories: {sorted(set(missing_categories))}"
    )
print("✓ Product compatibility validated successfully.")

# ==========================================================
# Build Compatible Product Lookup
# ==========================================================

compatible_products = {}

for machine_type, categories in machine_product_categories.items():

    compatible_products[machine_type] = []

    for category in categories:

        compatible_products[machine_type].extend(
            products_by_category[category]
        )

# Verify every machine type has at least one compatible product
for machine_type, products in compatible_products.items():

    if len(products) == 0:
        raise ValueError(
            f"No compatible products found for {machine_type}"
        )

print("✓ Compatible product lookup created successfully.")

# ----------------------------------------------------------
# Cache Machine Records
# ----------------------------------------------------------

eligible_machine_records = eligible_machines.to_dict("records")
print("✓ Machine lookup cache created successfully.")

# ==========================================================
# Business Rules
# ==========================================================

# Units produced per batch by machine type
units_range = {
    "CNC Machine": (40, 120),
    "Assembly Robot": (150, 450),
    "Injection Molding Machine": (300, 900),
    "Laser Cutter": (60, 200),
    "Hydraulic Press": (100, 350),
    "Packaging Machine": (500, 1800)
}

# Maximum production hours allowed for one batch
MAX_BATCH_HOURS = 8.0

# Base defect rate (%) by machine type
base_defect_rate = {
    "CNC Machine": 1.2,
    "Assembly Robot": 0.8,
    "Injection Molding Machine": 1.5,
    "Laser Cutter": 1.0,
    "Hydraulic Press": 1.8,
    "Packaging Machine": 0.5
}

print("✓ Business rules loaded successfully.")

# ==========================================================
# Helper Functions
# ==========================================================

START_DATE_OBJ = datetime.strptime(START_DATE, "%Y-%m-%d")
END_DATE_OBJ = datetime.strptime(END_DATE, "%Y-%m-%d")


def random_production_date():
    """
    Generate a random production date within the configured date range.
    """
    total_days = (END_DATE_OBJ - START_DATE_OBJ).days
    random_days = rng.randint(0, total_days)
    return START_DATE_OBJ + timedelta(days=random_days)


def calculate_machine_age(installation_date, production_date):
    """
    Calculate machine age in years at the time of production.
    """
    return (production_date - installation_date).days / 365.25


def generate_units(machine_type):
    """
    Generate realistic units produced based on machine type.
    """
    minimum, maximum = units_range[machine_type]
    return rng.randint(minimum, maximum)


def generate_production_hours():
    """
    Generate production hours between 1 and 8.
    """
    return round(rng.uniform(1.0, MAX_BATCH_HOURS), 2)

# ==========================================================
# Defect Rate Calculation
# ==========================================================

def calculate_defect_rate(machine_type, machine_age, experience_years):
    """
    Returns a realistic defect percentage.

    Rules:
    - Most batches: 0–2%
    - Older machines increase defects
    - Experienced operators reduce defects
    - Maximum defect rate capped at 8%
    """

    # Base defect rate by machine type
    defect_rate = base_defect_rate[machine_type]

    # -----------------------------
    # Machine age effect
    # -----------------------------
    if machine_age >= 12:
        defect_rate += 1.2
    elif machine_age >= 8:
        defect_rate += 0.8
    elif machine_age >= 5:
        defect_rate += 0.4

    # -----------------------------
    # Employee experience effect
    # -----------------------------
    if experience_years >= 15:
        defect_rate -= 0.60
    elif experience_years >= 10:
        defect_rate -= 0.40
    elif experience_years >= 5:
        defect_rate -= 0.20

    # -----------------------------
    # Natural batch variation
    # (Right-skewed distribution)
    # -----------------------------
    defect_rate += rng.triangular(-0.25, 2.5, 0.15)

    # Clamp between 0 and 8%
    defect_rate = max(0.0, min(defect_rate, 8.0))

    return round(defect_rate, 2)


def calculate_defective_units(units_produced, defect_rate):
    """
    Calculate defective units from defect percentage.
    """

    defective_units = round(
        units_produced * defect_rate / 100
    )

    return min(defective_units, units_produced)
# ==========================================================
# Generate One Production Batch
# ==========================================================

def generate_batch():

    # ---------------------------------------------
    # Select Machine
    # ---------------------------------------------

    machine = rng.choice(eligible_machine_records)

    machine_id = machine["machine_id"]
    machine_type = machine["machine_type"]
    factory_id = machine["factory_id"]
    installation_date = machine["installation_date"]

    # ---------------------------------------------
    # Select Employee (Same Factory)
    # ---------------------------------------------

    employee = rng.choice(
        employees_by_factory[factory_id]
    )

    employee_id = employee["employee_id"]
    shift_id = employee["shift_id"]
    experience_years = employee["experience_years"]

    # ---------------------------------------------
    # Select Compatible Product
    # ---------------------------------------------

    product = rng.choice(
        compatible_products[machine_type]
    )

    product_id = product["product_id"]

    # ---------------------------------------------
    # Production Date
    # ---------------------------------------------

    production_date = random_production_date()

    # Machine must exist before production
    while production_date < installation_date:
        production_date = random_production_date()

    # ---------------------------------------------
    # Production Metrics
    # ---------------------------------------------

    machine_age = calculate_machine_age(
        installation_date,
        production_date
    )

    units_produced = generate_units(machine_type)

    production_hours = generate_production_hours()

    defect_rate = calculate_defect_rate(
        machine_type,
        machine_age,
        experience_years
    )

    defective_units = calculate_defective_units(
        units_produced,
        defect_rate
    )

    # ---------------------------------------------
    # Return Batch
    # ---------------------------------------------

    return {
        "production_date": production_date.date(),
        "machine_id": machine_id,
        "employee_id": employee_id,
        "product_id": product_id,
        "shift_id": shift_id,
        "units_produced": units_produced,
        "defective_units": defective_units,
        "production_hours": production_hours
    }

# ==========================================================
# Generator Validation
# ==========================================================

print("\nRunning generator validation...")

for i in range(10):

    batch = generate_batch()

    assert batch["units_produced"] >= batch["defective_units"]

    assert batch["production_hours"] <= MAX_BATCH_HOURS

    assert batch["production_hours"] > 0

print("✓ Generator validation passed.")

# ==========================================================
# Generate Production Batches
# ==========================================================

print("\nGenerating production batches...")

production_batches = []

for _ in range(TOTAL_BATCHES):

    production_batches.append(
        generate_batch()
    )

print("✓ Batch generation completed.")

# ==========================================================
# Convert to DataFrame
# ==========================================================

production_df = pd.DataFrame(production_batches)

# ==========================================================
# Arrange Columns
# ==========================================================

production_df = production_df[
    [
        "production_date",
        "machine_id",
        "employee_id",
        "product_id",
        "shift_id",
        "units_produced",
        "defective_units",
        "production_hours"
    ]
]

# ==========================================================
# Export CSV
# ==========================================================

output_file = os.path.join(
    BASE_DATA_PATH,
    "production_batches.csv"
)

production_df.to_csv(
    output_file,
    index=False
)

# ==========================================================
# Final Summary
# ==========================================================

print("\n" + "=" * 60)
print("PRODUCTION BATCH GENERATION COMPLETED")
print("=" * 60)

print(f"Total Batches Generated : {len(production_df):,}")
print(f"Machines Used           : {production_df['machine_id'].nunique()}")
print(f"Employees Used          : {production_df['employee_id'].nunique()}")
print(f"Products Produced       : {production_df['product_id'].nunique()}")
print(f"Date Range              : {START_DATE} to {END_DATE}")
print(f"Output File             : {output_file}")

print("=" * 60)
print("CSV READY FOR MYSQL IMPORT")
print("=" * 60)