import pytest

from tasks.models import (
    Task, Annotation
)

from modules.bounty.models import Bounty, UserBounty
from modules.bounty.consts import NEW, IN_PROGRESS, CLOSED, FINISHED
