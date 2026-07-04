import pandas as pd
import random
from faker import Faker
from datetime import date

fake = Faker("en_IN")

factories = [
    ("Chennai Manufacturing Plant","Chennai, Tamil nadu"),
    ("Hosur Manufacturing Plant","Hosur, Tamil nadu"),
    ("Bengaluru Manufacturing Plant","Bengaluru, Karnataka"),
    ("Pune Manufacturing Plant","Pune, Maharashtra"),
    ("Ahmedabad Manufacturing Plant","Ahmedabad, Gujarat")

]

factory_data = []

for factory_name, location in factories:  #loops the factories data

    manager_name = fake.name()            #Generates indian name

    year = random.randint(1995, 2018)     #Using random function enters year-month-day
    month = random.randint(1, 12)         #Using random function enters year-month-day
    day = random.randint(1, 28)           #Using random function enters year-month-day

    established_date = date(year, month, day)     #Creates date object "YYYY-MM-DD"

    factory_data.append({                 #Adds the complete data into the list
        "factory_name": factory_name,
        "location": location,
        "manager_name": manager_name,
        "established_date": established_date
    })

df = pd.DataFrame(factory_data)
df.to_csv("C:/Users/AMITHAB/OneDrive/Documents/My Project/manufacturing-analytics/data/raw/factories.csv", index=False)
print("Factories dataset generated successfully!")
print(df)