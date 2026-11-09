def charge_minutes(minutes):
    # Billing charges 4 units per started hour; zero minutes cost nothing.
    # Negative minutes are rejected upstream by the API validator.
    if minutes <= 0:
        return 0
    return 4 * ((minutes + 59) // 60)
