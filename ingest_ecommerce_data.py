import sqlite3
from pathlib import Path

import pandas as pd


WORKDIR = Path(__file__).resolve().parent
DB_PATH = WORKDIR / "ecommerce.db"


def load_csv(file_name: str) -> pd.DataFrame:
    df = pd.read_csv(WORKDIR / file_name)
    return df


def normalize_users(df: pd.DataFrame) -> pd.DataFrame:
    df["is_prime_member"] = (
        df["is_prime_member"].astype(str).str.lower().isin({"true", "1", "yes"})
    )
    return df


def create_schema(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON;")

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            created_at TEXT NOT NULL,
            country TEXT,
            gender TEXT,
            age INTEGER CHECK(age >= 0),
            is_prime_member INTEGER NOT NULL CHECK(is_prime_member IN (0, 1))
        );
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            sub_category TEXT,
            brand TEXT,
            price REAL NOT NULL CHECK(price >= 0),
            rating REAL CHECK(rating BETWEEN 0 AND 5),
            stock_quantity INTEGER NOT NULL CHECK(stock_quantity >= 0)
        );
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            order_date TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            order_status TEXT NOT NULL,
            total_amount REAL NOT NULL CHECK(total_amount >= 0),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            price_per_unit REAL NOT NULL CHECK(price_per_unit >= 0),
            line_total REAL NOT NULL CHECK(line_total >= 0),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            review_id TEXT PRIMARY KEY,
            product_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
            review_text TEXT,
            review_date TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """
    )

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_reviews_product_id ON reviews(product_id);"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id);"
    )


def clear_tables(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM reviews;")
    conn.execute("DELETE FROM order_items;")
    conn.execute("DELETE FROM orders;")
    conn.execute("DELETE FROM products;")
    conn.execute("DELETE FROM users;")


def insert_dataframe(conn: sqlite3.Connection, table: str, df: pd.DataFrame) -> None:
    placeholders = ", ".join(["?"] * len(df.columns))
    columns = ", ".join(df.columns)
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    conn.executemany(sql, df.itertuples(index=False, name=None))


def main() -> None:
    users_df = normalize_users(load_csv("users.csv"))
    products_df = load_csv("products.csv")
    orders_df = load_csv("orders.csv")
    order_items_df = load_csv("order_items.csv")
    reviews_df = load_csv("reviews.csv")

    with sqlite3.connect(DB_PATH) as conn:
        create_schema(conn)
        clear_tables(conn)

        insert_dataframe(conn, "users", users_df)
        insert_dataframe(conn, "products", products_df)
        insert_dataframe(conn, "orders", orders_df)
        insert_dataframe(conn, "order_items", order_items_df)
        insert_dataframe(conn, "reviews", reviews_df)

        conn.commit()

    print("Ingestion completed successfully")


if __name__ == "__main__":
    main()

