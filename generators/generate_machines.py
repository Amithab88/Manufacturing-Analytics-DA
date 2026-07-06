import pandas as pd
import random
from datetime import date, timedelta

# ==========================================================
# Configuration
# ==========================================================

CURRENT_YEAR = 2026
TOTAL_MACHINES = 100

# ==========================================================
# Factory Distribution
# ==========================================================

factory_distribution = {
    1: 28,   # Chennai
    2: 24,   # Hosur
    3: 20,   # Bengaluru
    4: 16,   # Pune
    5: 12    # Ahmedabad
}

# ==========================================================
# Machine Type Distribution
# ==========================================================

machine_type_distribution = {
    "CNC Machine": 25,
    "Assembly Robot": 20,
    "Injection Molding Machine": 15,
    "Laser Cutter": 12,
    "Hydraulic Press": 10,
    "Packaging Machine": 10,
    "Conveyor System": 8
}

# ==========================================================
# Machine Name Prefixes
# ==========================================================

machine_prefix = {
    "CNC Machine": "CNC",
    "Assembly Robot": "ROB",
    "Injection Molding Machine": "INJ",
    "Laser Cutter": "LAS",
    "Hydraulic Press": "HYD",
    "Packaging Machine": "PKG",
    "Conveyor System": "CON"
}

# ==========================================================
# Factory-wise Machine Allocation Matrix
# ==========================================================

factory_machine_matrix = {

    1: {
        "CNC Machine": 8,
        "Assembly Robot": 6,
        "Injection Molding Machine": 4,
        "Laser Cutter": 4,
        "Hydraulic Press": 3,
        "Packaging Machine": 2,
        "Conveyor System": 1
    },

    2: {
        "CNC Machine": 6,
        "Assembly Robot": 5,
        "Injection Molding Machine": 4,
        "Laser Cutter": 3,
        "Hydraulic Press": 2,
        "Packaging Machine": 2,
        "Conveyor System": 2
    },

    3: {
        "CNC Machine": 5,
        "Assembly Robot": 4,
        "Injection Molding Machine": 3,
        "Laser Cutter": 2,
        "Hydraulic Press": 2,
        "Packaging Machine": 2,
        "Conveyor System": 2
    },

    4: {
        "CNC Machine": 4,
        "Assembly Robot": 3,
        "Injection Molding Machine": 2,
        "Laser Cutter": 2,
        "Hydraulic Press": 2,
        "Packaging Machine": 2,
        "Conveyor System": 1
    },

    5: {
        "CNC Machine": 2,
        "Assembly Robot": 2,
        "Injection Molding Machine": 2,
        "Laser Cutter": 1,
        "Hydraulic Press": 1,
        "Packaging Machine": 2,
        "Conveyor System": 2
    }
}

# ==========================================================
# Factory-wise Status Allocation
# (Ensures realistic analytics across factories)
# ==========================================================

factory_status_matrix = {

    1: {
        "Running": 23,
        "Idle": 3,
        "Under Maintenance": 2,
        "Retired": 0
    },

    2: {
        "Running": 20,
        "Idle": 2,
        "Under Maintenance": 2,
        "Retired": 0
    },

    3: {
        "Running": 17,
        "Idle": 2,
        "Under Maintenance": 1,
        "Retired": 0
    },

    4: {
        "Running": 13,
        "Idle": 2,
        "Under Maintenance": 1,
        "Retired": 0
    },

    5: {
        "Running": 9,
        "Idle": 1,
        "Under Maintenance": 0,
        "Retired": 2
    }

}

# ==========================================================
# Machine Name Counters
# ==========================================================

machine_counter = {
    machine_type: 1
    for machine_type in machine_type_distribution
}

# ==========================================================
# Store Generated Machines
# ==========================================================

machine_data = []

# ==========================================================
# Helper Functions
# ==========================================================

def random_installation_date(status):
    """
    Generate installation date based on machine status.
    """

    if status == "Running":
        year = random.randint(2015, 2025)

    elif status == "Idle":
        year = random.randint(2012, 2022)

    elif status == "Under Maintenance":
        year = random.randint(2012, 2025)

    else:  # Retired
        year = random.randint(2012, 2016)

    month = random.randint(1, 12)
    day = random.randint(1, 28)

    return date(year, month, day)


