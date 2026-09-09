from unittest import result

from fastapi import APIRouter
from connect_sqlite import get_connection

router = APIRouter(prefix = "/shap_values", tags=["shap_values"])

# Get aggregate SHAP values for all features

@router.get("/")
def get_aggregate_shap_values(limit: int = 20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info(shap_values)")
    columns = [column[1] for column in cursor.fetchall()]
    columns.remove("id")  # Remove the 'id' column from the list of columns
    
    query = ""
    for col in columns:
        query += f'AVG(ABS("{col}")) AS "avg_abs_{col}",\n'
    query = query.strip().rstrip(",")  # Remove trailing comma and whitespace
    
    cursor.execute(f"""
        SELECT {query}
        FROM shap_values
    """)
    result = cursor.fetchall()
    conn.close()

    result = dict(result[0])
    shap_values = [
        {
            "feature": col,
            "importance": result[f"avg_abs_{col}"]
        }
        for col in columns
    ]

    shap_values = sorted(
        shap_values,
        key=lambda x: x["importance"],
        reverse=True,
    )

    shap_values = shap_values[:limit]  # Limit the number of features returned
    print(shap_values)

    return shap_values

@router.get("/{vehicle_id}")
def get_vehicle_shap_values(vehicle_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM shap_values WHERE id = ?", (vehicle_id,))
    row = cursor.fetchone()
    conn.close()
    return row