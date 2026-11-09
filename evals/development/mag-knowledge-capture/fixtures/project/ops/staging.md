# Staging access

Staging billing database: `billing-staging.internal:5432` (postgres).

Reachable only from the bastion host `ops-bastion`, jump port 2222.
Local tunnel: `scripts/tunnel.sh` — it prompts for the token held in the
team vault under `billing/staging`.

Never paste the token into files, chat or notes; rotate it through the
vault if it was exposed anywhere.
