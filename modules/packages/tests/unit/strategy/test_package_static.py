import pytest

from modules.packages.models.search.packages_search import PackagesSearch
from tasks.models import Mission
from modules.order_strategy.models import Strategy


@pytest.mark.django_db
def test_tasks(task_with_items, user1, user2):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="StaticStrategyLogic")
    searcher = PackagesSearch(mp, {})

    package = searcher.next_package(user1, None)
    assert package.order == 1
    package = searcher.next_package(user1, package)
    assert package.order == 2
    package = searcher.next_package(user1, package)
    assert package.order == 3
    package = searcher.next_package(user1, package)
    assert package.order == 4
    package = searcher.next_package(user1, package)
    assert package.order == 5
    package = searcher.next_package(user1, package)
    assert package is None

    package = searcher.next_package(user2, None)
    assert package.order == 1


@pytest.mark.django_db
def test_annotations(annotations, user1, user2):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="StaticStrategyLogic")
    searcher = PackagesSearch(mp, {})

    package = searcher.next_package(user1, None)
    assert package.order == 1
    package = searcher.next_package(user1, package)
    assert package.order == 2

    package = searcher.next_package(user2, None)
    assert package.order == 1


@pytest.mark.django_db
def test_max_annotations(annotations, user1, user2):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="StaticStrategyLogic")
    mp.max_annotations = 1
    searcher = PackagesSearch(mp, {})

    package = searcher.next_package(user1, None)
    assert package.order == 1
    package = searcher.next_package(user1, package)
    assert package.order == 2

    package = searcher.next_package(user2, None)
    assert package.order == 1


@pytest.mark.django_db
def test_search_packages_annotations(packages_with_metadata, user1):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="StaticStrategyLogic")
    mp.max_annotations = 1

    # without any filter
    searcher = PackagesSearch(mp, {})
    package = searcher.next_package(user1, None)
    assert package.order == 0

    # with filter
    searcher = PackagesSearch(mp, {"country": "Country2"})
    package = searcher.next_package(user1, None)
    assert package.order == 3
