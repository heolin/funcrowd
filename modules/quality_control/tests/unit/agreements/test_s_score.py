import pytest

from tasks.models import Task
from modules.quality_control.models import AgreementMetric
from modules.quality_control.exceptions import MultipleTempaltesFound


@pytest.mark.django_db
def test_one_field(setup_task_one_variable):
    task = Task.objects.first()
    s_score, _ = AgreementMetric.objects.get_or_create(name="SScoreMetric")
    for metric in s_score.evaluate(task):
        assert metric.name == "SScoreMetric"
        assert metric.column == "output"
        assert round(metric.value, 2) == 0.22


@pytest.mark.django_db
def test_high_agreement(setup_task_high_agreement):
    task = Task.objects.first()
    s_score, _ = AgreementMetric.objects.get_or_create(name="SScoreMetric")
    for metric in s_score.evaluate(task):
        assert metric.name == "SScoreMetric"
        assert metric.column == "output"
        assert round(metric.value, 2) == 0.65


@pytest.mark.django_db
def test_multiple_templates(setup_task_multiple_templates):
    task = Task.objects.first()
    s_score, _ = AgreementMetric.objects.get_or_create(name="SScoreMetric")
    with pytest.raises(MultipleTempaltesFound):
        s_score.evaluate(task)


@pytest.mark.django_db
def test_two_fields(setup_task_two_variables):
    task = Task.objects.first()
    s_score, _ = AgreementMetric.objects.get_or_create(name="SScoreMetric")
    for metric, column in zip(s_score.evaluate(task), ["output1", "output2"]):
        assert metric.name == "SScoreMetric"
        assert metric.column == column
        assert round(metric.value, 2) == 0.22


@pytest.mark.django_db
def test_missing_data(setup_task_missing_data):
    task = Task.objects.first()
    s_score, _ = AgreementMetric.objects.get_or_create(name="SScoreMetric")

    logic = s_score._logic(task)
    logic.df["output"] = logic.df["data"].apply(lambda x: x["output"])
    counts = logic._get_pivot_table_counts("output")
    assert len(counts) == 9

    for metric in s_score.evaluate(task):
        assert metric.name == "SScoreMetric"
        assert metric.column == "output"
        assert round(metric.value, 2) == 0.19

