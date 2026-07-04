import pandas as pd
import random


products = [
    ("Brake Pad", "Braking System"),
    ("Brake Disc", "Braking System"),
    ("Clutch Plate", "Transmission"),
    ("Gear Shaft", "Transmission"),
    ("Crankshaft", "Engine"),
    ("Engine Valve", "Engine"),
    ("Piston Ring", "Engine"),
    ("Ball Bearing", "Bearings"),
    ("Roller Bearing", "Bearings"),
    ("Steering Knuckle", "Steering"),
    ("Axle Shaft", "Drivetrain"),
    ("Wheel Hub", "Wheels"),
    ("Suspension Arm", "Suspension"),
    ("Control Arm", "Suspension"),
    ("Fuel Injector", "Fuel System"),
    ("Oil Pump", "Engine"),
    ("Flywheel", "Engine"),
    ("Timing Belt", "Engine"),
    ("Chassis Bracket", "Chassis"),
    ("Mounting Plate", "Chassis")
]

cost_ranges = {
    "Bearings": (500, 1200),
    "Braking System": (800, 2000),
    "Transmission": (1500, 3500),
    "Engine": (2000, 4000),
    "Steering": (1200, 2500),
    "Drivetrain": (1500, 3200),
    "Wheels": (1000, 2200),
    "Suspension": (1200, 2800),
    "Fuel System": (1800, 3500),
    "Chassis": (800, 1800)
}

product_data = []

for product_name, category in products:

    min_cost, max_cost = cost_ranges[category]

    unit_cost = random.randint(min_cost, max_cost) #calculates the unit cost of each item according to the category

    profit_margin = random.uniform(0.20, 0.50)   #Profit margin from 20 to 50 percent

    selling_price = round(unit_cost * (1 + profit_margin), 2) #2500*(1+0.20) = 3000

    product_data.append({
        "product_name": product_name,
        "category": category,
        "unit_cost": unit_cost,
        "selling_price": selling_price
    })

    df = pd.DataFrame(product_data)
    df.to_csv("C:/Users/AMITHAB/OneDrive/Documents/My Project/manufacturing-analytics/data/raw/products.csv",index=False)
print("Successfully generated product dataset")
print(df)

