from fastapi import APIRouter
from connect_sqlite import get_connection
import math

router = APIRouter(prefix = "/vehicles", tags=["vehicles"])

@router.get("/")
def get_vehicles(
    limit: int = 25,
    page: int = 1,
    search: str = None,
    sort_by: str = "id",
):
    conn = get_connection()
    conn.create_function("ceil", 1, math.ceil)
    cursor = conn.cursor()

    allowed_sort_columns = {
        "v.id",
        "manufacturer",
        "model",
        "year",
        "price",
        "odometer",
        "condition"
    }

    original_query = """
        SELECT 
            v.id, manufacturer, model, price, predicted_price, 
            absolute_error, condition, vehicle_age, odometer, fuel, transmission, drive,
            title_status, state, miles_per_year
        FROM vehicles v
        JOIN predictions p
        ON v.id = p.id
    """

    if sort_by not in allowed_sort_columns:
        sort_by = "v.id"

    if search:
        cursor.execute(f"""
        {original_query}
        WHERE model LIKE ? 
        OR manufacturer LIKE ? 
        OR cylinders LIKE ? 
        OR fuel LIKE ? 
        OR condition LIKE ? 
        ORDER BY {sort_by} 
        LIMIT ?
        OFFSET ?
    """, (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%", limit, (page - 1) * limit))
    else:
        cursor.execute(f"""
            {original_query}
            ORDER BY {sort_by}
            LIMIT ?
            OFFSET ?
        """, (limit, (page - 1) * limit))
    rows = cursor.fetchall()
    conn.close()
    return rows

@router.get("/vehicle_page_count")
def get_vehicles_page_number(
    limit: int = 25,
    search: str = None,
):
    conn = get_connection()
    cursor = conn.cursor()
    if search:
        search_pattern = f"%{search}%"

        cursor.execute("""
            SELECT COUNT(*)
            FROM vehicles v
            JOIN predictions p
            ON v.id = p.id
            WHERE 
                v.manufacturer LIKE ?
                OR v.model LIKE ?
                OR v.condition LIKE ?
                OR v.fuel LIKE ?
                OR v.state LIKE ?
        """, (
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
            search_pattern,
        ))

    else:
        cursor.execute("""
            SELECT COUNT(*)
            FROM vehicles v
            JOIN predictions p
            ON v.id = p.id
        """)

    total_rows = cursor.fetchone()[0]
    total_pages = math.ceil(total_rows / limit)

    conn.close()

    return total_pages
 


@router.get("/{vehicle_id}")
def get_vehicle(vehicle_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
    row = cursor.fetchone()
    conn.close()
    return row