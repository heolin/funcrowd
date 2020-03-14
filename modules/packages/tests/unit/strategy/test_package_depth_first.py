import pytest

from modules.packages.models.search.packages_search import PackagesSearch
from modules.packages.tests.conftest import add_annotation
from tasks.models import Mission
from modules.order_strategy.models import Strategy


@pytest.mark.django_db
def test_tasks_one_user(task_with_items, user1):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    searcher = PackagesSearch(mp, {})

    package = searcher.next_package(user1, None)
    assert package.order == 1
    package = searcher.next_package(user1, package)
    assert package.order == 1

    add_annotation(package, package.items.all()[0], user1)
    package = searcher.next_package(user1, package)
    assert package.order == 1

    add_annotation(package, package.items.all()[1], user1)
    package = searcher.next_package(user1, package)
    assert package.order == 2

    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)
    package = searcher.next_package(user1, package)
    assert package.order == 3

    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)
    package = searcher.next_package(user1, package)
    assert package.order == 4

    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)
    package = searcher.next_package(user1, package)
    assert package is None


@pytest.mark.django_db
def test_tasks_two_users(task_with_items, user1, user2):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    searcher = PackagesSearch(mp, {})

    package = searcher.next_package(user1, None)
    assert package.order == 1
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    package = searcher.next_package(user2, package)
    assert package.order == 2
    add_annotation(package, package.items.all()[0], user2)
    add_annotation(package, package.items.all()[1], user2)

    package = searcher.next_package(user1, package)
    assert package.order == 3

    package = searcher.next_package(user2, package)
    assert package.order == 3
    add_annotation(package, package.items.all()[0], user2)

    package = searcher.next_package(user1, package)
    assert package.order == 3

    """
    # this part is not working yet, since we are using wrongly defined annotations_done
    add_annotation(package, package.items.all()[0], user1)

    package = mp.next_package(user2, package)
    assert package.order == 3

    add_annotation(package, package.items.all()[1], user1)

    package = mp.next_package(user1, package)
    assert package.order == 4
    """


@pytest.mark.django_db
def test_max_annotations(task_with_items, user1, user2):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    mp.max_annotations = 1
    searcher = PackagesSearch(mp, {})

    package = searcher.next_package(user1, None)
    assert package.order == 1
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    package = searcher.next_package(user2, None)
    assert package.order == 2
    add_annotation(package, package.items.all()[0], user2)
    add_annotation(package, package.items.all()[1], user2)

    package = searcher.next_package(user2, None)
    assert package.order == 3

    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    package = searcher.next_package(user1, None)
    assert package.order == 4

    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    package = searcher.next_package(user1, None)
    assert package is None


@pytest.mark.django_db
def test_search_packages_annotations(packages_with_metadata, user1):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="DepthFirstStrategyLogic")
    mp.max_annotations = 1

    # without any filter
    searcher = PackagesSearch(mp, {})
    package = searcher.next_package(user1, None)
    assert package.order == 0

    # with filter
    searcher = PackagesSearch(mp, {"country": "Country2"})
    package = searcher.next_package(user1, None)
    assert package.order == 3

    for item in package.items.all():
        add_annotation(package, item, user1)

    package = searcher.next_package(user1, None)
    assert package.order == 4

    for item in package.items.all():
        add_annotation(package, item, user1)

    package = searcher.next_package(user1, None)
    assert package is None
