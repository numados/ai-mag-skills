# Synthetic fixture, not a production service.
POLL_SECONDS = 1200

def poll_once(inbox, reports):
    for upload in inbox.pending():
        reports.build(upload)  # measured build duration is in support evidence
