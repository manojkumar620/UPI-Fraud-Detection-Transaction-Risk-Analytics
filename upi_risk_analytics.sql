CREATE DATABASE IF NOT EXISTS upi_risk_analytics;
USE upi_risk_analytics;

CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    risk_segment VARCHAR(50),
    account_creation_date DATE
);

CREATE TABLE dim_device (
    device_id INT PRIMARY KEY,
    hardware_token VARCHAR(100),
    root_status_flag INT,
    os_version VARCHAR(30)
);

CREATE TABLE dim_merchant (
    merchant_id INT PRIMARY KEY,
    category VARCHAR(50),
    chargeback_rate DECIMAL(5,2)
);

CREATE TABLE fact_transactions (
    txn_id BIGINT PRIMARY KEY,
    customer_id INT,
    device_id INT,
    merchant_id INT,
    txn_timestamp DATETIME,
    amount INT,
    transaction_status VARCHAR(30),
    geographic_city VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (device_id) REFERENCES dim_device(device_id),
    FOREIGN KEY (merchant_id) REFERENCES dim_merchant(merchant_id)
);

CREATE INDEX idx_txn_timestamp ON fact_transactions(txn_timestamp);
CREATE INDEX idx_customer_txn ON fact_transactions(customer_id, txn_timestamp);
CREATE INDEX idx_device_txn ON fact_transactions(device_id);