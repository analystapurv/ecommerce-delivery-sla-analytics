"""
run_pipeline.py
Runs the full E-commerce Fulfilment & Delivery SLA Analytics pipeline:
  1. Load and enrich real Olist order/delivery data (load_data.py)
  2. Compute late-delivery rates by state and seller (sla_metrics.py)
  3. Correlate lateness with real review scores (review_correlation.py)
"""

import os
import pandas as pd
from load_data import load_delivered_orders, attach_customer_state, load_order_items, load_reviews
from sla_metrics import late_rate_by_state, late_rate_by_seller
from review_correlation import compute_review_correlation

os.makedirs("../results", exist_ok=True)

print("Step 1/3: Loading and enriching real Olist delivery data...")
delivered = attach_customer_state(load_delivered_orders())
items = load_order_items()
reviews = load_reviews()
delivered.to_csv("../results/delivered_orders_enriched.csv", index=False)
print(f"  {len(delivered)} delivered orders | {delivered['is_late'].sum()} late ({100*delivered['is_late'].mean():.2f}%)")

print("\nStep 2/3: Computing SLA metrics by state and seller...")
by_state = late_rate_by_state(delivered)
by_seller = late_rate_by_seller(delivered, items)
by_state.to_csv("../results/late_rate_by_state.csv")
by_seller.to_csv("../results/late_rate_by_seller.csv")
print("Top 5 states by late-delivery rate:")
print(by_state.head(5))

print("\nStep 3/3: Correlating lateness with real review scores...")
review_stats = compute_review_correlation(delivered, reviews)
print("=== REVIEW SCORE vs LATE DELIVERY ===")
for k, v in review_stats.items():
    print(f"{k}: {v}")

pd.Series(review_stats).to_csv("../results/review_correlation_summary.csv")
print("\nSaved all outputs to results/")
