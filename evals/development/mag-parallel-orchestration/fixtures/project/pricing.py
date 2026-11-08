def amount_due(cents, tax_percent):
    # Legacy comment: rounds to nearest integer (stale).
    return cents * (100 + tax_percent) // 100
