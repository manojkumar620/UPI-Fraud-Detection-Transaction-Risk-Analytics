SELECT 
    customer_id,
    COUNT(txn_id) AS consecutive_txn_count,
    MAX(amount) AS highest_fraud_ticket,
    geographic_city
FROM fact_transactions
WHERE txn_timestamp BETWEEN '2026-06-10 12:00:00' AND '2026-06-10 12:02:00'
GROUP BY customer_id, geographic_city
HAVING consecutive_txn_count > 10;