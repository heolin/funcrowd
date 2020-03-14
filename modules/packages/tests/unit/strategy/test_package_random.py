import pytest

from modules.packages.models.search.packages_search import PackagesSearch
from modules.packages.tests.conftest import add_annotation
from tasks.models import Mission
from modules.order_strategy.models import Strategy


@pytest.mark.django_db
def test_tasks(task_with_items, user1, user2, db_random):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="RandomStrategyLogic")
    searcher = PackagesSearch(mp, {})

    orders = set()
    for _ in range(30):
        package = searcher.next_package(user1, None)
        orders.add(package.order)
    assert orders == {1, 2, 3, 4}

    package = mp.packages.first()
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    orders = set()
    for _ in range(30):
        package = searcher.next_package(user1, None)
        orders.add(package.order)
    assert orders == {2, 3, 4}

    orders = set()
    for _ in range(30):
        package = searcher.next_package(user2, None)
        orders.add(package.order)
    assert orders == {1, 2, 3, 4}


@pytest.mark.django_db
def test_max_annotations(task_with_items, user1, user2, db_random):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="RandomStrategyLogic")
    mp.max_annotations = 1
    searcher = PackagesSearch(mp, {})

    orders = set()
    for _ in range(30):
        package = searcher.next_package(user1, None)
        orders.add(package.order)
    assert orders == {1, 2, 3, 4}

    package = mp.packages.first()
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    orders = set()
    for _ in range(30):
        package = searcher.next_package(user1, None)
        orders.add(package.order)
    assert orders == {2, 3, 4}

    orders = set()
    for _ in range(30):
        package = searcher.next_package(user2, None)
        orders.add(package.order)
    assert orders == {2, 3, 4}


@pytest.mark.django_db
def test_search_packages_annotations(packages_with_metadata, user1):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="RandomStrategyLogic")
    mp.max_annotations = 1

    # without any filter
    searcher = PackagesSearch(mp, {})
    orders = set()
    for _ in range(30):
        package = searcher.next_package(user1, None)
        orders.add(package.order)
    assert orders == {0, 1, 2, 3, 4, 5}

    # with filter
    searcher = PackagesSearch(mp, {"country": "Country2"})
    orders = set()
    for _ in range(30):
        package = searcher.next_package(user1, None)
        orders.add(package.order)
    assert orders == {3, 4}

