import pandas

shift_data = [
    {
        "shift_name": "Morning",
        "start_time": "06:00:00",
        "end_time": "14:00:00"
    },
    {
        "shift_name": "Afternoon",
        "start_time": "14:00:00",
        "end_time": "22:00:00"
    },
    {
        "shift_name": "Night",
        "start_time": "22:00:00",
        "end_time": "06:00:00"
    }
]

df = pandas.DataFrame(shift_data)
df.to_csv("C:/Users/AMITHAB/OneDrive/Documents/My Project/manufacturing-analytics/data/raw/shifts.csv", index=False)
print("Shifts dataset generated successfully!")
print(df)