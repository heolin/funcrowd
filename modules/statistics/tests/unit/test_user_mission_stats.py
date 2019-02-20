import pytest

from tasks.models import Mission


@pytest.mark.django_db
def test_user_mission_stats_task_data(setup_user, setup_other_user, setup_tasks):
    mission = Mission.objects.first()
    user = setup_user
    stats = user.get_mission_stats(mission.id)

    assert stats.annotated_documents == 0
    assert stats.high_agreement_count == 0
    assert stats.agreement_ranking_position == 0
    assert stats.agreement_ranking_percentage == 0.0

    user = setup_other_user
    stats = user.get_mission_stats(mission.id)
    assert stats.annotated_documents == 0

    mission = Mission.objects.last()
    stats = user.get_mission_stats(mission.id)
    assert stats.annotated_documents == 0


@pytest.mark.django_db
def test_user_mission_stats_annotation_data(setup_user, setup_tasks_annotations):
    mission = Mission.objects.first()
    user = setup_user
    stats = user.get_mission_stats(mission.id)

    assert stats.annotated_documents == 6
    assert stats.high_agreement_count == 0
    assert stats.agreement_ranking_position == 0
    assert stats.agreement_ranking_percentage == 0.0
