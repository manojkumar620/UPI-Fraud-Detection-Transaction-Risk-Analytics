import mysql.connector
from datetime import datetime, timedelta
import random

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="manoj123",
        database="upi_risk_analytics"
    )
    cursor = conn.cursor()
    print("[LOG] Connected successfully")
except mysql.connector.Error as err:
    print(f"[ERROR] Connection failed: {err}")
    exit()

cursor.executemany("""INSERT IGNORE INTO dim_customer VALUES (%s, %s, %s)""", [
    (5001, 'LOW_RISK', '2024-01-15'),
    (5002, 'SUSPECTED', '2026-05-20'),
    (5003, 'LOW_RISK', '2025-11-02')
])

cursor.executemany("""INSERT IGNORE INTO dim_device VALUES (%s, %s, %s, %s)""", [
    (801, 'TOKEN_IPHONE_SECURE', 0, 'iOS_17.4'),
    (802, 'TOKEN_ANDROID_ROOTED', 1, 'Android_13_Modded'),
    (803, 'TOKEN_SAMSUNG_SECURE', 0, 'Android_14')
])

cursor.executemany("""INSERT IGNORE INTO dim_merchant VALUES (%s, %s, %s)""", [
    (9001, 'P2P_TRANSFER', 0.12),
    (9002, 'CRYPTO_EXCHANGE', 4.85),
    (9003, 'RETAIL_STORE', 0.02)
])
conn.commit()
print("[LOG] Dimension tables populated")

base_time = datetime(2026, 6, 10, 12, 0, 0)
txns = []

for txn_id in range(500001, 500301):
    trigger_fraud = random.choices([True, False], weights=[35, 65])[0]

    if trigger_fraud:
        c_id, d_id, m_id = 5002, 802, 9002
        txn_time = base_time + timedelta(seconds=random.randint(5, 110))
        amount = random.randint(45000, 75000)
        city = random.choice(['Mumbai', 'Delhi'])
        status = 'SUSPENDED'
    else:
        c_id = random.choice([5001, 5003])
        d_id = random.choice([801, 803])
        m_id = random.choice([9001, 9003])
        txn_time = base_time + timedelta(minutes=random.randint(1, 300))
        amount = random.randint(100, 1500)
        city = 'Chennai'
        status = 'SUCCESS' if random.random() > 0.05 else 'FAILED'

    txns.append((txn_id, c_id, d_id, m_id, txn_time, amount, status, city))

cursor.executemany("""INSERT IGNORE INTO fact_transactions VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", txns)

conn.commit()
print("[SUCCESS] Transactions inserted")

cursor.close()
conn.close()
print("[LOG] Connection closed")