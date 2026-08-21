import sqlite3
import pandas as pd

conn = sqlite3.connect("../../data/database/used_car.db")

# Create the schema for the shap_values table
shap_df = pd.read_parquet("../../data/processed/shap_values.parquet")
shap_schema_content = ""
for column in shap_df.columns:
    if column == "id":
        shap_schema_content += f'"{column}" VARCHAR(50) PRIMARY KEY,\n'
    else:
        shap_schema_content += f'"{column}" REAL,\n'
shap_schema_content += "FOREIGN KEY(id) REFERENCES vehicles(id)"


# Write the schema to a file
with open("schema.sql", "r") as f:
    conn.executescript(f.read())
conn.executescript(f"CREATE TABLE shap_values ({shap_schema_content});")

conn.commit()
conn.close()