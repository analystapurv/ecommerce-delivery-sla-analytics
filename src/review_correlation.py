"""
review_correlation.py
Uses real customer review scores as a genuine dissatisfaction proxy,
quantifying the relationship between late delivery and negative reviews.
"""

import pandas as pd


def compute_review_correlation(delivered: pd.DataFrame, reviews: pd.DataFrame) -> dict:
    merged = delivered.merge(reviews[["order_id", "review_score"]], on="order_id", how="inner")
    late = merged[merged["is_late"]]
    on_time = merged[~merged["is_late"]]

    return {
        "orders_with_review_data": len(merged),
        "avg_score_late": round(late["review_score"].mean(), 2),
        "avg_score_on_time": round(on_time["review_score"].mean(), 2),
        "score_gap": round(on_time["review_score"].mean() - late["review_score"].mean(), 2),
        "pct_1_2_star_late": round(100 * (late["review_score"] <= 2).mean(), 1),
        "pct_1_2_star_on_time": round(100 * (on_time["review_score"] <= 2).mean(), 1),
    }


if __name__ == "__main__":
    delivered = pd.read_csv("../results/delivered_orders_enriched.csv")
    reviews = pd.read_csv("/mnt/user-data/uploads/olist_order_reviews_dataset.csv")

    stats = compute_review_correlation(delivered, reviews)
    print("=== REVIEW SCORE vs LATE DELIVERY ===")
    for k, v in stats.items():
        print(f"{k}: {v}")
