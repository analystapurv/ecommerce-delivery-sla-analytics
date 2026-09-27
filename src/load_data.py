"""
load_data.py
Loads the real Olist orders, customers, items, and reviews tables, filters
to genuinely delivered orders with valid dates, and computes the core
delivery-lateness fields used by the rest of the pipeline.
"""

import pandas as pd

DATA_DIR = "C:/Data engineer/Group B/project3/data"


def load_delivered_orders() -> pd.DataFrame:
    orders = pd.read_csv(
        f"{DATA_DIR}/olist_orders_dataset.csv",
        parse_dates=["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"],
    )
    delivered = orders[orders["order_status"] == "delivered"].dropna(
        subset=["order_delivered_customer_date", "order_estimated_delivery_date"]
    ).copy()

    delivered["delivery_delta_days"] = (
        delivered["order_delivered_customer_date"] - delivered["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400
    delivered["is_late"] = delivered["delivery_delta_days"] > 0
    return delivered


def attach_customer_state(delivered: pd.DataFrame) -> pd.DataFrame:
    customers = pd.read_csv(f"{DATA_DIR}/olist_customers_dataset.csv")
    return delivered.merge(customers[["customer_id", "customer_state"]], on="customer_id", how="left")


def load_order_items() -> pd.DataFrame:
    return pd.read_csv(f"{DATA_DIR}/olist_order_items_dataset.csv")


def load_reviews() -> pd.DataFrame:
    return pd.read_csv(f"{DATA_DIR}/olist_order_reviews_dataset.csv")


if __name__ == "__main__":
    delivered = attach_customer_state(load_delivered_orders())
    delivered.to_csv("../results/delivered_orders_enriched.csv", index=False)
    print(f"Loaded {len(delivered)} delivered orders with valid delivery + estimate dates")
    print(f"Late deliveries: {delivered['is_late'].sum()} ({100*delivered['is_late'].mean():.2f}%)")
