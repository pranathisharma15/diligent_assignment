## E-Commerce Synthetic Dataset

This project bootstraps a realistic 2024–2025 style e-commerce dataset and demonstrates how to ingest it into a SQLite database for analytics or prototyping.

### Contents
- `generate_ecommerce_data.py` – creates five CSVs with coherent relationships:
  - `users.csv` (50 records) – customer demographics and Prime membership flag.
  - `products.csv` (80) – modern catalog spanning electronics, beauty, fitness, etc.
  - `orders.csv` (150) – payment methods, statuses, ISO timestamps.
  - `order_items.csv` (350) – line-level quantities/prices tied to orders and products.
  - `reviews.csv` (120) – 1–5 star feedback with timestamps.
- `ingest_ecommerce_data.py` – loads the CSVs into `ecommerce.db` using pandas + sqlite3 with referential integrity and indexes.
- `run_query.py` – helper script that outputs a customer/order/product join result, including per-order totals and lifetime spend.

### Prerequisites
- Python 3.11+ (Faker installed for the generator: `pip install faker pandas`)

### Usage
1. **Generate CSVs**
   ```bash
   python generate_ecommerce_data.py
   ```
   Files are written to the repository root.

2. **Ingest into SQLite**
   ```bash
   python ingest_ecommerce_data.py
   ```
   Creates/refreshes `ecommerce.db` with schema, indexes, and data. Shows `Ingestion completed successfully` when done.

3. **Run sample analytics query**
   ```bash
   python run_query.py
   ```
   Prints a table with user details, orders, line items, order totals, and lifetime spend sorted descending.

### Notes
- Faker ensures consistent but realistic values; all IDs are UUIDs to mimic distributed systems.
- Foreign keys are enforced in SQLite, and key columns are indexed for performant joins.
- Adjust volumes or categories by editing the configuration lists near the top of `generate_ecommerce_data.py`.

