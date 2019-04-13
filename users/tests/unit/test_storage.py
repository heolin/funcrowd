import pytest


@pytest.mark.django_db
def test_storage(setup_user, setup_other_user):
    storage = setup_user.get_storage("test")
    assert storage.data == {}

    setup_user.set_storage("test", {"data": 1})

    storage = setup_user.get_storage("test")
    assert storage.data == {"data": 1}

    setup_user.set_storage("test2", {"data": 2})

    storage = setup_user.get_storage("test")
    assert storage.data == {"data": 1}

    storage = setup_user.get_storage("test2")
    assert storage.data == {"data": 2}

    setup_other_user.set_storage("test", {"data": 2})

    storage = setup_other_user.get_storage("test")
    assert storage.data == {"data": 2}
