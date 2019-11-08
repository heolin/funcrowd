
NEW = "NEW"
IN_PROGRESS = "IN_PROGRESS"
VERIFICATION = "VERIFICATION"
FINISHED = "FINISHED"

STATUSES = (
    NEW,
    IN_PROGRESS,
    VERIFICATION,
    FINISHED
)


class MissionStatus:
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"


MISSION_STATUSES = (
    (MissionStatus.LOCKED, "Locked"),
    (MissionStatus.UNLOCKED, "Unlocked"),
    (MissionStatus.IN_PROGRESS, "InProgress"),
    (MissionStatus.FINISHED, "Finished"),
)
