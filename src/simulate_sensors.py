import random
import csv
from datetime import datetime, timedelta
import os

SRC_FOLDER = os.path.dirname(__file__)  # path to src/
PROJECT_ROOT = os.path.dirname(SRC_FOLDER)  # one level up, project root

OUTPUT_CSV = os.path.join(PROJECT_ROOT, "data", "simulated_sensor_data.csv")

def random_timestamp(start: datetime, end: datetime):
    """Generate a random timestamp between start and end dates."""
    delta = end - start
    rand_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=rand_seconds)

def simulate_record(farm_id: int, ts: datetime):
    """Return one simulated soil + weather record."""
    return {
        "timestamp": ts.isoformat(),
        "farm_id": farm_id,
        "N": round(random.uniform(10, 140), 2),  # Nitrogen
        "P": round(random.uniform(5, 145), 2),   # Phosphorus
        "K": round(random.uniform(5, 205), 2),   # Potassium
        "pH": round(random.uniform(4.5, 8.5), 2),
        "temperature_C": round(random.uniform(15, 40), 2),
        "humidity_percent": round(random.uniform(30, 100), 2),
        "soil_moisture_percent": round(random.uniform(10, 60), 2),
        "rainfall_mm": round(random.uniform(0, 300), 2)
    }

def generate_dataset(num_records=1000, num_farms=3):
    """Generate dataset of simulated sensor readings."""
    start = datetime.now() - timedelta(days=30)
    end = datetime.now()

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    fieldnames = [
        "timestamp", "farm_id", "N", "P", "K", "pH",
        "temperature_C", "humidity_percent",
        "soil_moisture_percent", "rainfall_mm"
    ]

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(num_records):
            ts = random_timestamp(start, end)
            farm_id = random.randint(1, num_farms)
            writer.writerow(simulate_record(farm_id, ts))

    print(f"✅ Generated {num_records} records for {num_farms} farms → {OUTPUT_CSV}")

if __name__ == "__main__":
    generate_dataset(num_records=1000, num_farms=3)