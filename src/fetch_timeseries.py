import pandas as pd
import requests
import xml.etree.ElementTree as ET
import sqlite3

# 🔹 SQLite Database File
db_file = "data/hydrodata.sqlite"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Load Station Numbers from SQLite (Instead of CSV)
cursor.execute("SELECT station_id FROM stations;")
station_codes = [row[0] for row in cursor.fetchall()]

# Define Base URL
base_url = "http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica"

# Function to Parse XML and Insert into SQLite
def parse_and_insert(response_text, station, tipo_dados, nivel_consistencia):
    root = ET.fromstring(response_text)
    parser = root.findall(".//SerieHistorica")

    if not parser:
        return  # Skip if no data

    prefix_dict = {1: "Cota",
                   2: "Chuva",
                   3: "Vazao"}
    prefix = prefix_dict[tipo_dados]

    print(f"Processing station {station} - Type: {tipo_dados}, Consistency: {nivel_consistencia}")
    records = []
    for serie in parser:
        # Extract Year and Month from DataHora
        base_date = pd.to_datetime(serie.findtext("DataHora"))
        year, month = base_date.year, base_date.month

        # Detect Method Field Dynamically
        for elem in serie:
            if "Metodo" in elem.tag or "Tipo" in elem.tag:
                method = elem.text
                break  

        # Loop Through Daily Values
        for day in range(1, 32):
            value = serie.findtext(f"{prefix}{day:02}")
            status = serie.findtext(f"{prefix}{day:02}Status")

            if value:
                records.append((station, tipo_dados, nivel_consistencia,
                                f"{year}-{month:02d}-{day:02d}", value, status, method))
    
    # Sort records by date before inserting
    records.sort(key=lambda x: x[3])  # Sorting by 'date' column (index 3)
    print(f"Period of Records: {records[0][3]} to {records[-1][3]}")
    
    # Insert Records in Bulk to SQLite
    with conn:
        conn.executemany("""
            INSERT OR IGNORE INTO timeseries (station_id, type_id, consistency_id, date, value, status, method_id)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, records)

# 🔹 Fetch and Process Data for Each Station
for station in station_codes:
    for tipo_dados in [1, 2, 3]:  # Iterate Over Types
        for nivel_consistencia in [1, 2]:  # Iterate Over Consistency Levels
            params = {
                "codEstacao": str(station),
                "dataInicio": "01/01/1900",
                "dataFim": "",
                "tipoDados": str(tipo_dados),
                "nivelConsistencia": str(nivel_consistencia)
            }

            try:
                response = requests.get(base_url, params=params)
                
                if response.status_code == 200:
                    parse_and_insert(response.text, station, tipo_dados, nivel_consistencia)
                else:
                    print(f"Failed for station {station} - Tipo: {tipo_dados}, Consistency: {nivel_consistencia} - Status Code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"Request error for station {station}: {e}")

# Close SQLite Connection
conn.close()
