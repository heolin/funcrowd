import pytest

from tasks.models import Task
from modules.agreement.models import AgreementMetric
from modules.agreement.exceptions import MultipleTempaltesFound


@pytest.mark.django_db
def test_one_field(setup_task_one_variable):
    task = Task.objects.first()
    gwets_gamma, _ = AgreementMetric.objects.get_or_create(name="GwetsGammaMetric")
    for metric in gwets_gamma.evaluate(task):
        assert metric.name == "GwetsGammaMetric"
        assert metric.column == "output"
        assert round(metric.value, 2) == 0.23


@pytest.mark.django_db
def test_high_agreement(setup_task_high_agreement):
    task = Task.objects.first()
    gwets_gamma, _ = AgreementMetric.objects.get_or_create(name="GwetsGammaMetric")
    for metric in gwets_gamma.evaluate(task):
        assert metric.name == "GwetsGammaMetric"
        assert metric.column == "output"
        assert round(metric.value, 2) == 0.66


@pytest.mark.django_db
def test_multiple_templates(setup_task_multiple_templates):
    task = Task.objects.first()
    gwets_gamma, _ = AgreementMetric.objects.get_or_create(name="GwetsGammaMetric")
    with pytest.raises(MultipleTempaltesFound):
        gwets_gamma.evaluate(task)


@pytest.mark.django_db
def test_two_fields(setup_task_two_variables):
    task = Task.objects.first()
    gwets_gamma, _ = AgreementMetric.objects.get_or_create(name="GwetsGammaMetric")
    for metric, column in zip(gwets_gamma.evaluate(task), ["output1", "output2"]):
        assert metric.name == "GwetsGammaMetric"
        assert metric.column == column
        assert round(metric.value, 2) == 0.23


@pytest.mark.django_db
def test_missing_data(setup_task_missing_data):
    task = Task.objects.first()
    gwets_gamma, _ = AgreementMetric.objects.get_or_create(name="GwetsGammaMetric")

    logic = gwets_gamma._logic(task)
    logic.df["output"] = logic.df["data"].apply(lambda x: x["output"])
    counts = logic._get_pivot_table_counts("output")
    assert len(counts) == 9

    for metric in gwets_gamma.evaluate(task):
        assert metric.name == "GwetsGammaMetric"
        assert metric.column == "output"
        assert round(metric.value, 2) == 0.2

