import pytest

from modules.packages.models.search.packages_search import PackagesSearch
from tests.modules.packages.conftest import add_annotation
from tasks.models import Mission
from modules.order_strategy.models import Strategy


@pytest.mark.django_db
def test_tasks_one_user(task_with_items, user1):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")
    searcher = PackagesSearch(mp, {})

    package = searcher.next_package(user1, None)
    assert package.order == 1
    package = searcher.next_package(user1, package)
    assert package.order == 1

    progress = package.get_user_progress(user1)
    print(package.items.all())
    print(progress.__dict__)

    add_annotation(package, package.items.all()[0], user1)
    progress = package.get_user_progress(user1)
    print(progress.__dict__)
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

"""
@pytest.mark.django_db
def test_tasks_two_users(task_with_items, user1, user2):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")
    searcher = PackagesSearch(mp, {})

    package = searcher.next_package(user1, None)
    assert package.order == 1
    add_annotation(package, package.items.all()[0], user1)
    add_annotation(package, package.items.all()[1], user1)

    package = searcher.next_package(user2, package)
    assert package.order == 1
    add_annotation(package, package.items.all()[0], user2)
    add_annotation(package, package.items.all()[1], user2)

    package = searcher.next_package(user1, package)
    assert package.order == 2
    add_annotation(package, package.items.all()[0], user1)

    package = searcher.next_package(user2, package)
    assert package.order == 2
    add_annotation(package, package.items.all()[0], user2)

    package = searcher.next_package(user2, package)
    assert package.order == 2

    add_annotation(package, package.items.all()[1], user2)
    package = searcher.next_package(user2, package)
    assert package.order == 3


@pytest.mark.django_db
def test_max_annotations(task_with_items, user1, user2):
    mission = Mission.objects.first()
    mp = mission.packages
    mp.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")
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
    mp.strategy = Strategy.objects.get(name="BreadthFirstStrategyLogic")
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
"""
