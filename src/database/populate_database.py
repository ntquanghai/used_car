import sqlite3
import pandas as pd

final_df = pd.read_parquet("../../data/processed/final_df.parquet")
predicted_df = pd.read_parquet("../../data/processed/predicted_df.parquet")
shap_values_df = pd.read_parquet("../../data/processed/shap_values.parquet")
