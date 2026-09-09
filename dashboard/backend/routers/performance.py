from fastapi import APIRouter
from connect_sqlite import get_connection
import numpy as np
import math

router = APIRouter(prefix = "/performance", tags=["performance"])


# MAE, RMSE and R2 score for the model's predictions on the test set
# Top 100 highest MAE errors
# Quartiles of the MAE errors

@router.get("/")
def get_aggregated_performance():
    conn = get_connection()
    conn.create_function("sqrt", 1, math.sqrt)

    cursor = conn.cursor()

    cursor.execute("""
        WITH 
        price_threshold AS (
            SELECT 1000 AS threshold_value
        ),
        mean_actual_price AS (
            SELECT AVG(actual_price) AS mean_actual_price FROM predictions WHERE actual_price > (SELECT threshold_value FROM price_threshold)
        ),
        all_rows AS (
            SELECT COUNT(*) AS total_count
            FROM predictions
        )
        SELECT
            (SELECT threshold_value FROM price_threshold) AS price_threshold,
            (SELECT total_count FROM all_rows) AS total_count,
            AVG(absolute_error) as mae,
            sqrt(AVG((residual) * (residual))) as rmse,
            1 - (
                SUM(residual * residual) / 
                SUM((actual_price - (SELECT mean_actual_price FROM mean_actual_price)) * (actual_price - (SELECT mean_actual_price FROM mean_actual_price)))
            ) as r2_score,
            COUNT(*) as filtered_count,
            AVG(absolute_error/actual_price)*100 as mean_absolute_percentage_error,
            AVG(CASE WHEN absolute_error <= actual_price*0.05 THEN 1 ELSE 0 END)*100 as accuracy_within_5_percent,
            AVG(CASE WHEN absolute_error <= actual_price*0.10 THEN 1 ELSE 0 END)*100 as accuracy_within_10_percent,
            AVG(CASE WHEN absolute_error <= actual_price*0.20 THEN 1 ELSE 0 END)*100 as accuracy_within_20_percent
        FROM predictions
        WHERE actual_price > (SELECT threshold_value FROM price_threshold)
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

@router.get("/top_errors")
def get_top_errors(limit: int = 100):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT id,
            actual_price,
            predicted_price,
            residual,
            absolute_error
        FROM predictions
        WHERE actual_price > 1000
        ORDER BY absolute_error DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows


@router.get("/error_quartiles")
def get_error_quartiles():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT 
            absolute_error
        FROM predictions
        WHERE actual_price > 1000
    """)
    error_rows = cursor.fetchall()
    errors = [row[0] for row in error_rows]

    q1 = np.percentile(errors, 25)
    median = np.median(errors)
    q3 = np.percentile(errors, 75)
    p90 = np.percentile(errors, 90)
    p95 = np.percentile(errors, 95)


    conn.close()
    return {
        "q1": float(q1),
        "median": float(median),
        "q3": float(q3),
        "p90": float(p90),
        "p95": float(p95)
    }

@router.get("/error_distribution")
def get_error_distribution(bins: int = 10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            CASE
                WHEN absolute_error < 1000 then '$0 - $1.000'
                WHEN absolute_error < 2000 then '$1.000 - $2.000'
                WHEN absolute_error < 5000 then '$2.000 - $5.000'
                WHEN absolute_error < 10000 then '$5.000 - $10.000'
                ELSE '$10.000+'
            END AS error_range,
            COUNT(*) AS frequency
        FROM predictions
        WHERE actual_price > 1000
        GROUP BY error_range
        ORDER BY frequency DESC
        """)
    rows = cursor.fetchall()
    conn.close()
    return rows
