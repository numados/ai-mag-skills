# Synthetic vendor reference: @fixture/memo-cache 2.4
This is authored fixture data, not third-party documentation.
Version source: fixture vendor reference for 2.4, https://memo-cache.example.test/v2/remember
Signature: cache.remember(key, loader, { ttlSeconds })
ttlSeconds is a positive number in seconds. This version does not accept ttlMs.
The key determines isolation; loader executes on a cache miss.
