
class UserPackageStatus:
    NONE = "NONE"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"


USER_PACKAGE_STATUSES = (
    (UserPackageStatus.NONE, "None"),
    (UserPackageStatus.IN_PROGRESS, "InProgress"),
    (UserPackageStatus.FINISHED, "Finished"),
)
