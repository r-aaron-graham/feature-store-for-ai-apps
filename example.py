"""Example usage of the FeatureStore."""

from __future__ import annotations

import time

from feature_store import FeatureStore


def total_purchases(data: dict, ts: float) -> float:
    purchases = data.get("purchases", [])
    return float(sum(purchases))


def average_purchase(data: dict, ts: float) -> float:
    purchases = data.get("purchases", [])
    return float(sum(purchases) / len(purchases)) if purchases else 0.0


def main() -> None:
    store = FeatureStore()
    store.register_feature("total_purchases", total_purchases)
    store.register_feature("average_purchase", average_purchase)
    # Simulate historical transactions for offline computation
    user_id = "user123"
    sample_data = {"purchases": [10.0, 20.0, 30.0]}
    timestamp = time.time()
    store.compute_offline(user_id, sample_data, timestamp)
    offline_feats = store.get_offline(user_id)
    print("Offline features:", offline_feats)
    # Simulate online retrieval with TTL
    online_feats = store.get_online(user_id)
    print("Online features:", online_feats)


if __name__ == "__main__":
    main()