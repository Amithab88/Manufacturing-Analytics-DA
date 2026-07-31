from analytics.production import get_production_batches

df = get_production_batches()

print(df.head())
print()
print("Rows:", len(df))
print("Columns:", len(df.columns))