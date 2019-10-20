
class BountyStatus:
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CLOSED = "CLOSED"


STATUSES = (
    (BountyStatus.NEW, "NEW"),
    (BountyStatus.IN_PROGRESS, "IN_PROGRESS"),
    (BountyStatus.FINISHED, "FINISHED"),
    (BountyStatus.CLOSED, "CLOSED")
)
