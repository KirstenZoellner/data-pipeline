DROP TABLE IF EXISTS correlation_by_country_year;

CREATE TABLE correlation_by_country_year (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(255),
    year INT,
    pearson_correlation FLOAT,
    lagged_pearson_correlation FLOAT
);
DROP TABLE IF EXISTS gdp_inflation;

CREATE TABLE gdp_inflation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(255),
    year INT,
    gdp_per_capita FLOAT,
    inflation FLOAT
);
