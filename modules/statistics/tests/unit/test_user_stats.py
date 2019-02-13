import pytest


@pytest.mark.django_db
def test_user_stats_task_data(setup_user):
    user = setup_user
    stats = user.stats

    assert stats.annotated_documents == 0
    assert stats.high_agreement_count == 0
    assert stats.agreement_ranking_position == 0
    assert stats.agreement_ranking_percentage == 0.0


@pytest.mark.django_db
def test_user_stats_annotation_data(setup_user, setup_tasks_annotations):
    user = setup_user
    stats = user.stats

    assert stats.annotated_documents == 10
    assert stats.high_agreement_count == 0
    assert stats.agreement_ranking_position == 0
    assert stats.agreement_ranking_percentage == 0.0
