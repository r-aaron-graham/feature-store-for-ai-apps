# Feature Store for AI Apps

A local Python example that materializes features in SQLite and serves them
from an in-memory cache. Successful offline updates invalidate cached values
for that entity. Cache misses read persisted values and use the feature
function as a fallback when a registered feature has no stored value.

## Run the demo

```bash
python example.py
```

The bundled transaction fixture returns total purchases of 60.0 and average
purchase of 20.0 from both the offline and online interfaces. The example
stores the latest values in `feature_store.db` in the current directory.
The cache TTL controls when the process rereads persisted values.
