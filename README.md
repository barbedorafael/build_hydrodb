# build_hydro_db

## Overview
This repository builds a hydrological database using data from ANA (Agência Nacional de Águas e Saneamento Básico). The system:
- Imports **station metadata** from a CSV file.
- Fetches **time series data** (e.g., discharge, precipitation, water level) via ANA’s API.
- Stores everything in a **SQLite database**.

## Repository Structure
```
build_hydro_db/
│── data/                      # Storage for input/output data
│   ├── stations.csv           # Input CSV with station metadata
│   ├── hydrodata.sqlite       # Output SQLite database
│── sql/                       # SQL scripts for database setup
│   ├── create_tables.sql      # Creates all tables
│   ├── populate_metadata.sql  # Populates metadata tables (methods, status)
│── scripts/                   # Python scripts for processing
│   ├── init_db.py             # Executes SQL scripts to create database structure
│   ├── import_stations.py     # Imports station metadata from CSV to SQLite
│   ├── fetch_timeseries.py    # Fetches time series data from API and stores in SQLite
│── requirements.txt           # Python dependencies
│── README.md                  # Documentation
│── .gitignore                 # Ignore unnecessary files (e.g., `*.sqlite`)

```

## Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/build_hydro_db.git
cd build_hydro_db
```

### 2️⃣ Set Up Python Environment

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3️⃣ Initialize the Database

```sh
python scripts/init_db.py
```

### 4️⃣ Import Station Metadata

```sh
python scripts/import_stations.py
```

### 5️⃣ Fetch Time Series Data

```sh
python scripts/fetch_timeseries.py
```

## Database Structure

### **Tables**

#### 1️⃣ **`stations`** (Station Metadata)

| Column Name | Description |
| --- | --- |
| `station_id` | Primary Key |
| `name` | Station Name |
| `station_type` | Type of Station |
| `longitude` | Geographic Longitude |
| `latitude` | Geographic Latitude |
| `basin_id` | Basin Code |
| `sub_basin_id` | Sub-Basin Code |
| `river_id` | River Code |
| `state_id` | State Code |
| `municipality_id` | Municipality Code |
| `responsible_id` | Responsible Entity |
| `operator_id` | Operator Code |
| `altitude` | Altitude (m) |
| `drainage_area` | Drainage Area (km²) |

#### 2️⃣ **`timeseries`** (Hydrological Data)

| Column Name | Description |
| --- | --- |
| `station_id` | Foreign Key (`stations`) |
| `type_id` | Foreign Key (`methods`) |
| `consistency_id` | Data Consistency Level |
| `date` | Date of Measurement |
| `value` | Measured Value |
| `status` | Data Status |
| `method_id` | Foreign Key (`methods`) |

### Visualize tables in python
```python
import sqlite3
import pandas as pd

# Connect to SQLite
conn = sqlite3.connect("data/hydrodata.sqlite")

# List all tables
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables:\n", tables)

# Choose a table & load sample data
table_name = "timeseries"  # Change to your table name
df = pd.read_sql(f"SELECT * FROM {table_name};", conn)

# Display
df.head()

# Close connection
conn.close()
```

## Notes

* The database uses **foreign keys** for integrity.n
* The `timeseries` table is updated dynamically to **prevent memory issues**.
* API requests can take **a long time**, depending on the number of stations.

## Contributing

To contribute:

1. **Fork the repository**.
2. **Create a new branch** for your changes.
3. **Submit a pull request**.

## License

MIT License
