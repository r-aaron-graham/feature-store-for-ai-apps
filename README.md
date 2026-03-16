# Feature Store for AI Apps

This repository implements a minimalistic feature store that supports offline and online
storage of features for machine learning applications.  A feature store centralizes
feature definitions, ensures offline/online consistency, and enables feature reuse across
models.  The implementation here is intentionally simple and uses SQLite for persistence
and an in‑memory dictionary for online serving.

## Features

* Define features via Python functions decorated with `@feature`.
* Store computed feature values offline in a SQLite database.
* Serve feature values online via an in‑memory cache with optional TTL.
* Fetch features for a given entity (e.g. user ID) and timestamp.

## Usage

Install dependencies and run the example:

```bash
pip install -r requirements.txt
python example.py
```

The example defines two features (`total_purchases` and `average_purchase`) and populates
the feature store with sample transaction data.  It then retrieves offline features and
serves online features for a user.

## Extending

In a production environment you would integrate with a distributed key‑value store (e.g.
Redis or DynamoDB) for online serving and a data warehouse (e.g. Snowflake) for offline
storage.  This example is meant to illustrate the core concepts with minimal overhead.