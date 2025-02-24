import sqlite3
import pandas as pd

# Load CSV File
csv_file = "data/stations.csv"
df = pd.read_csv(csv_file)

# Filter Only Required Columns
columns_needed = [
    "Codigo", "Nome", "TipoEstacao", "Longitude", "Latitude",
    "BaciaCodigo", "SubBaciaCodigo", "RioCodigo", "EstadoCodigo", "MunicipioCodigo",
    "ResponsavelCodigo", "ResponsavelUnidade", "ResponsavelJurisdicao",
    "OperadoraCodigo", "OperadoraUnidade", "OperadoraSubUnidade",
    "CodigoAdicional", "Altitude", "AreaDrenagem"
]

# Ensure the CSV has all required columns
df = df[columns_needed]

# Rename Columns to Match SQLite Table
df = df.rename(columns={
    "Codigo": "station_id",
    "Nome": "name",
    "TipoEstacao": "station_type",
    "Longitude": "lon",
    "Latitude": "lat",
    "BaciaCodigo": "basin_id",
    "SubBaciaCodigo": "sub_basin_id",
    "RioCodigo": "river_id",
    "EstadoCodigo": "state_id",
    "MunicipioCodigo": "municipality_id",
    "ResponsavelCodigo": "responsible_id",
    "ResponsavelUnidade": "responsible_unit",
    "ResponsavelJurisdicao": "responsible_jurisdiction",
    "OperadoraCodigo": "operator_id",
    "OperadoraUnidade": "operator_unit",
    "OperadoraSubUnidade": "operator_subunit",
    "CodigoAdicional": "additional_code",
    "Altitude": "altitude",
    "AreaDrenagem": "drainage_area"
})

# Connect to SQLite
conn = sqlite3.connect("data/hydrodata.sqlite")
cursor = conn.cursor()

# Insert Data into SQLite
df.to_sql("stations", conn, if_exists="append", index=False)

print("✅ Stations Data Imported Successfully!")

# Close Connection
conn.close()
