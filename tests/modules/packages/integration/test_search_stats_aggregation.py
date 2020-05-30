import pytest
from django.test import Client

from tasks.models import Mission


@pytest.mark.django_db
def test_search_stats_packages(packages_with_metadata_and_statuses, user1, user2):
    client = Client()

    mission = Mission.objects.first()

    # get stats for not logged user
    response = client.get(f'/api/v1/missions/{mission.id}/search/stats/?search=country:Country1&aggregation=city')
    assert response.status_code == 200

    expected_values = [
        {
            'field': "city",
            'value': 'City1',
            'package_status': {
                'FINISHED': 1,
                'IN_PROGRESS': 1,
                'NEW': 0,
                'VERIFICATION': 0,
            },
            'user_status': {},
            'total': 2
        },
        {
            'field': 'city',
            'value': 'City2',
            'package_status': {
                'FINISHED': 0,
                'IN_PROGRESS': 0,
                'NEW': 1,
                'VERIFICATION': 0,
            },
            'user_status': {},
            'total': 1
        }
    ]

    assert len(response.data) == 2
    for response_data, expected_data in zip(response.data, expected_values):
        assert response_data == expected_data

    # get stats for user 1
    client.force_login(user1)
    response = client.get(f'/api/v1/missions/{mission.id}/search/stats/?search=country:Country1&aggregation=city')
    assert response.status_code == 200

    expected_values = [
        {
            'field': "city",
            'value': 'City1',
            'package_status': {
                'FINISHED': 1,
                'IN_PROGRESS': 1,
                'NEW': 0,
                'VERIFICATION': 0,
            },
            'user_status': {
                'FINISHED': 1,
                'IN_PROGRESS': 1,
                'NONE': 0
            },
            'total': 2
        },
        {
            'field': 'city',
            'value': 'City2',
            'package_status': {
                'FINISHED': 0,
                'IN_PROGRESS': 0,
                'NEW': 1,
                'VERIFICATION': 0,
            },
            'user_status': {},
            'total': 1
        }
    ]

    assert len(response.data) == 2
    for response_data, expected_data in zip(response.data, expected_values):
        assert response_data == expected_data

    # get stats for user 2
    client.force_login(user2)
    response = client.get(f'/api/v1/missions/{mission.id}/search/stats/?search=country:Country1&aggregation=city')
    assert response.status_code == 200

    expected_values = [
        {
            'field': "city",
            'value': 'City1',
            'package_status': {
                'FINISHED': 1,
                'IN_PROGRESS': 1,
                'NEW': 0,
                'VERIFICATION': 0,
            },
            'user_status': {
                'FINISHED': 1,
                'IN_PROGRESS': 0,
                'NONE': 0
            },
            'total': 2
        },
        {
            'field': 'city',
            'value': 'City2',
            'package_status': {
                'FINISHED': 0,
                'IN_PROGRESS': 0,
                'NEW': 1,
                'VERIFICATION': 0,
            },
            'user_status': {},
            'total': 1
        }
    ]

    assert len(response.data) == 2
    for response_data, expected_data in zip(response.data, expected_values):
        assert response_data == expected_data


@pytest.mark.django_db
def test_stats_packages(packages_with_metadata_and_statuses, user1):
    client = Client()

    mission = Mission.objects.first()

    # get stats for not logged user
    response = client.get(f'/api/v1/missions/{mission.id}/search/stats/?aggregation=city')
    assert response.status_code == 200

    expected_values = [
        {
            'field': 'city',
            'value': 'City1',
            'package_status': {
                'FINISHED': 1,
                'IN_PROGRESS': 1,
                'NEW': 0,
                'VERIFICATION': 0,
            },
            'user_status': {},
            'total': 2
        },
        {
            'field': 'city',
            'value': 'City2',
            'package_status': {
                'FINISHED': 0,
                'IN_PROGRESS': 0,
                'NEW': 1,
                'VERIFICATION': 0,
            },
            'user_status': {},
            'total': 1
        },
        {
            'field': 'city',
            'value': 'City3',
            'package_status': {
                'FINISHED': 0,
                'IN_PROGRESS': 0,
                'NEW': 1,
                'VERIFICATION': 0,
            },
            'user_status': {},
            'total': 1
        },
        {
            'field': 'city',
            'value': 'City4',
            'package_status': {
                'FINISHED': 0,
                'IN_PROGRESS': 0,
                'NEW': 1,
                'VERIFICATION': 0,
            },
            'user_status': {},
            'total': 1
        },
        {
            'field': 'city',
            'value': 'City5',
            'package_status': {
                'FINISHED': 0,
                'IN_PROGRESS': 0,
                'NEW': 1,
                'VERIFICATION': 0,
            },
            'user_status': {},
            'total': 1
        }
    ]

    assert len(response.data) == 5
    for response_data, expected_data in zip(response.data, expected_values):
        assert response_data == expected_data
