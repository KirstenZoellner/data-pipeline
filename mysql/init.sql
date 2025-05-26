DROP DATABASE IF EXISTS btc_djia_data;
CREATE DATABASE btc_djia_data;
USE btc_djia_data;

CREATE TABLE btc_djia_correlation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_date DATE,
    end_date DATE,
    n_days INT,
    correlation FLOAT
);
