import sqlite3
from fastapi import FastAPI

DB_PATH = "../../data/database/used_car.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn