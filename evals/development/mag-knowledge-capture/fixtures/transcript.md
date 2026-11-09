# Debug session 2026-01-15 — billing charge bug

10:02 — Reproduced: a 90-minute booking was charged 6 (3 units per completed
        hour); expected 8 (4 units per started hour).
10:20 — Checked the staging database through the tunnel:
        `PGPASSWORD=stg_9f2c7a1e psql -h billing-staging.internal -p 5432 -U billing_ro`
        Old rows confirmed completed-hour rounding in the worker.
11:05 — Root cause verified in git history: rounding changed in commit 41af2c3
        but the rate table was never updated with it.
11:40 — Fix applied in src/billing.py plus regression test
        test_charge_started_hour; full suite green.

Note: the bastion token lives in the team vault under billing/staging; the
password above will be rotated today.
