import pytest

from modules.packages.models.search.packages_search import PackagesSearch
from modules.order_strategy.models import Strategy


@pytest.mark.django_db
def test_tasks(packages_with_items, user1, user2):
    mp = packages_with_items
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
def test_annotations(packages_with_annotated_items, user1, user2):
    mp = packages_with_annotated_items
    mp.strategy = Strategy.objects.get(name="StaticStrategyLogic")
    searcher = PackagesSearch(mp, {})

    package = searcher.next_package(user1, None)
    assert package.order == 3
    package = searcher.next_package(user1, package)
    assert package.order == 4

    package = searcher.next_package(user2, None)
    assert package.order == 2


@pytest.mark.django_db
def test_search_packages_annotations(packages_with_metadata, user1):
    mp = packages_with_metadata
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
