
class UserPackageStatus:
    """
    Possible statuses defining progress of user's annotation for selected Package:

    - NONE - Initial state. The package has no annotations from this user
    - IN_PROGRESS - The package has at least one annotation from this user
    - FINISHED - The user finished annotating this package
    - CLOSED - The package was manually closed regardless the annotation progress
    """

    NONE = "NONE"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    CLOSED = "CLOSED"


USER_PACKAGE_STATUSES = (
    (UserPackageStatus.NONE, "None"),
    (UserPackageStatus.IN_PROGRESS, "InProgress"),
    (UserPackageStatus.FINISHED, "Finished"),
    (UserPackageStatus.CLOSED, "Closed"),
)


class PackageStatus:
    """
    Possible statuses for the Package during annotation:

    - NONE - Initial state. The package has no annotations
    IN_PROGRESS - The package was finished at least one time
    - FINISHED - The package reached required number of annotations:
    (more or equal than `max_annotations / 2` and less than `max_annotations`)
    with a probability of each answer over 0.5.
    - VERIFICATION - If the package's annotations count reached the `max_annotations`,
    and probability of all items is not over 0.5, the package will be moved to `VERIFICATION` status.
    This means this package won't be annotated by more users and should be verified manually.
    - CLOSED - The package was closed manually. This means this package won't be
    annotated by more users.
    """

    NONE = "NONE"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    VERIFICATION = "VERIFICATION"
    CLOSED = "CLOSED"


PACKAGE_STATUSES = (
    (PackageStatus.NONE, "None"),
    (PackageStatus.IN_PROGRESS, "InProgress"),
    (PackageStatus.FINISHED, "Finished"),
    (PackageStatus.VERIFICATION, "Verification"),
    (PackageStatus.CLOSED, "Closed")
)
