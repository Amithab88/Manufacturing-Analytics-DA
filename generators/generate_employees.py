import pandas as pd
from faker import Faker
import random
from datetime import date

# ==========================================================
# Configuration
# ==========================================================

fake = Faker("en_IN")

CURRENT_YEAR = 2026
TOTAL_EMPLOYEES = 300

# Workforce distribution
designations = {
    "Operator": 180,
    "Technician": 50,
    "Quality Inspector": 30,
    "Supervisor": 20,
    "Maintenance Engineer": 15,
    "Plant Manager": 5
}

# Monthly salary ranges (INR)
salary_ranges = {
    "Operator": (25000, 40000),
    "Technician": (35000, 55000),
    "Quality Inspector": (40000, 60000),
    "Supervisor": (60000, 90000),
    "Maintenance Engineer": (50000, 80000),
    "Plant Manager": (90000, 140000)
}

# Store all generated employees
employee_data = []

# Factory managers (must match the Factories table)
factory_managers = {
    1: "Ira Mane",
    2: "Jai Sankar",
    3: "Yahvi Mitter",
    4: "Warhi Butala",
    5: "Vasatika Bhatt"
}

# ==========================================================
# Generate Plant Managers
# ==========================================================

for factory_id, manager_name in factory_managers.items():

    # Plant managers are experienced employees
    experience = random.randint(15, 25)

    # Hire year derived from experience
    hire_year = CURRENT_YEAR - experience
    hire_month = random.randint(1, 12)
    hire_day = random.randint(1, 28)
    hire_date = date(hire_year, hire_month, hire_day)

    # Salary increases with experience
    base_salary = salary_ranges["Plant Manager"][0]
    salary = base_salary + (experience * 1800) + random.randint(-3000, 3000)

    # Ensure salary stays within the defined range
    salary = min(salary, salary_ranges["Plant Manager"][1])

    employee_data.append({
        "employee_name": manager_name,
        "designation": "Plant Manager",
        "experience_years": experience,
        "salary": salary,
        "hire_date": hire_date,
        "factory_id": factory_id,
        "shift_id": 1
    })

#Workforce genaration for each factory based on the distribution defined above

workforce_distribution = {
    1: {
        "Operator": 48,
        "Technician": 13,
        "Quality Inspector": 8,
        "Maintenance Engineer": 4,
        "Supervisor": 6
    },
    2: {
        "Operator": 41,
        "Technician": 12,
        "Quality Inspector": 7,
        "Maintenance Engineer": 4,
        "Supervisor": 5
    },
    3: {
        "Operator": 36,
        "Technician": 10,
        "Quality Inspector": 6,
        "Maintenance Engineer": 3,
        "Supervisor": 4
    },
    4: {
        "Operator": 31,
        "Technician": 8,
        "Quality Inspector": 5,
        "Maintenance Engineer": 2,
        "Supervisor": 3
    },
    5: {
        "Operator": 24,
        "Technician": 7,
        "Quality Inspector": 4,
        "Maintenance Engineer": 2,
        "Supervisor": 2
    }
}


# Experience range (in years) for each designation
experience_ranges = {
    "Operator": (0, 15),
    "Technician": (2, 18),
    "Quality Inspector": (3, 20),
    "Supervisor": (8, 25),
    "Maintenance Engineer": (5, 20)
}

# Shift allocation based on designation
shift_rules = {
    "Operator": [1, 2, 3],
    "Technician": [1, 2, 3],
    "Quality Inspector": [1, 2, 3],
    "Maintenance Engineer": [1, 2, 3],
    "Supervisor": [1, 2]
}



experience_increment = {
    "Operator": 500,
    "Technician": 700,
    "Quality Inspector": 800,
    "Maintenance Engineer": 1000,
    "Supervisor": 1200,
    "Plant Manager": 1800
}


# ==========================================================
# Function to generate one employee
# ==========================================================

def generate_employee(designation, factory_id):

    # Experience based on designation
    min_exp, max_exp = experience_ranges[designation]
    experience = random.randint(min_exp, max_exp)

    # Hire date derived from experience
    hire_year = CURRENT_YEAR - experience
    hire_month = random.randint(1, 12)
    hire_day = random.randint(1, 28)
    hire_date = date(hire_year, hire_month, hire_day)

    # Salary based on designation and experience
    min_salary, max_salary = salary_ranges[designation]

    salary = (
    min_salary
    + (experience * experience_increment[designation])
    + random.randint(-2000, 2000)
)

    # Salary should never exceed maximum salary
    salary = max(min_salary, min(salary, max_salary))

    # Assign shift according to role
    shift_id = random.choice(shift_rules[designation])

    # Generate employee record
    return {
        "employee_name": fake.name(),
        "designation": designation,
        "experience_years": experience,
        "salary": salary,
        "hire_date": hire_date,
        "factory_id": factory_id,
        "shift_id": shift_id
    }

# ==========================================================
# Generate Remaining Employees
# ==========================================================

for factory_id, roles in workforce_distribution.items():

    for designation, count in roles.items():

        for _ in range(count):

            employee = generate_employee(designation, factory_id)
            employee_data.append(employee)

# ==========================================================
# Create DataFrame
# ==========================================================

df = pd.DataFrame(employee_data)

print(f"Total Employees: {len(df)}")

print("\nEmployees by Designation")
print(df["designation"].value_counts())

print("\nEmployees by Factory")
print(df["factory_id"].value_counts().sort_index())

print("\nFirst 10 Employees")
print(df.head(10))

# ==========================================================
# Export CSV
# ==========================================================

df.to_csv("C:/Users/AMITHAB/OneDrive/Documents/My Project/manufacturing-analytics/data/raw/employees.csv", index=False)

print("\nEmployees dataset exported successfully!")

