import csv
import os
import random
import uuid
from datetime import datetime, timedelta

try:
    from faker import Faker
except ImportError as exc:  # pragma: no cover - dependency guard
    raise SystemExit(
        "Faker is required: install with `pip install faker`"
    ) from exc


def bounded_date(start_days_ago: int, end_days_ago: int) -> datetime:
    now = datetime.utcnow()
    delta = random.randint(end_days_ago, start_days_ago)
    return now - timedelta(days=delta, seconds=random.randint(0, 86400))


def main() -> None:
    fake = Faker()
    random.seed(42)
    Faker.seed(42)

    countries = [
        "United States",
        "Canada",
        "United Kingdom",
        "Germany",
        "Australia",
        "India",
        "Singapore",
        "Brazil",
        "France",
        "Japan",
    ]
    genders = ["Female", "Male", "Non-binary", "Prefer not to say"]

    users = []
    for _ in range(50):
        created_at = fake.date_time_between(start_date="-2y", end_date="now")
        users.append(
            {
                "user_id": str(uuid.uuid4()),
                "full_name": fake.name(),
                "email": fake.unique.email(),
                "phone": f"+1-{fake.msisdn()[0:10]}",
                "created_at": created_at.isoformat(),
                "country": random.choice(countries),
                "gender": random.choice(genders),
                "age": random.randint(18, 70),
                "is_prime_member": random.random() < 0.65,
            }
        )

    categories = {
        "Electronics": ["Smartphones", "Laptops", "Tablets", "Wearables", "Audio"],
        "Home": ["Kitchen", "Decor", "Furniture", "Lighting"],
        "Beauty": ["Skincare", "Makeup", "Haircare"],
        "Fashion": ["Men", "Women", "Athleisure", "Footwear"],
        "Fitness": ["Equipment", "Wearables", "Supplements"],
        "Accessories": ["Bags", "Watches", "Jewelry"],
        "Outdoors": ["Camping", "Travel", "Cycling"],
    }
    brands = [
        "Apex",
        "Nimbus",
        "Solace",
        "PulseGear",
        "UrbanLeaf",
        "Zenova",
        "LumaSkin",
        "Voyage",
        "TempoFit",
        "Crafted",
    ]
    product_adjectives = [
        "Ultra",
        "Pro",
        "Max",
        "Flex",
        "Glow",
        "Pure",
        "Edge",
        "Prime",
        "Air",
        "Nova",
    ]
    product_nouns = [
        "Speaker",
        "Watch",
        "Lamp",
        "Blender",
        "Serum",
        "Sneaker",
        "Mat",
        "Backpack",
        "Camera",
        "Jacket",
        "Bike",
        "Monitor",
        "Headphones",
        "Router",
        "Diffuser",
    ]

    products = []
    for _ in range(80):
        category = random.choice(list(categories.keys()))
        sub_category = random.choice(categories[category])
        products.append(
            {
                "product_id": str(uuid.uuid4()),
                "product_name": f"{random.choice(product_adjectives)} {random.choice(product_nouns)}",
                "category": category,
                "sub_category": sub_category,
                "brand": random.choice(brands),
                "price": round(random.uniform(15, 1800), 2),
                "rating": round(random.uniform(3.2, 4.9), 1),
                "stock_quantity": random.randint(10, 500),
            }
        )

    payment_methods = [
        "Credit Card",
        "Debit Card",
        "PayPal",
        "Apple Pay",
        "Google Pay",
        "BNPL",
    ]
    order_statuses = ["Processing", "Shipped", "Delivered", "Returned"]

    orders = []
    order_items = []

    for _ in range(150):
        user = random.choice(users)
        order_id = str(uuid.uuid4())
        order_date = fake.date_time_between(start_date="-18M", end_date="now")
        payment_method = random.choices(
            payment_methods, weights=[35, 25, 15, 10, 10, 5]
        )[0]
        status = random.choices(order_statuses, weights=[15, 35, 45, 5])[0]

        orders.append(
            {
                "order_id": order_id,
                "user_id": user["user_id"],
                "order_date": order_date.isoformat(),
                "payment_method": payment_method,
                "order_status": status,
                "total_amount": 0.0,
            }
        )

    def add_item(order: dict) -> None:
        product = random.choice(products)
        quantity = random.randint(1, 3)
        price_per_unit = product["price"]
        line_total = round(price_per_unit * quantity, 2)
        order_items.append(
            {
                "order_item_id": str(uuid.uuid4()),
                "order_id": order["order_id"],
                "product_id": product["product_id"],
                "quantity": quantity,
                "price_per_unit": price_per_unit,
                "line_total": line_total,
            }
        )
        order["total_amount"] = round(order["total_amount"] + line_total, 2)

    # Guarantee at least one line per order
    for order in orders:
        add_item(order)

    while len(order_items) < 350:
        add_item(random.choice(orders))

    eligible_users = [order["user_id"] for order in orders]
    reviews = []
    for _ in range(120):
        product = random.choice(products)
        user_id = random.choice(eligible_users)
        reviews.append(
            {
                "review_id": str(uuid.uuid4()),
                "product_id": product["product_id"],
                "user_id": user_id,
                "rating": random.randint(1, 5),
                "review_text": fake.sentence(nb_words=random.randint(8, 18)),
                "review_date": fake.date_time_between(
                    start_date="-12M", end_date="now"
                ).isoformat(),
            }
        )

    files_data = [
        (
            "users.csv",
            users,
            [
                "user_id",
                "full_name",
                "email",
                "phone",
                "created_at",
                "country",
                "gender",
                "age",
                "is_prime_member",
            ],
        ),
        (
            "products.csv",
            products,
            [
                "product_id",
                "product_name",
                "category",
                "sub_category",
                "brand",
                "price",
                "rating",
                "stock_quantity",
            ],
        ),
        (
            "orders.csv",
            orders,
            [
                "order_id",
                "user_id",
                "order_date",
                "payment_method",
                "order_status",
                "total_amount",
            ],
        ),
        (
            "order_items.csv",
            order_items,
            [
                "order_item_id",
                "order_id",
                "product_id",
                "quantity",
                "price_per_unit",
                "line_total",
            ],
        ),
        (
            "reviews.csv",
            reviews,
            [
                "review_id",
                "product_id",
                "user_id",
                "rating",
                "review_text",
                "review_date",
            ],
        ),
    ]

    for filename, rows, headers in files_data:
        path = os.path.join(os.getcwd(), filename)
        with open(path, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    print("Generated:")
    for filename, *_ in files_data:
        print(f" - {filename}")


if __name__ == "__main__":
    main()

