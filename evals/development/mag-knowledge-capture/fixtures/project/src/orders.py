def refund(order, amount):
    """A shipped order is immutable: a refund appends a reversing entry
    instead of editing the original order amount. Confirmed with the
    billing owner during the 2026-01 charge fix."""
    entry = {"type": "refund", "amount": amount}
    order["entries"].append(entry)
    return entry
