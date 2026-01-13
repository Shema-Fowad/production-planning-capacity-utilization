import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)

# -----------------------------
# CONFIG
# -----------------------------
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 6, 30)
dates = pd.date_range(start_date, end_date, freq="D")

# -----------------------------
# PLANTS
# -----------------------------
plants = pd.DataFrame([
    {"plant_id": "P1", "plant_name": "Punjab Textile Unit", "location": "Punjab", "product_focus": "Bath Linen", "operational_status": "Active"},
    {"plant_id": "P2", "plant_name": "MP Textile Unit", "location": "Madhya Pradesh", "product_focus": "Bed Linen", "operational_status": "Active"}
])

# -----------------------------
# PRODUCTION LINES
# -----------------------------
production_lines = pd.DataFrame([
    {"line_id": "L1", "plant_id": "P1", "line_type": "Bath Linen", "max_units_per_hour": 120, "setup_time_minutes": 45, "is_bottleneck_prone": True},
    {"line_id": "L2", "plant_id": "P1", "line_type": "Bath Linen", "max_units_per_hour": 100, "setup_time_minutes": 30, "is_bottleneck_prone": False},
    {"line_id": "L3", "plant_id": "P1", "line_type": "Yarn", "max_units_per_hour": 80, "setup_time_minutes": 60, "is_bottleneck_prone": True},
    {"line_id": "L4", "plant_id": "P2", "line_type": "Bed Linen", "max_units_per_hour": 110, "setup_time_minutes": 40, "is_bottleneck_prone": False},
    {"line_id": "L5", "plant_id": "P2", "line_type": "Bed Linen", "max_units_per_hour": 95, "setup_time_minutes": 35, "is_bottleneck_prone": False},
    {"line_id": "L6", "plant_id": "P2", "line_type": "Yarn", "max_units_per_hour": 75, "setup_time_minutes": 55, "is_bottleneck_prone": True}
])

# -----------------------------
# SHIFTS
# -----------------------------
shifts = pd.DataFrame([
    {"shift_id": "S1", "shift_name": "Morning", "start_time": "06:00", "end_time": "14:00", "planned_hours": 8, "labor_cost_per_hour": 220},
    {"shift_id": "S2", "shift_name": "Evening", "start_time": "14:00", "end_time": "22:00", "planned_hours": 8, "labor_cost_per_hour": 230},
    {"shift_id": "S3", "shift_name": "Night", "start_time": "22:00", "end_time": "06:00", "planned_hours": 8, "labor_cost_per_hour": 250}
])

# -----------------------------
# PRODUCTS
# -----------------------------
products = pd.DataFrame([
    {"product_id": "PR1", "product_category": "Towel", "gsm": 450, "standard_minutes_per_unit": 0.45, "selling_price": 280},
    {"product_id": "PR2", "product_category": "Towel", "gsm": 550, "standard_minutes_per_unit": 0.55, "selling_price": 340},
    {"product_id": "PR3", "product_category": "Bedsheet", "gsm": 180, "standard_minutes_per_unit": 0.65, "selling_price": 620},
    {"product_id": "PR4", "product_category": "Bedsheet", "gsm": 220, "standard_minutes_per_unit": 0.75, "selling_price": 720},
    {"product_id": "PR5", "product_category": "Yarn", "gsm": 0, "standard_minutes_per_unit": 0.90, "selling_price": 210}
])

# -----------------------------
# PRODUCTION CALENDAR
# -----------------------------
calendar_rows = []
for d in dates:
    for plant in plants["plant_id"]:
        is_working = d.weekday() < 6  # Sunday off
        calendar_rows.append({
            "date": d.date(),
            "plant_id": plant,
            "is_working_day": is_working,
            "planned_shifts": 3 if is_working else 0,
            "planned_hours": 24 if is_working else 0
        })

production_calendar = pd.DataFrame(calendar_rows)

# -----------------------------
# ORDERS
# -----------------------------
orders = []
for i in range(1200):
    order_date = start_date + timedelta(days=random.randint(0, 150))
    orders.append({
        "order_id": f"O{i+1}",
        "product_id": random.choice(products["product_id"].tolist()),
        "order_quantity": random.randint(500, 5000),
        "due_date": (order_date + timedelta(days=random.randint(7, 30))).date(),
        "priority_level": random.choices(["High", "Medium", "Low"], weights=[0.25, 0.5, 0.25])[0],
        "customer_type": random.choice(["Export", "Domestic"])
    })

orders = pd.DataFrame(orders)

# -----------------------------
# PRODUCTION RUNS
# -----------------------------
runs = []
run_id = 1

for d in dates:
    for _, line in production_lines.iterrows():
        if d.weekday() == 6:
            continue

        for _, shift in shifts.iterrows():
            base_hours = shift["planned_hours"]
            efficiency = np.random.normal(0.88, 0.05)
            if shift["shift_name"] == "Night":
                efficiency -= 0.05

            downtime = random.randint(10, 60) if line["is_bottleneck_prone"] else random.randint(0, 30)
            effective_hours = max(base_hours - downtime / 60, 4)

            max_units = line["max_units_per_hour"] * effective_hours
            planned_units = int(max_units * efficiency)
            actual_units = int(planned_units * np.random.uniform(0.95, 1.0))
            scrap_units = int(actual_units * np.random.uniform(0.01, 0.04))

            runs.append({
                "run_id": f"R{run_id}",
                "date": d.date(),
                "plant_id": line["plant_id"],
                "line_id": line["line_id"],
                "shift_id": shift["shift_id"],
                "product_id": random.choice(products["product_id"].tolist()),
                "planned_units": planned_units,
                "actual_units": actual_units,
                "run_hours": round(effective_hours, 2),
                "downtime_minutes": downtime,
                "scrap_units": scrap_units
            })
            run_id += 1

production_runs = pd.DataFrame(runs)

# -----------------------------
# MAINTENANCE LOGS
# -----------------------------
maintenance_logs = []
for _, line in production_lines.iterrows():
    for _ in range(12):
        maintenance_logs.append({
            "maintenance_id": f"M{random.randint(1000,9999)}",
            "line_id": line["line_id"],
            "date": (start_date + timedelta(days=random.randint(0, 180))).date(),
            "downtime_minutes": random.randint(60, 240),
            "maintenance_type": random.choice(["Planned", "Breakdown"]),
            "root_cause": random.choice(["Mechanical", "Electrical", "Wear & Tear"])
        })

maintenance_logs = pd.DataFrame(maintenance_logs)

# -----------------------------
# SAVE FILES
# -----------------------------
plants.to_csv("plants.csv", index=False)
production_lines.to_csv("production_lines.csv", index=False)
shifts.to_csv("shifts.csv", index=False)
products.to_csv("products.csv", index=False)
production_calendar.to_csv("production_calendar.csv", index=False)
orders.to_csv("orders.csv", index=False)
production_runs.to_csv("production_runs.csv", index=False)
maintenance_logs.to_csv("maintenance_logs.csv", index=False)

print("✅ Realistic operations dataset generated successfully.")
