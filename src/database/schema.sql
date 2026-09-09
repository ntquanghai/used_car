CREATE TABLE vehicles (
    id VARCHAR(50) PRIMARY KEY,
    region VARCHAR(100),
    price REAL,
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    condition VARCHAR(20),
    cylinders VARCHAR(20),
    fuel VARCHAR(20),
    odometer REAL,
    title_status VARCHAR(20),
    transmission VARCHAR(20),
    drive VARCHAR(20),
    type VARCHAR(20),
    paint_color VARCHAR(20),
    state VARCHAR(20),
    lat REAL,
    long REAL,
    posting_hour INTEGER CHECK (posting_hour >= 0 AND posting_hour <= 23),
    posting_day INTEGER CHECK (posting_day >= 1 AND posting_day <= 31),
    posting_month INTEGER CHECK (posting_month >= 1 AND posting_month <= 12),
    posting_year INTEGER CHECK (posting_year >= 1995 AND posting_year <= 2100),
    posting_weekday INTEGER CHECK (posting_weekday >= 0 AND posting_weekday <= 6),
    vehicle_age INTEGER,
    miles_per_year REAL
);

CREATE TABLE predictions (
    id VARCHAR(50) PRIMARY KEY,
    actual_price REAL,
    predicted_price REAL,
    residual REAL,
    absolute_error REAL,
    FOREIGN KEY(id) REFERENCES vehicles(id)
);