def random_service_date(status, installation_date):
    """
    Generate last service date based on machine status.
    """

    today = date(CURRENT_YEAR, 1, 1)

    if status == "Running":
        days_back = random.randint(30, 180)

    elif status == "Idle":
        days_back = random.randint(90, 365)

    elif status == "Under Maintenance":
        days_back = random.randint(0, 30)

    else:  # Retired
        days_back = random.randint(365, 1095)

    service_date = today - timedelta(days=days_back)

    if service_date < installation_date:
        service_date = installation_date

    return service_date

# ==========================================================
# Generate One Machine
# ==========================================================

def generate_machine(factory_id, machine_type, status):

    prefix = machine_prefix[machine_type]
    machine_number = machine_counter[machine_type]

    machine_name = f"{prefix}-{machine_number:03d}"

    # Increment counter for next machine
    machine_counter[machine_type] += 1

    # Generate dates
    installation_date = random_installation_date(status)
    last_service_date = random_service_date(status, installation_date)

    return {
        "machine_name": machine_name,
        "machine_type": machine_type,
        "installation_date": installation_date,
        "status": status,
        "last_service_date": last_service_date,
        "factory_id": factory_id
    }


# ==========================================================
# Generate Machines
# ==========================================================

for factory_id in sorted(factory_machine_matrix.keys()):

    # ------------------------------------------------------
    # Build Factory Status Pool
    # ------------------------------------------------------

    factory_status_pool = []

    for status, count in factory_status_matrix[factory_id].items():
        factory_status_pool.extend([status] * count)

    # Shuffle to avoid assigning the same status
    # to one machine type repeatedly.
    random.shuffle(factory_status_pool)

    status_index = 0

    # ------------------------------------------------------
    # Generate Machines by Machine Type
    # ------------------------------------------------------

    for machine_type, quantity in factory_machine_matrix[factory_id].items():

        for _ in range(quantity):

            status = factory_status_pool[status_index]
            status_index += 1

            machine = generate_machine(
                factory_id=factory_id,
                machine_type=machine_type,
                status=status
            )

            machine_data.append(machine)

# ==========================================================
# Validation
# ==========================================================

print("=" * 60)
print("VALIDATING GENERATED MACHINE DATA")
print("=" * 60)

# ----------------------------------------------------------
# Total Machines
# ----------------------------------------------------------

assert len(machine_data) == TOTAL_MACHINES

print(f"✓ Total Machines : {len(machine_data)}")

# ----------------------------------------------------------
# Create DataFrame
# ----------------------------------------------------------

df = pd.DataFrame(machine_data)

# ----------------------------------------------------------
# Validate Factory Distribution
# ----------------------------------------------------------

print("\nFactory Distribution")

factory_counts = (
    df["factory_id"]
    .value_counts()
    .sort_index()
)

print(factory_counts)

for factory_id, expected_count in factory_distribution.items():

    actual_count = factory_counts[factory_id]

    assert actual_count == expected_count

print("✓ Factory distribution validated")

# ----------------------------------------------------------
# Validate Machine Type Distribution
# ----------------------------------------------------------

print("\nMachine Type Distribution")

type_counts = df["machine_type"].value_counts()

print(type_counts)

for machine_type, expected_count in machine_type_distribution.items():

    actual_count = type_counts[machine_type]

    assert actual_count == expected_count

print("✓ Machine type distribution validated")

# ----------------------------------------------------------
# Validate Status Distribution
# ----------------------------------------------------------

print("\nMachine Status Distribution")

status_counts = df["status"].value_counts()

print(status_counts)

expected_status_counts = {
    "Running": 82,
    "Idle": 10,
    "Under Maintenance": 6,
    "Retired": 2
}

for status, expected_count in expected_status_counts.items():

    actual_count = status_counts[status]

    assert actual_count == expected_count

print("✓ Status distribution validated")

# ----------------------------------------------------------
# Validate Duplicate Machine Names
# ----------------------------------------------------------

duplicates = df["machine_name"].duplicated().sum()

assert duplicates == 0

print("✓ Machine names are unique")

# ----------------------------------------------------------
# Validate Service Dates
# ----------------------------------------------------------

invalid_dates = (
    df["last_service_date"] <
    df["installation_date"]
).sum()

assert invalid_dates == 0

print("✓ Service dates validated")

print("=" * 60)
print("ALL VALIDATIONS PASSED")
print("=" * 60)