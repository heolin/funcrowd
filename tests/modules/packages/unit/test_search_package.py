import pytest

from modules.packages.models.search.packages_search import PackagesSearch
from tasks.models import Mission


@pytest.mark.django_db
def test_setup_tasks(packages_with_metadata):
    mission = Mission.objects.first()
    assert mission.packages is not None

    mp = mission.packages
    assert mp.packages.count() == 6

    # no search
    search = PackagesSearch(mp, {})
    assert search.items.count() == 6

    # search with one field
    search_query = {"country": "Country1"}
    search = PackagesSearch(mp, search_query)
    assert search.items.count() == 3
    for package in search.items:
        for field, value in search_query.items():
            assert package.metadata[field] == value

    # search with two field
    search_query = {"country": "Country1", "city": "City1"}
    search = PackagesSearch(mp, search_query)
    assert search.items.count() == 2
    for package in search.items:
        for field, value in search_query.items():
            assert package.metadata[field] == value

    # search with one wrong field
    search_query = {"planet": "Earth"}
    search = PackagesSearch(mp, search_query)
    assert search.items.count() == 0

    # search with two fields, one wrong, one correct
    search_query = {"planet": "Earth", "country": "Country1"}
    search = PackagesSearch(mp, search_query)
    assert search.items.count() == 0
