"""Simple feature store for demonstration purposes."""

from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional


@dataclass
class Feature:
    """Definition of a feature."""

    name: str
    func: Callable[[Dict[str, Any], float], Any]


class FeatureStore:
    """In‑memory and offline feature store."""

    def __init__(self, db_path: Path | str = "feature_store.db") -> None:
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self._init_schema()
        self.features: Dict[str, Feature] = {}
        self.online_cache: Dict[tuple, tuple[float, Any]] = {}

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS feature_values (
                entity_id TEXT NOT NULL,
                feature_name TEXT NOT NULL,
                value BLOB,
                timestamp REAL NOT NULL,
                PRIMARY KEY (entity_id, feature_name)
            );
            """
        )
        self.conn.commit()

    def register_feature(self, name: str, func: Callable[[Dict[str, Any], float], Any]) -> None:
        self.features[name] = Feature(name=name, func=func)

    def compute_offline(self, entity_id: str, data: Dict[str, Any], ts: float) -> None:
        """Compute all features for an entity and persist them offline."""
        cur = self.conn.cursor()
        for feature in self.features.values():
            value = feature.func(data, ts)
            cur.execute(
                "INSERT OR REPLACE INTO feature_values (entity_id, feature_name, value, timestamp) VALUES (?, ?, ?, ?)",
                (entity_id, feature.name, value, ts),
            )
        self.conn.commit()

    def get_offline(self, entity_id: str) -> Dict[str, Any]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT feature_name, value FROM feature_values WHERE entity_id = ?",
            (entity_id,),
        )
        rows = cur.fetchall()
        return {name: value for name, value in rows}

    def get_online(self, entity_id: str, ttl: float = 60.0) -> Dict[str, Any]:
        """Retrieve feature values from the online cache, computing on miss or stale."""
        now = time.time()
        result: Dict[str, Any] = {}
        for name, feature in self.features.items():
            key = (entity_id, name)
            entry = self.online_cache.get(key)
            if entry and now - entry[0] < ttl:
                result[name] = entry[1]
                continue
            # Compute fresh value.  In a real system you would call a streaming computation or DB.
            value = feature.func({}, now)
            self.online_cache[key] = (now, value)
            result[name] = value
        return result