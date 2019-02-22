import pytest

from tasks.models import Mission, Annotation
from users.models import EndWorker


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
def test_user_mission_stats_annotation_data(setup_tasks_annotations):
    mission = Mission.objects.first()

    high_agreement_counts = [8, 8, 8, 10, 10, 10, 10, 10, 9, 9, 8, 8, 4, 2]
    sorted_counts = sorted(high_agreement_counts, reverse=True)

    for i, user in enumerate(EndWorker.objects.all()):
        stats = user.get_mission_stats(mission.id)
        assert stats.annotated_documents == 10
        assert stats.high_agreement_count == high_agreement_counts[i]
        assert stats.agreement_ranking_position == sorted_counts.index(stats.high_agreement_count)
        assert round(stats.agreement_ranking_percentage, 2) == \
            round(stats.agreement_ranking_position / EndWorker.objects.count(), 2)
