
NEW = "NEW"
IN_PROGRESS = "IN_PROGRESS"
VERIFICATION = "VERIFICATION"
FINISHED = "FINISHED"
PERMANENT = "PERMANENT"

STATUSES = (
    NEW,
    IN_PROGRESS,
    VERIFICATION,
    FINISHED,
    PERMANENT
)


class MissionStatus:
    HIDDEN = "HIDDEN"
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"


MISSION_STATUSES = (
    (MissionStatus.HIDDEN, "Hidden"),
    (MissionStatus.LOCKED, "Locked"),
    (MissionStatus.UNLOCKED, "Unlocked"),
    (MissionStatus.IN_PROGRESS, "InProgress"),
    (MissionStatus.FINISHED, "Finished"),
)


class TaskStatus:
    LOCKED = "LOCKED"
    UNLOCKED = "UNLOCKED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    PERMANENT = "PERMANENT"


TASK_STATUSES = (
    (TaskStatus.LOCKED, "Locked"),
    (TaskStatus.UNLOCKED, "Unlocked"),
    (TaskStatus.IN_PROGRESS, "InProgress"),
    (TaskStatus.FINISHED, "Finished"),
    (TaskStatus.PERMANENT, "Permanent"),
)


EXP_BONUS_1 = 10
EXP_BONUS_3 = 5
EXP_BONUS_5 = 1
