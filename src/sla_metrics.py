"""
sla_metrics.py
Computes late-delivery rates broken down by customer state and by seller,
to isolate where fulfilment SLA breaches are concentrated.
"""

import pandas as pd


def late_rate_by_state(delivered: pd.DataFrame, min_orders: int = 50) -> pd.DataFrame:
    by_state = delivered.groupby("customer_state")["is_late"].agg(["mean", "count"])
    by_state = by_state[by_state["count"] >= min_orders].sort_values("mean", ascending=False)
    by_state["late_rate_pct"] = (by_state["mean"] * 100).round(2)
    return by_state.drop(columns="mean")


def late_rate_by_seller(delivered: pd.DataFrame, order_items: pd.DataFrame, min_orders: int = 20) -> pd.DataFrame:
    merged = order_items.merge(delivered[["order_id", "is_late"]], on="order_id", how="inner")
    by_seller = merged.groupby("seller_id")["is_late"].agg(["mean", "count"])
    by_seller = by_seller[by_seller["count"] >= min_orders].sort_values("mean", ascending=False)
    by_seller["late_rate_pct"] = (by_seller["mean"] * 100).round(2)
    return by_seller.drop(columns="mean")


if __name__ == "__main__":
    delivered = pd.read_csv("../results/delivered_orders_enriched.csv")
    items = pd.read_csv("/mnt/user-data/uploads/olist_order_items_dataset.csv")

    by_state = late_rate_by_state(delivered)
    by_seller = late_rate_by_seller(delivered, items)

    print("Top 5 states by late-delivery rate (min 50 orders):")
    print(by_state.head(5))
    print(f"\nSellers analyzed (min 20 orders): {len(by_seller)}")
    print(f"Worst seller late rate: {by_seller['late_rate_pct'].max():.1f}%")

    by_state.to_csv("../results/late_rate_by_state.csv")
    by_seller.to_csv("../results/late_rate_by_seller.csv")
