# Synthetic operational observations
Source: fixture-only trace sample at current upload volume.
- Upload A: arrived 10:01:00; next poll 10:20:00; report ready 10:20:00.300.
- Upload B: arrived 10:21:00; next poll 10:40:00; report ready 10:40:00.280.
- No backlog remained after either poll; one worker handled both.
These two traces support a polling-delay explanation for the sample, not a general throughput guarantee.
