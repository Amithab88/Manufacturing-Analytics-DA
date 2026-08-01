from analytics.trends import TrendAnalytics

print("Daily Production")
print(TrendAnalytics.daily_production())

print("\nMonthly Production")
print(TrendAnalytics.monthly_production())

print("\nDaily Defect Rate")
print(TrendAnalytics.daily_defect_rate())

print("\nMonthly Defect Rate")
print(TrendAnalytics.monthly_defect_rate())

print("\nProduction Hours Trend")
print(TrendAnalytics.production_hours_trend())