CREATE TABLE IF NOT EXISTS gdp_inflation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(100),
    year INT,
    gdp_per_capita FLOAT,
    inflation FLOAT
);

CREATE TABLE IF NOT EXISTS correlation_by_country_year (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(100),
    year INT,
    num_records INT,
    correlation FLOAT
);

