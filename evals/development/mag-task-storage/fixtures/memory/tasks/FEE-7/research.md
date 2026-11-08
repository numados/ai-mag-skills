# FEE-7 research
Requested: 4 units per started hour, zero at zero minutes, reject negative minutes.
Observed source: src/fees.py, fee(minutes), returns (minutes // 60) * 3.
Approval: research requested; no implementation approval.
Evidence currentness: fixture excerpt only, no source revision established.
Knowledge: ../../knowledge/fee-policy.md records current completed-hour behavior, not future approval.
Next: verify the current source and draft a proposed plan with boundary checks.
