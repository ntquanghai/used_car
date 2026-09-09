from fastapi import APIRouter
from connect_sqlite import get_connection
import numpy as np

router = APIRouter(prefix = "/stats", tags=["stats"])


# Manufacturer listings
# Manufacturer-based models
# Condition distribution
# Price distribution (Price range, average price, median price and quartiles)
@router.get("/manufacturer")
def get_manufacturer_stats(limit: int = 20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT v.manufacturer, count(*) as count
        FROM vehicles v
        JOIN predictions p
        on v.id = p.id
        GROUP BY manufacturer
        ORDER BY count DESC
        LIMIT {limit}
    """)

    manufacturer_listings = cursor.fetchall()
    conn.close()
    return manufacturer_listings

@router.get(f"/{{manufacturer}}/models")
def get_model_stats(manufacturer: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.model, count(*) as count
        FROM vehicles v
        JOIN predictions p
        ON v.id = p.id
        WHERE manufacturer = ?
        GROUP BY model
        ORDER BY count DESC
    """, (manufacturer,))

    manufacturer_models = cursor.fetchall()
    conn.close()
    return manufacturer_models

@router.get("/condition")
def get_condition_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT COALESCE(v.condition, 'Unknown') AS condition, count(*) as count
        FROM vehicles v
        JOIN predictions p
        ON v.id = p.id
        GROUP BY condition
        ORDER BY CASE condition
            WHEN 'new' THEN 1
            WHEN 'like new' THEN 2
            WHEN 'excellent' THEN 3
            WHEN 'good' THEN 4
            WHEN 'fair' THEN 5
            WHEN 'salvage' THEN 6
            ELSE 7
        END ASC;
    """)

    condition_distribution = cursor.fetchall()
    conn.close()
    return condition_distribution

@router.get("/price")
def get_price_stats():
    conn = get_connection()
    cursor = conn.cursor()

    price_stats = {}

    cursor.execute("""
        SELECT 
            price
        FROM vehicles v
        JOIN predictions p
        ON v.id = p.id
    """)
    price_distribution_rows = cursor.fetchall()
    price_distribution = [row[0] for row in price_distribution_rows]

    q1 = np.percentile(price_distribution, 25)
    median = np.median(price_distribution)
    q3 = np.percentile(price_distribution, 75)
    p05 = np.percentile(price_distribution, 5)
    p90 = np.percentile(price_distribution, 90)
    p95 = np.percentile(price_distribution, 95)

    filtered_prices = [
        p for p in price_distribution
        if p05 <= p <= p95
    ]

    hist, bins = np.histogram(
        filtered_prices,
        bins=30
    )

    price_hist = {
        "bins": bins[:-1].tolist(),
        "counts": hist.tolist(),
        "lower_bound": float(p05),
        "upper_bound": float(p95),
        "n": len(filtered_prices)
    }

    cursor.execute("""
        SELECT 
            MIN(price) as min_price,
            MAX(price) as max_price,
            AVG(price) as avg_price
        FROM vehicles v
        JOIN predictions p
        ON v.id = p.id
    """)

    price_range_stats = cursor.fetchall()
    conn.close()

    price_stats["min_price"] = price_range_stats[0]["min_price"]
    price_stats["max_price"] = price_range_stats[0]["max_price"]
    price_stats["avg_price"] = price_range_stats[0]["avg_price"]
    price_stats["median"] = float(median)
    price_stats["q1"] = float(q1)
    price_stats["q3"] = float(q3)   
    price_stats["p05"] = float(p05)
    price_stats["p90"] = float(p90)
    price_stats["p95"] = float(p95)

    return price_hist, price_stats


