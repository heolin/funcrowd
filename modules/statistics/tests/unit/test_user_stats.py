import pytest

from users.models import EndWorker


@pytest.mark.django_db
def test_user_stats_task_data(user1):
    stats = user1.stats

    assert stats.annotated_documents == 0
    assert stats.high_agreement_count == 0
    assert stats.agreement_ranking_position == 0
    assert stats.agreement_ranking_percentage == 0.0
    assert stats.annotated_missions == 0


@pytest.mark.django_db
def test_user_stats_annotation_data(tasks_annotations):
    high_agreement_counts = [8, 8, 8, 10, 10, 10, 10, 10, 9, 9, 8, 8, 4, 2]
    sorted_counts = sorted(high_agreement_counts, reverse=True)

    for i, user in enumerate(EndWorker.objects.all()):
        stats = user.stats
        assert stats.annotated_documents == 10
        assert stats.high_agreement_count == high_agreement_counts[i]
        assert stats.agreement_ranking_position == sorted_counts.index(stats.high_agreement_count)
        assert round(stats.agreement_ranking_percentage, 2) == \
            round(stats.agreement_ranking_position / EndWorker.objects.count(), 2)
        assert stats.annotated_missions == 1


@pytest.mark.django_db
def test_user_stats_annotation_data(two_missions, user1):
    stats = user1.stats
    stats.update()

    assert stats.annotated_documents == 2
    assert stats.annotated_missions == 2
