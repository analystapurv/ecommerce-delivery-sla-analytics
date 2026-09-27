# E-commerce Fulfilment & Delivery SLA Analytics

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.2-black)
![Status](https://img.shields.io/badge/status-validated-brightgreen)

An analysis of real order-to-delivery timelines to identify late-delivery
drivers by region and seller, and a quantified link between delivery
lateness and customer dissatisfaction using real review data.

## Dataset
[Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
by Olist — **96,470 real delivered orders** with valid delivery and estimate
dates, joined against **96,353 real customer reviews**.

## Problem statement
Late deliveries are one of the biggest drivers of customer churn in
e-commerce, but "late" needs to be measured against what the customer was
promised, not an arbitrary cutoff. This project compares actual delivery
dates against the *estimated* delivery date shown to the customer at
checkout, breaks down where lateness is concentrated (by state, by
seller), and uses real review scores — not a simulated churn label — as a
genuine, defensible proxy for customer dissatisfaction caused by late
delivery.

## Architecture
```
Real Olist tables (orders, customers, items, reviews)
        │
        ▼
  load_data.py ──► delivered_orders_enriched.csv
        │           (filters to delivered orders, computes is_late,
        │            delivery_delta_days, joins customer_state)
        ▼
 sla_metrics.py ──► late_rate_by_state.csv
        │       └─► late_rate_by_seller.csv
        ▼
review_correlation.py ──► review_correlation_summary.csv
        ▼
   run_pipeline.py  (orchestrates all steps, prints summary)
```

## Real results (computed by running `run_pipeline.py`)

### Delivery SLA
| Metric | Value |
|---|---|
| Delivered orders analyzed (valid dates) | 96,470 |
| **Late deliveries** | **7,826 (8.11%)** |
| Avg days late (when late) | 9.55 |
| Avg days early (when on-time) | 13.01 |

### Worst states by late-delivery rate (min. 50 orders)
| State | Late rate | Orders |
|---|---|---|
| AL (Alagoas) | 23.93% | 397 |
| MA (Maranhão) | 19.67% | 717 |
| PI (Piauí) | 15.97% | 476 |
| CE (Ceará) | 15.32% | 1,279 |
| SE (Sergipe) | 15.22% | 335 |

881 sellers were analyzed (min. 20 orders each); the worst-performing
seller had a 50.0% late-delivery rate.

### Review score vs. late delivery (real dissatisfaction proxy)
| Metric | Late deliveries | On-time deliveries |
|---|---|---|
| Avg review score | 2.57 / 5 | 4.29 / 5 |
| % giving a 1-2 star review | 54.0% | 9.2% |

**Score gap: 1.73 points.** Customers with a late delivery were roughly
5.9x more likely to leave a 1-2 star review than customers whose order
arrived on time.

All numbers above are the direct, unedited output of running the code —
see `results/delivered_orders_enriched.csv`, `results/late_rate_by_state.csv`,
and `results/late_rate_by_seller.csv` for full breakdowns.

## What this demonstrates for an FDE role
- Turning a vague business question ("why are customers churning?") into
  a measurable, evidence-backed metric
- Joining multiple real operational tables (orders, customers, items,
  reviews) the way a real fulfilment analytics stack would
- Segmenting a problem by dimension (state, seller) to find where to
  intervene, rather than reporting a single aggregate number

## How to run it
```bash
pip install -r requirements.txt
cd src
python run_pipeline.py
```
Update the `DATA_DIR` constant in `load_data.py` to point to your local
folder containing the Olist CSV files first.

## Project structure
```
src/
  load_data.py           # loads/merges real Olist tables, computes lateness
  sla_metrics.py           # late-rate breakdowns by state and seller
  review_correlation.py    # review score vs. lateness analysis
  run_pipeline.py           # orchestrates the full pipeline end to end
results/
  delivered_orders_enriched.csv
  late_rate_by_state.csv
  late_rate_by_seller.csv
  review_correlation_summary.csv
requirements.txt
```
