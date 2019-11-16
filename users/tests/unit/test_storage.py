import pytest


@pytest.mark.django_db
def test_storage(user1, user2):
    storage = user1.get_storage("test")
    assert storage.data == {}

    user1.set_storage("test", {"data": 1})

    storage = user1.get_storage("test")
    assert storage.data == {"data": 1}

    user1.set_storage("test2", {"data": 2})

    storage = user1.get_storage("test")
    assert storage.data == {"data": 1}

    storage = user1.get_storage("test2")
    assert storage.data == {"data": 2}

    user2.set_storage("test", {"data": 2})

    storage = user2.get_storage("test")
    assert storage.data == {"data": 2}
