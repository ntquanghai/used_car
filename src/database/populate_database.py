import sqlite3
import pandas as pd

final_df = pd.read_parquet("../../data/processed/final_df.parquet")
predicted_df = pd.read_parquet("../../data/processed/predicted_df.parquet")
shap_values_df = pd.read_parquet("../../data/processed/shap_values.parquet")


conn = sqlite3.connect("../../data/database/used_car.db")
final_df.to_sql("vehicles", conn, if_exists="append", index=False)
predicted_df.to_sql("predictions", conn, if_exists="append", index=False)
shap_values_df.to_sql("shap_values", conn, if_exists="append", index=False)

conn.execute("""
    UPDATE predictions 
    SET residual = actual_price - predicted_price, absolute_error = ABS(actual_price - predicted_price);
""")

conn.commit()