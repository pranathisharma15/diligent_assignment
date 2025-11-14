import sqlite3
import pandas as pd

QUERY = """
WITH user_totals AS (
    SELECT user_id, SUM(total_amount) AS lifetime_spend
    FROM orders
    GROUP BY user_id
)
SELECT
    u.user_id,
    u.full_name        AS user_name,
    o.order_id,
    o.order_date,
    p.product_name,
    p.category,
    oi.quantity,
    oi.price_per_unit,
    oi.line_total,
    o.total_amount     AS order_total_amount,
    ut.lifetime_spend
FROM user_totals ut
JOIN users u        ON u.user_id = ut.user_id
JOIN orders o       ON o.user_id = u.user_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p     ON p.product_id = oi.product_id
ORDER BY ut.lifetime_spend DESC, o.order_date DESC;
"""

def main():
    with sqlite3.connect("ecommerce.db") as conn:
        df = pd.read_sql_query(QUERY, conn)
    pd.set_option("display.max_columns", None)
    print(df.to_string(index=False))

if __name__ == "__main__":
    main()