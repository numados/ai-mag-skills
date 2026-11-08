from pricing import amount_due


def invoice_total(cents, tax_percent):
    return amount_due(cents, tax_percent)["total"]
