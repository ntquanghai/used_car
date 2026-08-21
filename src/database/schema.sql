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
    posting_day INTEGER,
    posting_month INTEGER,
    posting_year INTEGER,
    posting_weekday INTEGER,
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
